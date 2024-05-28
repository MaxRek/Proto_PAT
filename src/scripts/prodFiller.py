import pandas as pd
import numpy as np
import random
import math
import os

def randInList(p:float, l:list):
    return()

#Si non spécifié, on assume que les producteurs peuvent répondre à environ 2 fois la demande
def prodFiller(path : str, file_p : str, df_d : pd, prod:dict, Q:int, K:int, ratio_sum_all :float = 2, var:float = 0.3,ratio_type_p : list = []):
    sum_p = len(prod["S"])+len(prod["P"])
    columns_name = []
    #Si on ne spécifie pas la répartition des producteurs/fillières, on assume qu'il y a autant de chances que les producteurs 
    if ratio_type_p == []:
        ratio_type_p = np.ones(sum_p)
        for i in range(sum_p):
            ratio_type_p[i] = (1/sum_p)*(i+1)
        ratio_type_p = ratio_type_p.tolist()
    print(ratio_type_p)
    print(df_d)
    dataP = pd.read_csv(path+file_p+".csv",sep = ";",na_values="NaN")
    sum_prod_per_E = np.zeros(sum_p)
    P = len(dataP)
    ind = 0
    for i in prod["S"]:
        if i in df_d.columns:
            sum_prod_per_E[ind] = df_d[i].sum()
            columns_name.append(str(i)+"_S")
            ind += 1

    for i in prod["P"]:
        if i in df_d.columns:
            sum_prod_per_E[ind] = df_d[i].sum()
            columns_name.append(i)
            ind += 1
        dataP.loc[:,i] = pd.Series(np.zeros(P))

    gen = False
    while not gen:
        gen = True
        #On détermine les produits que peuvent fournir un producteur, puis on leur affecte ensuite une quantité. Un prod fourni impérativement au moins un type de produit 
        count_prod_per_F = np.zeros(sum_p).tolist()
        prod_per_F = np.zeros((P,sum_p)).tolist()
        for i in range(P):   
            print(prod)
            stop1 = False
            while not stop1:
                j=0
                prod = random.random() 
                stop2 = False
                while not stop2 and j < sum_p:
                    if(prod < ratio_type_p[j]):
                        stop2 = True
                    else:
                        j+=1
                if prod_per_F[i][j] != 1:
                    prod_per_F[i][j] = 1
                    count_prod_per_F[j] += 1
                else:
                    stop1=True
        
        moy_p = sum_prod_per_E/count_prod_per_F*2
        sum_prod_per_F = np.zeros(sum_p).tolist()
        
        print(dataP.columns)
        gen_p = np.zeros((P,sum_p))
        for i in range(P):
            for j in range(sum_p):
                gen_p[i][j] = round(prod_per_F[i][j]*((1-var)*moy_p[j] + random.random()*var*moy_p[j]*2))
                sum_prod_per_F[j] += gen_p[i][j]
        #Les producteurs étant assignés à un type de produit, nous pouvons assigner 
        print(Q)        
        print(sum_prod_per_E)
        print(sum_prod_per_F)
        for i in range(sum_p):
            if not gen: 
                if sum_prod_per_F[i]>= sum_prod_per_E[i]:
                    # if math.ceil(sum_prod_per_F[i]/Q) < math.ceil(sum_prod_per_E[i]/Q):
                    #     gen = False
                    # else:
                    print("Generation réussie")
                else:
                    gen = False
                    
    for i in range(len(columns_name)):
        print(gen_p[i])
        dataP.loc[:,columns_name[i]] = pd.Series(gen_p[:,i])

    print(dataP[columns_name])

    nameFile = file_p + "_prod"
    if nameFile+".csv" in os.listdir(path):
        os.remove(path+nameFile+".csv")
    dataP.to_csv(path+nameFile+".csv", sep=";")
