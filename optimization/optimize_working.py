import json
import pandas as pd
from pandas import json_normalize
import requests
import pyomo.environ as pe
import numpy as np
import math
from abc import ABC
import json
from pyomo.gdp import Disjunct, Disjunction
from matplotlib import pyplot as plt


def opti_model(processes, carbon_api_data):
    # create model
    m = pe.ConcreteModel()

    # Get carbon data in API model
    c_df = pd.read_json(carbon_api_data)
    hr_mins = c_df.index.to_list()
    m.hr_mins = pe.Set(initialize=hr_mins)
    m.carbon_value = c_df['value'].to_dict()

    # index set to simplify notation
    m.processes = pe.Set(initialize=processes.keys())
    m.process_pairs = pe.Set(initialize = m.processes * m.processes, dimen=2, filter=lambda m, j, k : j < k)


    # decision variables
    m.start = pe.Var(m.processes, domain=pe.NonNegativeReals)
    m.finish = pe.Var(m.processes, domain=pe.NonNegativeReals)
    m.y = pe.Var(m.process_pairs, domain=pe.Boolean)

    def get_total_c_credits(model):
        carbon_credits = 0
        for j in model.processes:
            carbon_credits += model.start[j]# *model.carbon_value[model.start[j]]
        return carbon_credits
    m.total_c_credits = pe.Expression(rule=get_total_c_credits)
    
    # objective function
    m.OBJ = pe.Objective(expr = m.total_c_credits, sense = pe.maximize)
    
    # constraints
    m.c = pe.ConstraintList()
    for j in m.processes:
        # Total process duration should be preserved
        m.c.add(m.finish[j] == m.start[j] + processes[j]['duration'])

        m.c.add(m.start[j] <= processes[j]['end_window']-processes[j]['duration'])

        # Process can start only based on start window
        m.c.add(m.start[j] >= processes[j]['start_window'])

    # TODO: Update this based on the actual dependencies
    # Machine Conflict constraints
    M = 1000.0
    for j,k in m.process_pairs:
        m.c.add(m.finish[j] <= m.start[k] + M*m.y[j,k])
        m.c.add(m.finish[k] <= m.start[j] + M*(1 - m.y[j,k]))

    pe.SolverFactory('cbc').solve(m)
    
    schedule = {}
    for j in m.processes:
        schedule[j] = {'start': m.start[j](), 'finish': m.start[j]() + processes[j]['duration']}
        
    return schedule



def plot_schedule(m):
    fig, ax = plt.subplots(3,1, figsize=(9,4))
    
    min_c_val = min([m.carbon_value[t] for t in m.T])
    ax[0].bar(m.T, [m.carbon_value[t]-min_c_val for t in m.T])
    ax[0].set_title('daily profit $c_t$')
    
    ax[1].bar(m.T, [m.x[t]() for t in m.T], label='normal operation')
    ax[1].set_title('process operating schedule $x_t$')
    
    ax[2].bar(m.Y, [m.y[t]() for t in m.Y])
    ax[2].set_title('1 starts $y_t$')
    for a in ax:
        a.set_xlim(0.1, len(m.T)+0.9)
        
    plt.tight_layout()
    plt.show()


## Look for it here: https://jckantor.github.io/ND-Pyomo-Cookbook/notebooks/04.04-Maintenance-Planning.html
def opti_disjunctive_method(processes, carbon_api_data):

    # create model
    m = pe.ConcreteModel()

    # problem parameters
    duration = 30         # Working duration of process
    num_proc_starts = 1   # number of process starts should be run (min. would be 1)

    # Get carbon data in API model
    c_df = pd.read_json(carbon_api_data)
    hr_mins = c_df.index.to_list()
    m.T = pe.Set(initialize=hr_mins)
    T = len(hr_mins)

    m.carbon_value = c_df['value'].to_dict()

    c_df['value'].to_excel('results.xlsx')

    # Process is not running except during the working duration
    m.Y = pe.RangeSet(1, T - duration)

    # This is the process working
    m.S = pe.RangeSet(0, duration - 1)

    # x_t corresponds to the operating mode of the process. x_t = 1 indicates process is operating. 
    m.x = pe.Var(m.T, domain=pe.Binary)

    # y_t indicates first day of process operating
    m.y = pe.Var(m.T, domain=pe.Binary)

    # objective
    m.total_carbon_credits = pe.Objective(expr = sum(m.carbon_value[t]*m.x[t] for t in m.T), sense=pe.maximize)

    # Required number of times the process must start: num_proc_starts
    m.sumy = pe.Constraint(expr = sum(m.y[t] for t in m.Y) == num_proc_starts)

    # no more than one start in the period of length duration
    m.sprd = pe.Constraint(m.Y, rule = lambda m, t: sum(m.y[t+s] for s in m.S) <= 1)

    # The process must start for a period of given duration
    # disjunctive constraints
    m.disj = Disjunction(m.Y, rule = lambda m, t: [m.y[t]==0, sum(m.x[t+s] for s in m.S)==0])

    # transformation and soluton
    pe.TransformationFactory('gdp.hull').apply_to(m)

    pe.SolverFactory('cbc').solve(m).write()
    
    plot_schedule(m)

    return m



