import pyomo.environ as pe
import numpy as np

class Process():
    def __init__(self, overall_process, unit_name, unit_info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.p = overall_process
        self.unit_name = unit_name
        self.p.m.process_duration = pe.Param(initialize = unit_info['duration_mins'])

        self.p.m.process_opti_start = pe.Var(
            initialize=0, 
            bounds=(self.p.hr_mins[0], self.p.hr_mins[-1]), # Convert to MW. Values input in GW
            within=pe.NonNegativeIntegers)

        self.p.m.process_opti_end = pe.Var(
            initialize=0, 
            bounds=(self.p.hr_mins[0], self.p.hr_mins[-1]), # Convert to MW. Values input in GW
            within=pe.NonNegativeIntegers)

        self.setup_constraints()

    def get_unit_name(self):
        return self.unit_name  
    
    def setup_constraints(self):

        # def proc_dependency_rule(model, h_m):
        #     return model.process_duration <= model.carbon_value[h_m]
        # self.p.m.proc_dependency = pe.Constraint(self.p.m.hr_mins, rule=proc_dependency_rule)

        return None