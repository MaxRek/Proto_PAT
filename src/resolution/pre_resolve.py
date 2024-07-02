from ..entity.instance.instance import Instance
from ..entity.instance.decision import Dec
from .struct.sub_data import Sub_data
from.tools import sub_matrix

import math
import numpy as np

def reduction(inst:Instance):
    indexes_loc = [[],[]]
    sub_tsp = []


    #Récupération des clients ayant passé commande
    indexes_loc[0] = list(inst.data.d.keys())

    for i in range(len(indexes_loc[0])):
        indexes_loc[0][i] = int(indexes_loc[0][i])

    #Récupération des producteurs qui ont au moins une commande
    for i in range(len(indexes_loc[0])):
        for j in inst.data.d[i].keys():
            #print(j)
            if(j not in indexes_loc[1]):
                indexes_loc[1].append(int(j))
                #print(inst.data.d[i][j])
                for f in inst.data.d[i][j]:
                    if f[0] == 0:
                        sub_tsp.append(j)
           # for f in range(len(inst.data.d[i][j])):
    indexes_loc[0] = sorted(indexes_loc[0])
    indexes_loc[1] = sorted(indexes_loc[1])
    # print(indexes_loc)
    # print(sub_tsp)


    #Adaptation de D pour ne récupérer que les clients des producteurs visités
    #D_{p,c}
    sub_D = np.zeros((len(indexes_loc[1]),len(indexes_loc[0])),dtype=int).tolist()
    for i in range(len(indexes_loc[0])):
        for j in range(len(indexes_loc[1])):#print(j)
            if(j in inst.data.d[i].keys()):
                sub_D[j][i] = 1

    #Modif de d pour refléter nouveau indices
    new_d = {}
    for i in inst.data.d.keys():
        i_c = i + inst.data.N
        new_d[i_c] = {}
        for j in inst.data.d[i].keys():
            j_c = inst.data.N+len(indexes_loc[0]) + indexes_loc[1].index(j)
            new_d[i_c][j_c] = []
            for k in inst.data.d[i][j]:
                new_d[i_c][j_c].append(k)
    
    #print(new_d)

    #adaptation de c pour réduire la matrice de coût uniquement à ceux qui nous intéressent
    #c_{i,j} 

    #Rassemblement des indexes
    sum_ind = list(range(inst.data.N))
    for i in indexes_loc[0]:
        sum_ind.append(i+inst.data.N)
    for i in indexes_loc[1]:
        sum_ind.append(i+inst.data.N+inst.data.C)
    
    sum_ind.append(inst.data.N+inst.data.C+inst.data.P)

    #print(str(len(inst.data.c)) + " "+ str(len(inst.data.c[0])))
    sub_c = sub_matrix(inst.data.c, sum_ind)
    #print(str(len(sub_c)) + " "+ str(len(sub_c)))
    

    sdata = Sub_data(inst.data.N,len(indexes_loc[0]),len(indexes_loc[1]),inst.data.F,sub_tsp, inst.data.Q, inst.data.O, sub_D, new_d, sub_c, indexes_loc, inst.data.df)

    # for i in i.data.d.keys():
    #     if 
    #     for j in i:

    return sdata
