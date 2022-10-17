from abc import ABC
import os
import pyomo.environ as pe
import pandas as pd
import json

def parse_json(file_path=None):
    with open(file_path, 'r') as fp:
        model_json = json.load(fp)
    return model_json

class ModelData(ABC):
    def __init__(self):
        self.m = pe.ConcreteModel()
        carbon_data = parse_json(file_path='./optimization/test_data.json')
        self.c_df = pd.read_json(carbon_data)
        self.hr_mins = self.c_df.index.to_list()
        self.m.hr_mins = pe.Set(initialize=self.hr_mins)
        self.m.carbon_value = self.c_df['value'].to_dict()
        self.resolution = self.c_df['duration'][0]

if __name__ == "__main__":
    pass