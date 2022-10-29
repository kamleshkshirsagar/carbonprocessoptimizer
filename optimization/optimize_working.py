import json
import pandas as pd
from pandas import json_normalize
import requests
import pyomo.environ as pe
import numpy as np
import math
from abc import ABC
import json

class Process():

    def __init__(self, overall_process, unit_name, unit_info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.p = overall_process
        self.unit_name = unit_name
        proc_duration = math.ceil(unit_info['duration']/self.p.resolution)
        self.p.m.process_duration = pe.Param(initialize = proc_duration)

        # print(self.p.hr_mins)
        # exit()
        # self.p.m.process_opti_start = pe.Var(
        #     initialize=0, 
        #     bounds=(self.p.hr_mins[0], self.p.hr_mins[-1]), # Convert to MW. Values input in GW
        #     within=pe.NonNegativeIntegers)

        self.p.m.process_active = pe.Var(self.p.m.hr_mins, domain=pe.Boolean, initialize=0)

        self.setup_constraints()

    def get_unit_name(self):
        return self.unit_name  
    
    def setup_constraints(self):


        # Given a process_opti_start value, the process_values will be 1s for the duration

        # Starting from the index of start of process which is given by model.process_opti_start,
        # model.process_active must have 1 for the given duration while everywhere else it should be zero

        # if model.process_opti_start <= i then model.process_active[i] == 1

        # if i <= model.process_opti_start + model.process_duration
        #     model.process_active[i] == 1
        # else
        #     zero


        # def process_size_rule():
        #     model.process_active[i]
        #     return 

        # self.p.m.process_size = pe.Expression(self.p.m.hr_mins, rule=process_size_rule)


        # When i - model.process_opti_start >= 0, model.process_active must be 0 

        # def process_active_rule_1(model, i):
        #     bigM=-5000
        #     return (bigM*(model.process_active[i]) >= (i - model.process_opti_start))
        # self.p.m.process_active_cons1 = pe.Constraint(self.p.m.hr_mins, rule=process_active_rule_1)

        
        # # When i - model.process_opti_start <= 0, model.process_active must be 0

        # def process_active_rule_2(model, i):
        #     bigM=5000
        #     return (bigM*(1 - model.process_active[i]) >= (i - model.process_opti_start))
        # self.p.m.process_active_cons2 = pe.Expression(self.p.m.hr_mins, rule=process_active_rule_2)


        # def opti_start_last_starting_point_rule(model):
        #     return model.process_active[i] <= self.p.hr_mins[-1] 
        # self.p.m.opti_start_last_starting_point = pe.Constraint(rule=opti_start_last_starting_point_rule)

        return None

    def define_c_credits(self):
        def get_process_c_credits(model): 
            c_credits = sum(model.carbon_value[h]*model.process_active[h] for h in model.hr_mins)
            return c_credits
        self.p.m.process_c_credits = pe.Expression(rule=get_process_c_credits)
        print('Defined C credits')

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
    fjson=json.loads(response.text)
    data_file = json.dumps(fjson[0])
    result=json.loads(data_file)['forecastData']
    return str.encode(json.dumps(result))

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

def spt(carbon_api_data, process_data, windowSize):
    processes = restructure_input_req(carbon_api_data, process_data, windowSize)
    SCHEDULE = dict()
    unfinished_processes = set(processes.keys())
    start = 0
    while len(unfinished_processes) > 0:
        start = max(start, min(processes[process]['start_window'] for process in unfinished_processes))
        spt = {process:processes[process]['duration'] for process in unfinished_processes if processes[process]['start_window'] <= start}
        process = min(spt, key=spt.get)
        finish = start + processes[process]['duration']
        unfinished_processes.remove(process)
        SCHEDULE[process] = {'start': start, 'finish': finish}
        start = finish

    print(SCHEDULE)
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
    data = webservice(url)
    print('calling NO Optimisation')
    nooptim_proc = nooptim(data, process_df, request)

    print('calling Shortest Processing Time')
    spt(data, request, windowSize)

    # print('calling Optimisation')
    # opti_model(data, request)

    return data

class ModelData(ABC):
    """
    This is the base class for the optimizer where we define the parent optimization model.
    Data that is used by the individual processes such as carbon api data is also stored here.
    """
    def __init__(self, carbon_api_data):
        self.m = pe.ConcreteModel()
        self.c_df = pd.read_json(carbon_api_data)
        self.hr_mins = self.c_df.index.to_list()
        self.m.hr_mins = pe.Set(initialize=self.hr_mins)
        self.m.carbon_value = self.c_df['value'].to_dict()
        self.resolution = self.c_df['duration'][0]


class Overall_Process(ModelData):
    def __init__(self, carbon_api_data, print_output=False, *args, **kwargs):
        print('Setting up Overall System')
        super().__init__(carbon_api_data, *args, **kwargs)
        self.num_units = []
        self.print_output=print_output

    def get_unit_names_list(self):
        unit_names_list = []
        for unit in self.num_units:
            unit_names_list.append(unit.get_unit_name())
        return unit_names_list

    def add_unit(self, unit_name=None, unit_info=None):
        if 'startTime' in unit_info and 'endTime' in unit_info:
            unit_process = Process(self, unit_name, unit_info)
        else:
            print('Please enter a valid input process')
            return None

        self.num_units.append(unit_process)
        print('Added process ',unit_process.get_unit_name())
        return None

    def set_overall_system_constraints(self):
        return None

    def set_overall_system_c_credits(self):
        units = self.get_unit_names_list()
        for unit in self.num_units:
            unit.define_c_credits()

        def get_total_c_credits(model):
            return model.process_c_credits
        self.m.total_c_credits = pe.Expression(rule=get_total_c_credits)

        return None

    def define_objective_function(self, obj_func='minimize_total_c_credits'):
        self.set_overall_system_c_credits()

        if obj_func=='minimize_total_c_credits':
            def objective_minimize_total_c_credits(model):
                return model.process_c_credits 
            self.m.obj = pe.Objective(rule=objective_minimize_total_c_credits, sense=pe.maximize)

    def export_the_results(self):
        df = pd.DataFrame()
        df['hr_mins'] = self.c_df.index.to_list()
        df['Process'] = [pe.value(self.m.process_active[h]) for h in self.m.hr_mins]
        df['Carbon Values'] =  [pe.value(self.m.carbon_value[h]) for h in self.m.hr_mins]

        df.to_excel('./results.xlsx', index=True)

    def print_output_func(self):
        print('Start index= {}'.format(round(pe.value(self.m.process_opti_start),3)))
        self.export_the_results()

    def solve(self, solver='cbc'):
        solver=pe.SolverFactory(solver)
        results = solver.solve(self.m, tee=True, options={'TimeLimit': 100})
        if(results.solver.status == pe.SolverStatus.ok) and (results.solver.termination_condition == pe.TerminationCondition.optimal):
            print('feasible')
        elif(results.solver.termination_condition == pe.TerminationCondition.infeasible):
            print('infeasible')
        else:
            print('Solver Status:', results.solver.status)

        self.print_output_func() if self.print_output==True else None
        self.results = results
        return None

def opti_model(carbon_api_data, process_data):

    # Setup the overall process model
    overall_process = Overall_Process(carbon_api_data, print_output=True)
    
    # Add each process unit as defined in the json
    for proc in process_data['processes']:
        print("Adding process: ", proc)
        proc_info = {
        "startTime": process_data['startTime'],
        "endTime": process_data['endTime'],
        "duration": proc['duration'],
        "dependencies": proc['dependencies']
        }

        overall_process.add_unit(unit_name=proc['name'], unit_info=proc_info)


    # Add any constraints that would apply to the overall process
    overall_process.set_overall_system_constraints()

    # Define objective function
    overall_process.define_objective_function()

    # Solve for the given objective
    overall_process.solve()

    return round(pe.value(overall_process.m.process_opti_start),3)


def main():
    init()
    with open('./optimization/request.json') as f:
        input_req = json.load(f)
    response_api = run(input_req)


if __name__ == "__main__":
    main()

