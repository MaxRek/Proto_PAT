from ..df import Df
from .decision import Dec
from .data import Data
import numpy as np
import os
import json
from src.scripts.demandFiller import demandFiller_Dcpf
from src.scripts.prodFiller import prodFiller

from src.constant import PATH_IN,PATH_INSTANCE, FIELDS_E,SUB_DEMAND
import pandas as pd


class Instance:
    prod:dict
    dec:Dec
    data:Data
    name:str

    def __init__(self, df:Df,K :int, F:int, Fp:int,Fs:int, Q : int, O:list, D:list, d:list, ct:np.matrix = np.zeros((1,1)),prod:dict = SUB_DEMAND ) -> None:
        self.prod = prod
        self.data= Data(df,df.N.shape[0], df.E.shape[0], df.F.shape[0], df.T.shape[0],K, F, F-Fs, Fs, Q,O,D,d,ct)
        self.dec = Dec(self.data.C, self.data.N, self.data.P,self.data.T)

    def load_instance(self):
        if "prod.json" in os.listdir(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/"):
            with(open(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/prod.json",'r')) as f:
                #print(json.load(f))
                temp_prod = json.load(f)
                self.prod = dict(temp_prod)
        self.data.load_data(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name)
        self.dec.load_dec(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/","dec")

    def load_data_prod(self,prod:dict,t:list=[]):
        if "e_demand.csv" not in os.listdir(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/"):
            demandFiller_Dcpf(PATH_IN+"/"+PATH_INSTANCE+"/",self.name+"/e")
        temp_d = pd.read_csv(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/e_demand.csv", sep = ";", na_values="NaN")

        # if "f_prod.csv" not in os.listdir(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/"):
        #     prodFiller(PATH_IN+"/"+PATH_INSTANCE+"/",self.name+"/f",temp_d, prod, self.data.Q, self.data.K)
        # temp_f = pd.read_csv(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/f_prod.csv", sep = ";", na_values="NaN")
        
        self.data.Fp = len(prod["P"])
        self.data.Fs = len(prod["S"])
        self.data.F = self.data.Fp + self.data.Fs

        self.data.D = np.zeros((self.data.C,self.data.P)).tolist()
        self.data.d = []
        for i in range(self.data.C):
            self.data.d.append(np.zeros((self.data.P,self.data.F)).tolist())
        #print(str(len(self.data.d)) + " "+ str(len(self.data.d[0])))
        ind = 0

        if self.data.Fs>0:
            # try:
            for i in range(len(prod["S"])):
                if prod["S"][i] in temp_d.columns and prod["S"][i]+"_S" in temp_f.columns:
                    temp_demand = temp_d[prod["S"][i]]
                    for j in range(self.data.C):
                        #print(str(j) + " " + str(self.data.C))
                        self.data.d[j][ind] = temp_demand[j]
                    ind +=1

            # except:
                # print("Bug dans prod sale")
                # print(self.data.d)
        if len(prod["P"])>0:
            # try:
            for i in prod["P"]:
                if i in temp_d.columns and i in temp_f.columns:
                    temp_demand = temp_d[i]
                    temp_prod = temp_f[i]
                    for j in range(self.data.C):
                        self.data.d[j][ind] = temp_demand[j]
                    ind += 1
            # except:
            #     print("Bug dans prod propre")
            #     print(self.data.d)

    def save_instance(self):
        #print(self.prod)
        
        if PATH_INSTANCE not in os.listdir(PATH_IN):
            os.mkdir(PATH_IN+"/"+PATH_INSTANCE)

        if self.name not in os.listdir(PATH_IN+"/"+PATH_INSTANCE):
            os.mkdir(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name)

        with(open(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/prod.json","+w")) as f:
            f.write(json.dumps(self.prod, indent=4))


        self.data.save_data(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/","data")
        self.dec.save_dec(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/","dec")

        
