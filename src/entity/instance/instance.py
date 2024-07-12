from ..df import Df
from .data import Data
import pandas as pd
import numpy as np
import os
import json
from copy import deepcopy
from src.constant import COMMUNES,PATH_IN,PATH_INSTANCE, SUB_DEMAND, A_NAME_CSV, NAME_CSV_D, NAME_DATA, FIELDS_F_NG, FIELDS_E_NG

class Instance:
    prod:dict
    data:Data
    name:str

    def __init__(self, name:str ,prod:dict = SUB_DEMAND) -> None:
        self.name = name
        self.data = Data()
        self.prod = prod

    def init_data(self,df:Df, F:int, Fs:int, Q : int, O:list, D:list, d:list, ct:np.matrix = np.zeros((1,1))):
        self.data = Data(df,df.N.shape[0], df.E.shape[0], df.F.shape[0], df.T.shape[0], F, F-Fs, Fs, Q,O,D,d,ct)

    def load_instance(self, path = PATH_IN+"/"+PATH_INSTANCE+"/"):
        if "prod.json" in os.listdir(path+"/"+self.name+"/"):
            with(open(path+"/"+self.name+"/prod.json",'r')) as f:
                #print(json.load(f))
                self.prod = dict(json.load(f))
        self.data.load_data(self.name,path+"/")
        

    def save_instance(self):
        #print(self.prod)
        
        if PATH_INSTANCE not in os.listdir(PATH_IN):
            os.mkdir(PATH_IN+"/"+PATH_INSTANCE)

        if self.name not in os.listdir(PATH_IN+"/"+PATH_INSTANCE):
            os.mkdir(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name)

        with(open(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/prod.json","+w")) as f:
            f.write(json.dumps(self.prod, indent=4))

        self.data.save_data(PATH_IN+"/"+PATH_INSTANCE+"/",self.name)

    def check_tableurs(self):
        functions = [self.data.df.load_csv_E,self.data.df.load_csv_F,self.data.df.load_csv_N,self.data.df.load_csv_T]

        path = PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/"
        files_names = os.listdir(path)
        flags = []
        sub_flags = []
        str_error = ""
        
        for t in A_NAME_CSV:
            if t+".csv" in files_names:
                sub_flags.append(True)
            else:
                sub_flags.append(False)
            
        flags.append(sub_flags)
        sub_flags0 = []
        sub_flags1 = []
        
        for i in range(4):
            if flags[0][i]:
                code = functions[i](path, A_NAME_CSV[i])
                sub_flags1.append(code)
                if code < 2:
                    sub_flags0.append(True)
                else:
                    sub_flags0.append(False)
            else:
                sub_flags1.append(-1)
                sub_flags0.append(False)


        flags.append(sub_flags0)
        flags.append(sub_flags1)

        if NAME_CSV_D+".csv" in files_names:
            flags.append(True)
        else:
            flags.append(False)


        if flags[0][0] and flags[0][1] and flags[-1]:
            f, str_error = self.check_d(path) 
            flags.append(f)

        print(flags)

        return flags, str_error

    def check_d(self,path:str):
        temp_F = pd.read_csv(path+"/"+A_NAME_CSV[1]+".csv", sep = ";", na_values="NaN", usecols=FIELDS_F_NG)
        temp_E = pd.read_csv(path+"/"+A_NAME_CSV[0]+".csv", sep = ";", na_values="NaN", usecols=FIELDS_E_NG)
        F = deepcopy(temp_F.loc[temp_F["Commune"].isin(COMMUNES)])
        E = deepcopy(temp_E.loc[temp_E["Commune"].isin(COMMUNES)])

        Pi = F.shape[0]
        Ei = E.shape[0]
        flag = True
        str_error = ""
        try:
            d = pd.read_csv(path+NAME_CSV_D+".csv", delimiter= ";",usecols=['E','P','F','d'])
        except pd.errors.EmptyDataError :
            print("Le tableur "+str(path+NAME_CSV_D+".csv")+" est vide (ni colonnes)")
            flag = False
                #print(d)
        if flag:
            len_prod = len(list(self.prod.keys()))
           
            for row in d.iterrows():
                row_data = row[1]
                #print(row_data)
                if row_data['E'] >=Ei or row_data['E'] < 0 or row_data['P'] >=Pi or row_data['E'] < 0 or row_data['F'] >= len_prod or row_data['F'] < 0:
                    if flag:
                        str_error = "Erreur dans la programmation des commandes : \n"
                    flag = False
                    str_error = "Ligne "+str(row[0])+" : "
                    if row_data['E'] not in range(0,Ei):
                        str_error += "Etablissement index "+str(row_data['E'])+" non compris entre 0 et "+str(Ei)+" ;"
                    if row_data['P'] not in range(0,Pi):
                        str_error += "Producteur index "+str(row_data['P'])+" non compris entre 0 et "+str(Pi)+" ;"
                    if row_data['F'] not in range(0, len_prod):
                        str_error += "Filiere index "+str(row_data['F'])+" non compris entre 0 et "+str(len_prod)+" ;"
                    str_error += "\n"
        return flag, str_error
    
    def check_data(self):
        path = PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/"+NAME_DATA
        print(os.listdir(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/"))
        
        if NAME_DATA not in os.listdir(PATH_IN+"/"+PATH_INSTANCE+"/"+self.name+"/"):
            open(path, 'w').close()
    
        read = open(path,'r')
        lines = read.readlines()
        read.close()
        data_to_find = ["N","C","P","T","F","Fs","Fp","Q","O","c"]
        for line in lines:
            for d in data_to_find:
                if d in line[0:len(d)]:
                    data_to_find.remove(d)


        return data_to_find

