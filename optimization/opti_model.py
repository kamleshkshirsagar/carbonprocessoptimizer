## Base file to run optimization
from optimization.ModelData import ModelData, parse_json
from optimization.Process import Process
import pyomo.environ as pe

class Overall_Process(ModelData):
    def __init__(self, print_output=False, *args, **kwargs):
        print('Setting up Overall System')
        super().__init__(*args, **kwargs)
        self.num_units = []
        self.print_output=print_output

    def get_unit_names_list(self):
        unit_names_list = []
        for unit in self.num_units:
            unit_names_list.append(unit.get_unit_name())
        return unit_names_list

    def add_unit(self, unit_name=None, unit_info=None):
        if 'start_time' in unit_info and 'end_time' in unit_info:
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

        def get_total_c_credits(model, y):
            c_credits = 0
            for unit in self.num_units:
                c_credits = +model.process_c_credits
            return c_credits
        self.m.total_c_credits = pe.Expression(rule=get_total_c_credits)

        return None

    def define_objective_function(self, obj_func='minimize_total_c_credits'):
        self.set_overall_system_c_credits()

        if obj_func=='minimize_total_c_credits':
            def objective_minimize_total_c_credits(model):
                return model.total_c_credits 
            self.m.obj = pe.Objective(rule=objective_minimize_total_c_credits, sense=pe.minimize)

    def print_output_func(self):
        print('Start index= {}'.format(round(pe.value(self.m.process_opti_start),3)))

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

def opti_model():
    overall_process = Overall_Process(print_output=True)

    proc_info = parse_json(file_path="./optimization/process_details.json")

    for proc in proc_info:
        overall_process.add_unit(unit_name=proc, unit_info=proc_info[proc])

    overall_process.set_overall_system_constraints()

    overall_process.define_objective_function()

    overall_process.solve()




if __name__ == "__main__":
    opti_model()