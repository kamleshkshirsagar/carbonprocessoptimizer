## Base file to run optimization
from optimization.ModelData import ModelData

class Overall_System(ModelData):
    pass

def model():
    system = Overall_System(print_output=True)
    return None

if __name__ == "__main__":
    model()