def opt_schedule(processes, carbon_api_data):
    # create model
    m = pe.ConcreteModel()

    # Get carbon data in API model
    c_df = pd.read_json(carbon_api_data)
    hr_mins = c_df.index.to_list()
    m.hr_mins = pe.Set(initialize=hr_mins)
    m.carbon_value = c_df['value'].to_dict()

    # index set to simplify notation
    m.processes = pe.Set(initialize=processes.keys())

    # decision variables
    m.start = pe.Var(m.processes, domain=pe.NonNegativeIntegers)
    m.finish = pe.Var(m.processes, domain=pe.NonNegativeIntegers)
    

    def get_total_c_credits(model):
        carbon_credits = 0
        for j in model.processes:
            carbon_credits += model.start[j]# *model.carbon_value[model.start[j]]
        return carbon_credits
    m.total_c_credits = pe.Expression(rule=get_total_c_credits)
    
    # objective function
    m.OBJ = pe.Objective(expr = m.total_c_credits, sense = pe.maximize)
    
    # constraints
    m.c = pe.ConstraintList()
    for j in m.processes:
        # Total process duration should be preserved
        m.c.add(m.finish[j] == m.start[j] + processes[j]['duration'])

        m.c.add(m.start[j] <= processes[j]['end_window']-processes[j]['duration'])

        # Process can start only based on start window
        m.c.add(m.start[j] >= processes[j]['start_window'])

    pe.SolverFactory('cbc').solve(m)
    
    schedule = {}
    for j in m.processes:
        schedule[j] = {'start': m.start[j](), 'finish': m.start[j]() + processes[j]['duration']}
        
    return schedule

def init():
    print('Inside init')

def request_parser(request, windowSize):
    #extracting process data 
    process_dat=pd.DataFrame.from_records(request['processes'])
    
    url = 'https://carbon-aware-api.azurewebsites.net/emissions/forecasts/current' 
    loc = request['location']
    startTime = str(request['startTime']) 
    endTime = str(request['endTime'])
    final_url= url + '?location=' + request['location'] + '&dataStartAt=' +startTime + '&dataEndAt='+endTime + '&windowSize='+windowSize
    return final_url, process_dat

def nooptim(data, process_data,request):
    carbon_dat=json_normalize(json.loads(data))
    nooptim_proc={}
    return nooptim_proc

def webservice(url):
    response =requests.get(url)
    print(response)
    if response.ok:
        fjson=json.loads(response.text)
        data_file = json.dumps(fjson[0])
        result=json.loads(data_file)['forecastData']
        return str.encode(json.dumps(result))
    else:
        print('Did not get data from Carbon API')
        return None

def restructure_input_req(carbon_api_data, process_data, windowSize):
    c_df = pd.read_json(carbon_api_data)
    indices = c_df.index.to_list()
    start_index = indices[0]
    end_index = indices[-1]
    input = dict()
    for proc in process_data['processes']:
        input[proc['name']] = {
        "start_window": start_index,
        "end_window": end_index,
        "duration": int(proc['duration']/windowSize),
        "dependencies": proc['dependencies']
        }
    return input

def shortest_processing_time(processes):
    schedule = dict()
    unfinished_processes = set(processes.keys())
    start = 0
    while len(unfinished_processes) > 0:
        start = max(start, min(processes[process]['start_window'] for process in unfinished_processes))
        spt = {process:processes[process]['duration'] for process in unfinished_processes if processes[process]['start_window'] <= start}
        process = min(spt, key=spt.get)
        finish = start + processes[process]['duration']
        unfinished_processes.remove(process)
        schedule[process] = {'start': start, 'finish': finish}
        start = finish

    print(schedule)
    return None

def run(request, windowSize=5):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    In the example we extract the data from the json input and call the scikit-learn model's predict()
    method and return the result back
    """
    print("Request received")
    print(request)
    print('creating url for extracting data')
    url, process_df= request_parser(request, str(windowSize))
    print('Getting data based on the request')
    carbon_api_data = webservice(url)

    if carbon_api_data!=None:
        print('calling NO Optimisation')
        nooptim_proc = nooptim(carbon_api_data, process_df, request)

        processes = restructure_input_req(carbon_api_data, request, windowSize)

        print('calling Shortest Processing Time')
        # shortest_processing_time(processes)

        print('calling Optimisation')
        # schedule = opt_schedule(processes, carbon_api_data)=
        # schedule = opti_model(processes, carbon_api_data)
        schedule = opti_disjunctive_method(processes, carbon_api_data)
        print(schedule)

    return carbon_api_data


def main():
    init()
    with open('./optimization/request.json') as f:
        input_req = json.load(f)
    response_api = run(input_req)


if __name__ == "__main__":
    main()

