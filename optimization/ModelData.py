from abc import ABC
import os
import pyomo.environ as pe
import pandas as pd

class ModelData(ABC):
    def __init__(self, data=None, df_table=pd.DataFrame()):
        self.m = pe.ConcreteModel()
        self.data = None
        
        self.m.hr_mins = pe.Set(initialize=self.hr_mins)