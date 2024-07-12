import os
import pandas as pd 
from ..df import Df
from src.constant import PATH_IN, PATH_INSTANCE, FIELDS_D, NAME_CSV_E, NAME_CSV_F, NAME_CSV_N, NAME_CSV_T
import ast

class Data:
    N:int
    C:int
    P:int
    T:int
    F:int
    Fs:int
    Fp:int
    Q:int
    O:list
    d:dict
    c:list
    time:list
    df:Df

    def __init__(self) -> None:
        # if len(o) != n and len(d) != c and len(d[0]) != f and len(S) != p and len(t) != n and len(t[0]) != fs and fp < fs :
            self.df = Df()
            self.N = 0
            self.C = 0
            self.P = 0
            self.T = 0
            self.F = 0
            self.Fs = 0
            self.Fp = 0
            self.Q = 0
            self.O = []
            self.d = {}
            self.c = []
            self.time = []
        # else:
        #     print("Erreur d'initialisation, problème impossible")
        
    def set_all_data(self, df:Df, n:int,c:int,p:int,t:int,f:int,fp:int,fs:int,q:int,o:list,D:list,d:dict,ct:list, time:list):
        self.N = n
        self.C = c
        self.P = p
        self.T = t
        self.F = f
        self.Fs = fs
        self.Fp = fp
        self.Q = q
        self.O = o
        self.d = d
        self.c = ct
        self.df = df
        self.time = time


    def save_data(self, path, name):
        writer = open(path+name+"/data.txt",'w')
        if self.N > 0 :
            writer.write("N:"+str(self.N)+"\n")
        if self.C > 0 :
            writer.write("C:"+str(self.C)+"\n")
        if self.P > 0 :
            writer.write("P:"+str(self.P)+"\n")
        if self.T > 0 :
            writer.write("T:"+str(self.T)+"\n")
        if self.F > 0 :
            writer.write("F:"+str(self.F)+"\n")
        if self.Fs > 0 :
            writer.write("Fs:"+str(self.Fs)+"\n")
        if self.Fp > 0 :
            writer.write("Fp:"+str(self.Fp)+"\n")
        if self.Q > 0 :
            writer.write("Q:"+str(self.Q)+"\n")
        if self.O != [] :
            writer.write("O:"+str(self.O)+"\n")
        if self.c != [] :
            writer.write("c:"+str(self.c)+"\n")
        if self.time != [] :
            writer.write("time:"+str(self.time)+"\n")
        writer.close()
        #self.df.save_df(path+name+"/","e","f","n","t")
        #self.save_d(name, "d")

    def load_data(self,name,path = PATH_IN+"/"+PATH_INSTANCE):
        self.load_data_txt(name,path)
        self.load_d("d",path+"/"+name)
        self.df.load_csv(path+"/"+name, e_name= NAME_CSV_E, f_name= NAME_CSV_F, n_name=NAME_CSV_N,t_name=NAME_CSV_T)

    def load_data_txt(self,name,path = PATH_IN+"/"+PATH_INSTANCE):
        if "data.txt" in os.listdir(path+"/"+name+"/"):
            read = open(path+"/"+name+"/data.txt",'r')
            lines = read.readlines()
            read.close()
            for i in lines:
                if "N:" in i:
                    n = i[2:]
                    self.N = int(n)
                elif "C:" in i:
                    c = i[2:]
                    self.C = int(c)
                elif "P:" in i:
                    p = i[2:]
                    self.P = int(p)
                elif "T:" in i:
                    t = i[2:]
                    self.T = int(t)
                elif "F:" in i:
                    f = i[2:]
                    self.F = int(f)
                elif "Fs:" in i:
                    fs = i[3:]
                    self.Fs = int(fs)
                elif "Fp:" in i:
                    fp = i[3:]
                    self.Fp = int(fp)
                elif "Q:" in i:
                    q = i[2:]
                    self.Q = int(q)
                elif "O:" in i:
                    o = i[2:]
                    self.O = ast.literal_eval(o)
                elif "d:" in i:
                    d = i[2:]
                    self.d = ast.literal_eval(d)
                elif "c:" in i:
                    c = i[2:]
                    self.c = ast.literal_eval(c)
                elif "time:" in i:
                    t = i[5:]
                    self.t = ast.literal_eval(t)
                else:
                    print("Ligne supplémentaire sans indication : "+i)
        else:
            print("ERREUR : data.txt absent dans "+PATH_IN+"/"+PATH_INSTANCE+"/"+name+"/")
    def load_d(self, file_d:str, path:str = PATH_IN+"/"+PATH_INSTANCE+"/"):
        if file_d+".csv" in os.listdir(path+"/"):
            self.d = {}
            temp_d = pd.read_csv(path+"/"+file_d+".csv", sep=";", usecols= FIELDS_D)
            # print("C = "+str(self.C))
            # print(str(self.C) + " " + str(self.P))
            # print(str(temp_d.shape[0]) + " " + str(temp_d.shape[1]))
            if temp_d.shape[0] > 0:
                for row in temp_d.iterrows():
                    r = row[1]
                    # print(self.d.keys())
                    if r["E"] not in self.d.keys():
                        self.d[r["E"]] = {}
                    if r["P"] not in self.d[r["E"]].keys():
                        self.d[r["E"]][r["P"]] = []
                        #print("r[E] = "+ str(r["E"]), ", r[P] = "+ str(r["P"]))
                    self.d[int(r["E"])][int(r["P"])].append((int(r["F"]),r["d"]))
        else:
            print("Pas de fichier \""+file_d+".csv\" dans "+path+"/")

    def save_d(self,name:str, file_d:str, path:str = PATH_IN+"/"+PATH_INSTANCE+"/"):
        # if file_d+".csv" in os.listdir(path+name+"/"):
        #     os.remove(path+name+"/"+file_d+".csv")
        temp_d = pd.DataFrame([],columns=["E","P","F","d"])
        #print(self.d)
        for key in self.d.keys():
            for key2 in self.d[key].keys():
                for values in self.d[key][key2]:
                    #print(values)
                    temp = [int(key), int(key2), int(values[0]), values[1]]
                    r = pd.DataFrame([temp],columns=["E","P","F","d"])
                    temp_d = pd.concat([temp_d,r])

        temp_d.to_csv(path+name+"/"+file_d+".csv",sep = ";")

    def print_d(self):
        for key in self.d.keys():
            print("client : "+str(key)+" avec commandes : ")
            for key2 in self.d[key].keys():
                string = ""
                for value in self.d[key][key2]:
                    string += "(Filière n"+str(value[0])+", qté = "+str(value[1])+")"
                print("   Fournisseur n"+str(key2)+" filières : "+string )
        