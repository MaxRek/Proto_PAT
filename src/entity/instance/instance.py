from ..df import Df
from .data import Data
import numpy as np
import os
import json
from src.constant import PATH_IN,PATH_INSTANCE, FIELDS_E,SUB_DEMAND

class Instance:
    prod:dict
    data:Data
    name:str

    def __init__(self, df:Df,K :int, F:int, Fs:int, Q : int, O:list, D:list, d:list, ct:np.matrix = np.zeros((1,1)),prod:dict = SUB_DEMAND ) -> None:
        self.prod = prod
        self.data= Data(df,df.N.shape[0], df.E.shape[0], df.F.shape[0], df.T.shape[0],K, F, F-Fs, Fs, Q,O,D,d,ct)

    def load_instance(self):
        if "prod.json" in os.listdir(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/"):
            with(open(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/prod.json",'r')) as f:
                #print(json.load(f))
                temp_prod = json.load(f)
                self.prod = dict(temp_prod)
        self.data.load_data(PATH_IN+"/"+PATH_INSTANCE+"/",self.name)

    def save_instance(self):
        #print(self.prod)
        
        if PATH_INSTANCE not in os.listdir(PATH_IN):
            os.mkdir(PATH_IN+"/"+PATH_INSTANCE)

        if self.name not in os.listdir(PATH_IN+"/"+PATH_INSTANCE):
            os.mkdir(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name)

        with(open(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/prod.json","+w")) as f:
            f.write(json.dumps(self.prod, indent=4))

        self.data.save_data(PATH_IN+"/"+PATH_INSTANCE+"/",self.name)