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


def opti_disjunctive_method(processes, carbon_api_data):
    """
    Only one process or all processes one after the other as a whole!!!
    """
    process_name = 'p1'
    process = processes[process_name]
    # create model
    m = pe.ConcreteModel()

    # problem parameters
    duration = process['duration']   # Working duration of process
    # number of process starts should be run (min. would be 1)
    num_proc_starts = 1

    # Get carbon data in API model
    c_df = pd.read_json(carbon_api_data)
    c_df.index += 1
    hr_mins = c_df.index.to_list()
    # print(hr_mins)
    m.T = pe.Set(initialize=hr_mins)
    T = len(hr_mins)
    # print([m.T[i] for i in m.T])

    m.carbon_value = c_df['value'].to_dict()

    # Process is not running except during the working duration
    m.Y = pe.RangeSet(1, T - duration+1)

    # This is the process working
    m.S = pe.RangeSet(0, duration - 1)

    # x_t corresponds to the operating mode of the process. x_t = 1 indicates process is operating.
    m.x = pe.Var(m.T, domain=pe.Binary)

    # y_t indicates first day of process operating
    m.y = pe.Var(m.T, domain=pe.Binary)

    # objective
    m.total_carbon_credits = pe.Objective(
        expr=sum(m.carbon_value[t]*m.x[t] for t in m.T), sense=pe.maximize)

    # Required number of times the process must start: num_proc_starts
    m.sumy = pe.Constraint(expr=sum(m.y[t] for t in m.Y) == num_proc_starts)

    # no more than one start in the period of length duration
    m.sprd = pe.Constraint(
        m.Y, rule=lambda m, t: sum(m.y[t+s] for s in m.S) <= 1)

    # The process must start for a period of given duration
    # disjunctive constraints
    m.disj = Disjunction(m.Y, rule=lambda m, t: [
                         m.y[t] == 0, sum(m.x[t+s] for s in m.S) == 0])

    # transformation and soluton
    pe.TransformationFactory('gdp.hull').apply_to(m)

    pe.SolverFactory('cbc').solve(m).write()

    # plot_schedule(m)
    proc_start = [m.y[t]() for t in m.Y]
    start = proc_start.index(1.0)
    finish = start + process['duration']
    schedule = dict()
    schedule[process_name] = {'name': process_name, 'dependencies': process['dependencies'],
                        'duration': process['duration'], 'start': start, 'finish': finish}
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


def init():
    print('Inside init')


def request_parser(request, windowSize):
    # extracting process data
    process_dat = pd.DataFrame.from_records(request['processes'])

    url = 'https://carbon-aware-api.azurewebsites.net/emissions/forecasts/current'
    loc = request['location']
    startTime = str(request['startTime'])
    endTime = str(request['endTime'])
    final_url = url + '?location=' + \
        request['location'] + '&dataStartAt=' + startTime + \
        '&dataEndAt='+endTime + '&windowSize='+windowSize
    return final_url, process_dat


def nooptim(processes, carbon_api_data):
    """
    No optimization but starting with start windown and considering dependencies.
    """
    c_df = pd.read_json(carbon_api_data)
    # print(c_df, processes)
    schedule = dict()
    unfinished_processes = set(processes.keys())
    start = 0

    while len(unfinished_processes) > 0:
        count = 1
        for process in processes:
            if process in unfinished_processes:
                # Start with a process having zero dependencies
                if processes[process]['dependencies'] == None:
                    start = processes[process]['start_window']
                    finish = start + processes[process]['duration']
                    schedule[process] = {'name': process, "dependencies": processes[process]['dependencies'],
                                         "duration": processes[process]['duration'], 'start': start, 'finish': finish}
                    unfinished_processes.remove(process)
                    last_process = process
                    break

                if processes[process]['dependencies'] != None:
                    combined = [i for i in processes[process]
                                ['dependencies'] if i in unfinished_processes]
                    if combined == []:

                        # Start will be after the dependencies
                        start = schedule[last_process]['finish']
                        finish = start + processes[process]['duration']
                        schedule[process] = {'name': process, "dependencies": processes[process]['dependencies'],
                                             "duration": processes[process]['duration'], 'start': start, 'finish': finish}
                        unfinished_processes.remove(process)
                        last_process = process
                        break
            count += 1

        if count >= 10000:
            schedule = None
            return schedule

    return schedule


def webservice(url):
    response = requests.get(url)
    print(response)
    if response.ok:
        fjson = json.loads(response.text)
        data_file = json.dumps(fjson[0])
        result = json.loads(data_file)['forecastData']
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
        start = max(start, min(
            processes[process]['start_window'] for process in unfinished_processes))
        spt = {process: processes[process]['duration']
               for process in unfinished_processes if processes[process]['start_window'] <= start}
        process = min(spt, key=spt.get)
        finish = start + processes[process]['duration']
        unfinished_processes.remove(process)
        schedule[process] = {'name': process, "dependencies": processes[process]['dependencies'],
                             "duration": processes[process]['duration'], 'start': start, 'finish': finish}
        start = finish

    return schedule


def run(request, windowSize=5):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    In the example we extract the data from the json input and call the scikit-learn model's predict()
    method and return the result back
    """
    print("Request received")
    print(request)
    print('creating url for extracting data')
    url, process_df = request_parser(request, str(windowSize))
    print('Getting data based on the request')
    carbon_api_data = webservice(url)

    if carbon_api_data != None:
        processes = restructure_input_req(carbon_api_data, request, windowSize)

        print('calling NO Optimisation')
        nooptim_proc = nooptim(processes, carbon_api_data)

        print('calling Shortest Processing Time')
        shortest_processing_time(processes)

        print('calling Optimisation')
        schedule = opti_disjunctive_method(processes, carbon_api_data)
        # print(schedule)

    return carbon_api_data

def main():
    init()
    with open('./optimization/request.json') as f:
        input_req = json.load(f)
    response_api = run(input_req)


if __name__ == "__main__":
    main()
