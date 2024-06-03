import numpy as np
import openrouteservice
import csv
import os
import requests
import time
import pandas as pd 
from openrouteservice import convert
from ..df import Df
from src.constant import APIKEY_OPENROUTE, PATH_IN, PATH_INSTANCE, PRIX_ESSENCE_100_KM, TARIF_HORAIRE_HT, FIELDS_D
import math
import ast

class Data:
    N:int
    C:int
    P:int
    T:int
    K:int
    F:int
    Fs:int
    Fp:int
    Q:int
    O:list
    D:list
    d:dict
    c:list
    df:Df

    def __init__(self, df:Df, n:int,c:int,p:int,t:int,k:int,f:int,fp:int,fs:int,q:int,o:list,D:list,d:dict,ct:list) -> None:
        # if len(o) != n and len(d) != c and len(d[0]) != f and len(S) != p and len(t) != n and len(t[0]) != fs and fp < fs :
            self.df = df
            self.N = n
            self.C = c
            self.P = p
            self.T = t
            self.K = k
            self.F = f
            self.Fs = fs
            self.Fp = fp
            self.Q = q
            self.O = o
            self.D = D
            self.d = d
            self.c = ct
        # else:
        #     print("Erreur d'initialisation, problème impossible")
        
    def save_data(self, path, name):
        writer = open(path+name+"/data.txt",'w')
        print(self.D)
        writer.write("N:"+str(self.N)+"\n")
        writer.write("C:"+str(self.C)+"\n")
        writer.write("P:"+str(self.P)+"\n")
        writer.write("T:"+str(self.T)+"\n")
        writer.write("K:"+str(self.K)+"\n")
        writer.write("F:"+str(self.F)+"\n")
        writer.write("Fs:"+str(self.Fs)+"\n")
        writer.write("Fp:"+str(self.Fp)+"\n")
        writer.write("Q:"+str(self.Q)+"\n")
        writer.write("O:"+str(self.O)+"\n")
        writer.write("D:"+str(self.D)+"\n")
        writer.write("c:"+str(self.c)+"\n")
        writer.close()
        self.df.save_df(path+name+"/","e","f","n","t")
        self.save_d(name, "d")

    def load_data(self,path,name):
        if "data.txt" in os.listdir(path+"/"+name+"/"):
            read = open(PATH_IN+"/"+PATH_INSTANCE+"/"+name+"/data.txt",'r')
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
                elif "K:" in i:
                    k = i[2:]
                    self.K = int(k)
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
                elif "D:" in i:
                    D = i[2:]
                    self.D = ast.literal_eval(D)
                elif "c:" in i:
                    c = i[2:]
                    self.c = ast.literal_eval(c)
                else:
                    print("Ligne supplémentaire sans indication : "+i)
            self.load_Dd(name,"d",path)
        else:
            print("ERREUR : data.txt absent dans "+PATH_IN+"/"+PATH_INSTANCE+"/"+name+"/")

    def load_Dd(self,name:str, file_d:str, path:str = PATH_IN+"/"+PATH_INSTANCE+"/"):
        if file_d+".csv" in os.listdir(path+name+"/"):
            self.d = {}
            temp_d = pd.read_csv(path+name+"/"+file_d+".csv", sep=";", usecols= FIELDS_D)
            self.D = np.zeros((self.C,self.P),dtype=int).tolist()
            #print("C = "+str(self.C)+", Taille D : "+str(len(self.D))+ " " + str(len(self.D[0])))
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
                        #print(self.D[45][11])
                    self.d[int(r["E"])][int(r["P"])].append((int(r["F"]),r["d"]))
                    self.D[int(r["E"])][int(r["P"])] = 1
            #print(self.D)   
        else:
            print("Pas de fichier \""+file_d+".csv\" dans "+path+"/"+name)

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
    
    def gen_c(self,key=APIKEY_OPENROUTE,rate_per_hour:float=1.0):
        total = self.N+self.C+self.P
        self.c = np.zeros((total,total)).tolist()
        it = math.ceil(total/25)
        nbit = (it-1)+((it-2)*(it-1))/2
        print("Usage d'OpenRouteServices : total du nombre de sommets = "+str(total)+", nombre de demandes = " + str(nbit))
        print("Temps d'attente estimé : "+str(math.floor(nbit/40))+" min minimum")
        temp_coords = []
        test =0
        for i in self.df.get_coords_N().values:
            temp_coords.append((i[0],i[1]))

        for i in self.df.get_coords_E().values:
            temp_coords.append((i[0],i[1]))

        for i in self.df.get_coords_F().values:
            temp_coords.append((i[0],i[1]))

        it = math.ceil(total/25)
        #Besoin d'ajouter un compteur à cause de la limite de temps imposé par OpenRouteService
        lim = 0
        for i in range(0,it-1):
            for j in range(i+1,it):
                test +=1
                coords = []
                i_coords = []
                i_l = i*25
                for l in temp_coords[i*25:min((i+1)*25,total)]:
                    coords.append(l)
                    i_coords.append(i_l)
                    i_l += 1
                i_k = j*25
                for k in temp_coords[j*25:min((j+1)*25,total)]:
                    coords.append(k)
                    i_coords.append(i_k)
                    i_k += 1

                # print(str(i) + " " + str(j))
                # print(range(i*25,min((i+1)*25,total)))
                # print(range(j*25,min((j+1)*25,total)))
                # print(i_coords)
                #Requête auprès de OpenRouteServices, on incrémente notre limite, sinon on attend et réinitialise
                if(lim < 40):
                    lim += 1
                else:
                    print("Limite atteinte, éxécution en pause")
                    time.sleep(60)
                    print("Reprise d'éxécution")
                    lim = 0
                
                temp_durations = request_c(coords,key)
                if type(temp_durations) == list:
                    for m in range(len(temp_durations)):
                        for n in range(len(temp_durations[i])):
                            self.c[i_coords[m]][i_coords[n]] = temp_durations[m][n]
                            self.c[i_coords[n]][i_coords[m]] = temp_durations[m][n]
                else:
                    print("erreur")
                # for m in range(len(i_coords)):
                #     for n in range(m+1,len(i_coords)):
                #         self.c[i_coords[m]][i_coords[n]] = 1
                #         self.c[i_coords[n]][i_coords[m]] = 1

        
        #cas impair, il y a un ensemble de points non reliés qui n'a pas été pris dans les itérations suivantes
        # if it/2 == math.ceil(it/2):
        #     coords = []
        #     i_coords = []
        #     i_l = i*25
        #     for i in temp_coords[math.floor(it/2)*25:min((math.floor(it/2)+1)*25,total)]:
        #         coords.append(i)
        #         i_coords.append(i_l)
        #         i_l += 1
        #         #Requête auprès de OpenRouteServices
        #         # temp_durations = request_c(coords,key)
        #         # for i in range(len(temp_durations)):
        #         #     for j in range(len(temp_durations[i])):
        #         #         self.c[i_coords[i],i_coords[j]] = temp_durations[i][j]
        #         #         self.c[i_coords[j]][i_coords[i]] = temp_durations[j][i]    
        #         for m in range(len(i_coords)):
        #             for n in range(m,len(i_coords)):
        #                 self.c[i_coords[m]][i_coords[n]] = 1
        #                 #self.c[i_coords[n]][i_coords[m]] = 1 
        #     print("Last case : " + str(i_l))
        #     print(range(i_l,min((i_l+25,total))))
        #     print(i_coords)
        
        # print(type(self.c))
        # print(test)

def request_c(coords,key,prix_esssence=PRIX_ESSENCE_100_KM,tarif_horaire=TARIF_HORAIRE_HT):
    r = 0
    try:
        body = {"locations":coords,"metrics":["distance","duration"]}
        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
            'Authorization': key,
            'Content-Type': 'application/json; charset=utf-8'
        }

        call = requests.post('https://api.openrouteservice.org/v2/matrix/driving-car', json=body, headers=headers)
        
        durations = call.json()["durations"]
        distances = call.json()["distances"]
        r = np.zeros((len(durations),len(durations[0]))).tolist()
        for i in range(len(durations)):
            for j in range(len(durations[i])):
                r[i][j]=math.ceil(durations[i][j]/60/60*TARIF_HORAIRE_HT + distances[i][j]/100000*PRIX_ESSENCE_100_KM)

    except:
        print(call.status_code)
        print(call.text)

    return r
        