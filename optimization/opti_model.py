## Base file to run optimization
from optimization.ModelData import ModelData, parse_json
from optimization.Process import Process

class Overall_Process(ModelData):
    def __init__(self, print_output=False, *args, **kwargs):
        print('Setting up Overall System')
        super().__init__(*args, **kwargs)
        self.num_units = []
        self.print_output=print_output

    def add_unit(self, unit_name=None, unit_info=None):
        if 'start_time' in unit_info and 'end_time' in unit_info:
            unit_process = Process(self, unit_name, unit_info)
        else:
            print('Please enter a valid input process')
            return None

        self.num_units.append(unit_process)
        print('Added process ',unit_process.get_unit_name())
        return None


def opti_model():
    overall_process = Overall_Process(print_output=True)

    proc_info = parse_json(file_path="./optimization/process_details.json")

    for proc in proc_info:
        overall_process.add_unit(unit_name=proc, unit_info=proc_info[proc])
    return None

if __name__ == "__main__":
    opti_model()