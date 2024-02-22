import pandas as pd
import numpy as np

def load_csv(path: str, file:str):
    data = pd.read_csv(path+file, sep = ";", na_values="NaN")
    return data