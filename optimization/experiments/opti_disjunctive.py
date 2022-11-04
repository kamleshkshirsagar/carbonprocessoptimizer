import pyomo.environ as pe
import numpy as np
import math
from abc import ABC
import json
from pyomo.gdp import Disjunct, Disjunction
from matplotlib import pyplot as plt
import pandas as pd


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


def opti_disjunctive_multi_process(processes, carbon_api_data):

    # create model
    m = pe.ConcreteModel()

    # Add carbon data from API in the model
    c_df = pd.read_json(carbon_api_data)
    hr_mins = c_df.index.to_list()
    m.T = pe.Set(initialize=hr_mins)
    T = len(hr_mins)
    m.carbon_value = c_df['value'].to_dict()
    # c_df['value'].to_excel('results.xlsx')
    c_df['timestamp_conv'] = c_df['timestamp'].apply(lambda t: t.replace(tzinfo=None))
    c_df=c_df.drop(['timestamp'], axis=1)
    c_df.to_excel('results.xlsx')

    # problem parameters
    duration = 30         # Working duration of process
    num_proc_starts = 1   # number of process starts should be run (min. would be 1)

    # index set to simplify notation
    m.processes = pe.Set(initialize=processes.keys())
    m.process_pairs = pe.Set(initialize = m.processes * m.processes, dimen=2, filter=lambda m, j, k : j < k)

    # Process is not running except during the working duration
    m.Y = pe.RangeSet(1, T - duration) # TODO: Assumed all processes of same duration. To update this for different durations.
    m.Y_matrix = pe.Set(initialize=m.processes * m.Y)
    # m.Y_combined = pe.Var(m.Y_matrix, initialize=0, domain=pe.NonNegativeReals)

    # This is the process working
    m.S = pe.RangeSet(0, duration - 1) # TODO: Assumed all processes of same duration. To update this for different durations.
    m.S_matrix = pe.Set(initialize=m.processes*m.S)
    # m.S_combined = pe.Var(m.S_matrix, initialize=0, domain=pe.NonNegativeReals)

    # x_t corresponds to the operating mode of the process. x_t = 1 indicates process is operating. 
    # m.x = pe.Var(m.T, domain=pe.Binary)
    m.x_t_matrix = pe.Set(initialize=m.processes*m.T)
    m.x_t_combined = pe.Var(m.x_t_matrix, domain=pe.Binary)

    # y_t indicates first day of process operating
    # m.y = pe.Var(m.processes*m.T, domain=pe.Binary)
    m.y_t_matrix = pe.Set(initialize=m.processes*m.T)
    m.y_t_combined = pe.Var(m.y_t_matrix, domain=pe.Binary)

    # constraints
    m.c = pe.ConstraintList()

    for j in m.processes:
        print(j)
        print([m.y_t_combined[j, t] for t in m.Y_matrix])
        # print([m.y_t_combined[j, t] for t in m.Y_combined[j, :]])
        # Required number of times the process must start: num_proc_starts
        m.c.add(sum(m.y_t_combined[j, t] for t in m.Y_matrix[j, :]) == num_proc_starts)

        # # no more than one start in the period of length duration
        # m.c.add(m.Y, rule = lambda m, t: sum(m.y_t_combined[j][t+s] for s in m.S_combined[j]) <= 1)

        # # The process must start for a period of given duration
        # # disjunctive constraints
        # m.c.add(Disjunction(m.Y, rule = lambda m, t: [m.y_t_combined[j][t]==0, sum(m.x_t_combined[j][t+s] for s in m.S_combined[j])==0]))


    # objective
    m.total_carbon_credits = pe.Objective(expr = sum(m.carbon_value[t]*m.x_t_combined[1] for t in m.T), sense=pe.maximize)

    # transformation and soluton
    pe.TransformationFactory('gdp.hull').apply_to(m)

    pe.SolverFactory('cbc').solve(m).write()
    
    plot_schedule(m)

    return m


def opti_model(processes, carbon_api_data):
    # create model
    m = pe.ConcreteModel()

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
