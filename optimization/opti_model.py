## Base file to run optimization
from optimization.ModelData import ModelData

class Overall_System(ModelData):
    def __init__(self, print_output=False, *args, **kwargs):
        print('Setting up Overall System')
        super().__init__(*args, **kwargs)
        self.print_output=print_output

def opti_model():
    system = Overall_System(print_output=True)
    return None

if __name__ == "__main__":
    opti_model()