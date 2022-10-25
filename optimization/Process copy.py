import pyomo.environ as pe
import numpy as np
import math

class Process():

    def __init__(self, overall_process, unit_name, unit_info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.p = overall_process
        self.unit_name = unit_name
        proc_duration = math.ceil(unit_info['duration_mins']/self.p.resolution)
        self.p.m.process_duration = pe.Param(initialize = proc_duration)

        self.p.m.process_opti_start = pe.Var(
            initialize=0, 
            bounds=(self.p.hr_mins[0], self.p.hr_mins[-1]-proc_duration), # Convert to MW. Values input in GW
            within=pe.NonNegativeIntegers)

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
        
        def process_active_rule_1(model, i):
            bigM=5000
            return (bigM*(model.process_active[i]) >= (i - model.process_opti_start))
        self.p.m.process_active_cons1 = pe.Constraint(self.p.m.hr_mins, rule=process_active_rule_1)

        
        def process_active_rule_2(model, i):
            bigM=5000
            return (bigM*(1 - model.process_active[i]) >= (model.process_opti_start + model.process_duration - i))
        self.p.m.process_active_cons2 = pe.Expression(self.p.m.hr_mins, rule=process_active_rule_2)


        def opti_start_last_starting_point_rule(model):
            return model.process_opti_start <= self.p.hr_mins[-1]-model.process_duration
        self.p.m.opti_start_last_starting_point = pe.Constraint(rule=opti_start_last_starting_point_rule)

        return None

    def define_c_credits(self):
        def get_process_c_credits(model): 
            c_credits = sum(model.carbon_value[h]*model.process_active[h] for h in model.hr_mins)
            return c_credits
        self.p.m.process_c_credits = pe.Expression(rule=get_process_c_credits)