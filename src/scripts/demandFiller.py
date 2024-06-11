import pandas as pd
import numpy as np
import math
import copy
import json
import os
import random
from src.constant import COUT_METRE_CARRE,NB_METRE_CARRE,ECART_PRIX_PLAT,RATIO_AMORTISSEMENT,SUB_DEMAND,COMMUNES,DOMAINES,SUB_FIELDS_E,FIELDS_F,FIELDS_D

def rowDemandFiller(nbrp : int, quantities : list[int]) -> np.array:
    return nbrp*np.array(quantities)/100

def demandFiller_Dcf(path : str, file : str, prod = SUB_DEMAND,mult:float=1.0):
    datAll = pd.read_csv(path+file+".csv", sep = ";",na_values="NaN")

    #Nettoyage des données, concentration sur les Communes du PAT
    data = datAll.loc[datAll["Commune"].isin(COMMUNES)]
    data = data.dropna(axis=0, subset=["Nombre de repas par jour"])

    #Correction de la colonne du nombre des repas, car possible présence d'espace
    newColumn = []
    for row in data.iterrows():
        if type(row[1]["Nombre de repas par jour"]) == str:
            value = ""
            for c in row[1]["Nombre de repas par jour"]:
                if(c in ["0","1","2","3","4","5","6","7","8","9"]):
                    value += c
            newColumn.append(int(value))
        else:
            newColumn.append(row[1]["Nombre de repas par jour"])
    data["Nombre de repas par jour"] = newColumn
    
    with(open("in/data/demandFillerRatio.json",'r+')) as f:
        ratios = json.load(f)

    with(open("in/data/demandFiller.json",'r+')) as f:
        demandQuantity = json.load(f)

    quantitiesNames = []
    quantities = []

    if prod != {}:
        for key in prod:
            if type(prod[key]) == list:
                if len(prod[key]) > 0:
                    if key in demandQuantity.keys():
                        keyTotal = 0
                        for value in prod[key]:
                            if value in demandQuantity[key].keys():
                                quantitiesNames.append(value)
                                if value in ratios.keys():
                                    subQuantity = demandQuantity[key][value]*ratios[value]
                                    keyTotal += subQuantity
                                    quantities.append(subQuantity)
                                else:
                                    keyTotal += demandQuantity[key][value]
                                    quantities.append(demandQuantity[key][value])
                                demandQuantity[key].pop(value)
                            else:
                                print("Erreur : Value dans prod \""+value+"\" avec aucune quantité affectée.")
                        quantitiesNames.append(key)
                        quantities.append(keyTotal)
                    else:
                        print("Erreur : Key dans prod \""+key+"\" n'est pas référencé dans les quantités.")
                else:
                    print("Erreur : Key dans prod \""+key+"\" avec valeur vide")
            else:
                print("Erreur : mauvais typage pour la valeur de key \""+key+"\" dans prod")
    else:
        print("Erreur : Key dans prod \""+key+"\" n'est pas référencé dans les quantités.")

    demand = data[SUB_FIELDS_E].loc[(data["Domaine"].isin(DOMAINES)) &(
        (data["Type de restauration"] == "Production et consommation sur place") |
        (data["Type de restauration"] == "Production pour consommation sur place et livraisons à des restaurants satellites")|
        (data["Type de restauration"] == "Production pour livraisons à des restaurants satellites"))
        & (data["Nombre de repas par jour"] > 0)]

    quantitySeries = demand.apply(lambda x : rowDemandFiller(x["Nombre de repas par jour"], quantities),axis=1)
    #quantityFrame = demand.apply(lambda x : rowDemandFiller(x["Nombre de repas par jour"], quantities),axis=1)
    demand[quantitiesNames] = 0
    values = quantitySeries.values*mult/36

    pos_SUB_DEMAND_key = []
    ind = 0
    for i in prod.keys():
        ind += len(prod[i])
        pos_SUB_DEMAND_key.append(ind)
        ind +=1

    for i in range(len(values)):
        sum_val = 0
        for j in range(len(values[i])):
            if j in pos_SUB_DEMAND_key:
                values[i][j] = sum_val
                sum_val = 0
            else:
                values[i][j] = math.ceil(values[i][j])
                sum_val += values[i][j]

    for i in range((demand.shape[0])):
        for j in range(len(values[i])):
            demand.iloc[i,j+len(SUB_FIELDS_E)] = values[i][j]

    nameFile = file + "_demand"
    if nameFile+".csv" in os.listdir(path):
        os.remove(path+nameFile+".csv")
    demand.to_csv(path+nameFile+".csv", sep=";")


def demandFiller_Dcpf(path : str, file_e : str, file_p : str, file_d : str,mult:float=1, prod = SUB_DEMAND, D :list = [], multi_f = 0, ratio_p = [], ratio_pc = []):
    datAll = pd.read_csv(path+file_e+".csv", sep = ";",na_values="NaN")

    #Nettoyage des données, concentration sur les Communes du PAT
    data_e = datAll.loc[datAll["Commune"].isin(COMMUNES)]
    data_e = data_e.dropna(axis=0, subset=["Nombre de repas par jour"])

    #Correction de la colonne du nombre des repas, car possible présence d'espace
    newColumn = []
    for row in data_e.iterrows():
        if type(row[1]["Nombre de repas par jour"]) == str:
            value = ""
            for c in row[1]["Nombre de repas par jour"]:
                if(c in ["0","1","2","3","4","5","6","7","8","9"]):
                    value += c
            newColumn.append(int(value))
        else:
            newColumn.append(row[1]["Nombre de repas par jour"])
    data_e["Nombre de repas par jour"] = newColumn
    
    with(open("in/data/demandFillerRatio.json",'r+')) as f:
        ratios = json.load(f)

    with(open("in/data/demandFiller.json",'r+')) as f:
        demandQuantity = json.load(f)

    quantitiesNames = []
    quantities = []

    if prod != {}:
        for key in prod:
            if type(prod[key]) == list:
                if len(prod[key]) > 0:
                    if key in demandQuantity.keys():
                        keyTotal = 0
                        for value in prod[key]:
                            if value in demandQuantity[key].keys():
                                quantitiesNames.append(value)
                                if value in ratios.keys():
                                    subQuantity = demandQuantity[key][value]*ratios[value]
                                    keyTotal += subQuantity
                                    quantities.append(subQuantity)
                                else:
                                    keyTotal += demandQuantity[key][value]
                                    quantities.append(demandQuantity[key][value])
                                    demandQuantity[key].pop(value)
                            else:
                                print("Erreur : Value dans prod \""+value+"\" avec aucune quantité affectée.")
                        quantitiesNames.append(key)
                        quantities.append(keyTotal)
                    else:
                        print("Erreur : Key dans prod \""+key+"\" n'est pas référencé dans les quantités.")
                else:
                    print("Erreur : Key dans prod \""+key+"\" avec valeur vide")
            else:
                print("Erreur : mauvais typage pour la valeur de key \""+key+"\" dans prod")
    else:
        print("Erreur : Key dans prod \""+key+"\" n'est pas référencé dans les quantités.")

    demand = data_e[SUB_FIELDS_E].loc[(data_e["Domaine"].isin(DOMAINES)) &(
        (data_e["Type de restauration"] == "Production et consommation sur place") |
        (data_e["Type de restauration"] == "Production pour consommation sur place et livraisons à des restaurants satellites")|
        (data_e["Type de restauration"] == "Production pour livraisons à des restaurants satellites"))
        & (data_e["Nombre de repas par jour"] > 0)]

    quantitySeries = demand.apply(lambda x : rowDemandFiller(x["Nombre de repas par jour"], quantities),axis=1)
    #quantityFrame = demand.apply(lambda x : rowDemandFiller(x["Nombre de repas par jour"], quantities),axis=1)
    demand[quantitiesNames] = 0

    #Usage de mult pour donner l'échelle
    values = []
    for i in range(len(quantitySeries.values)):
        values.append(quantitySeries.values[i])
        for j in range(len(values[i])):
            values[i][j] = values[i][j]*mult


    pos_SUB_DEMAND_key = []
    ind = 0
    for i in prod.keys():
        ind += len(prod[i])
        pos_SUB_DEMAND_key.append(ind)
        ind +=1
    #print(pos_SUB_DEMAND_key)

    for i in range(len(values)):
        sum_val = 0
        for j in range(len(values[i])):
            if j in pos_SUB_DEMAND_key:
                values[i][j] = sum_val
                sum_val = 0
            else:
                values[i][j] = math.ceil(values[i][j])
                sum_val += values[i][j]

    for i in range((demand.shape[0])):
        for j in range(len(values[i])):
            demand.iloc[i,j+len(SUB_FIELDS_E)] = values[i][j]

    nameFile = file_e + "_demand"
    if nameFile+".csv" in os.listdir(path):
        os.remove(path+nameFile+".csv")
    demand.to_csv(path+nameFile+".csv", sep=";")

    #______________________________________________________
    #Affectation des commandes
    #______________________________________________________
    for i in range(len(pos_SUB_DEMAND_key)):
        pos_SUB_DEMAND_key[i] += len(SUB_FIELDS_E)

    F = demand.iloc[:,pos_SUB_DEMAND_key]
    #print(demand.columns)
    #print(F)
    
    data_p = pd.read_csv(path+file_p+".csv", sep = ";",na_values="NaN")
    
    #Affectation alétoire aux filières
    if "Filieres" not in data_p.columns:
        data_p = data_p[FIELDS_F]
        if D == []:
            if(len(ratio_p) != len(pos_SUB_DEMAND_key)):
                print("ratio_p n'est pas représentatif des filières à traiter (len(ratio_p) = "+str(len(ratio_p))+" , len(demand_key) = "+str(len(pos_SUB_DEMAND_key))+"), séparation égale pour chaque filière")
                r = 1/len(pos_SUB_DEMAND_key)
                ratio_p = np.ones(len(pos_SUB_DEMAND_key)).tolist()
                for i in range(len(ratio_p)):
                    ratio_p[i] = ratio_p[i]*r

        #print(ratio_p)
        affect = []
        ind_f_p = []
        for i in range(len(prod.keys())):
            ind_f_p.append([])
        k = 0
        for row in data_p.iterrows():
            stop = False
            temp_l = list(range(len(pos_SUB_DEMAND_key)))
            temp_r = copy.copy(ratio_p)
            temp_f = []
            ind_f = []
            while not stop:
                if temp_l != []:
                    i, pre_sum_r = randinlist(temp_l,temp_r)
                    # print("i = "+ str(i))
                    # print("pré sum_r = "+str(pre_sum_r))

                    temp_f.append(F.columns[temp_l[i]])
                    ind_f.append(temp_l[i])
                    temp_l.pop(i)
                    post_sum_r = pre_sum_r - temp_r[i]
                    # print("post sum_r = "+str(post_sum_r))

                    temp_r.pop(i)
                    for j in range(len(temp_r)):
                        temp_r[j] = temp_r[j]*(pre_sum_r/post_sum_r)
                else:
                    stop = True
                if random.random() > multi_f :
                    stop = True
            affect.append(str(temp_f))
            # print(temp_f)
            # print(ind_f)
            # print(j)
            for i in ind_f:
                ind_f_p[i].append(k)
            k += 1
            
        data_p["Filieres"] = affect
        # print(data_p["Filieres"])
        data_p.to_csv(path+file_p+"_prod.csv", sep = ";")
    else:
        data_p = data_p[copy.copy(FIELDS_F).append("Filieres")]
        ind_f_p = []
        for i in range(len(prod.keys())):
            ind_f_p.append([])

        for i in range(data_p.shape[0]):
            j = 0
        
            for key in prod.keys():
                #sum_ind_p_f.append[[]]
                if key in data_p.iloc[i]["Filieres"]:
                    # print(key)
                    # print(data_p.loc[i]["Filieres"])
                    ind_f_p[j].append(i)
                j += 1

    #Génération des commandes

    # if file_d+".csv" not in os.listdir(path):
    # pd.read_csv(path+file_d+".csv",sep=";",usecols=FIELDS_D)
    #     pd.DataFrame([], columns=FIELDS_D).to_csv(path+file_d+".csv",sep=";")
    d = pd.DataFrame([], columns=FIELDS_D).to_csv(path+file_d+".csv",sep=";")

    if ratio_pc == []:
        print("ratio_pc non spécifié, le client se fournit chez un producteur par filière")
        ratio_pc = np.ones(len(pos_SUB_DEMAND_key),dtype=int).tolist()
    #print(ind_f_p)

    # print(values)
    # print(demand["Legumes"])

    #Pour chaque etablissement
    for e in range(demand.shape[0]):
        temp_ratio_pc = np.zeros(len(pos_SUB_DEMAND_key),dtype=int).tolist()
        while(temp_ratio_pc != ratio_pc):
        #On choisit une filière de produit
            
            f = randinlist(ratio_pc)
            f = f[0]
            #print("ratio_pc = "+str(ratio_pc)+" ,f = "+str(f))
            temp_d = []
            temp_f = []
            temp_p = []

            #verifier si il y a une demande pour le produit, et que la demande n'est pas déjà remplie
            if demand.iloc[e][list(prod.keys())[f]] > 0 and temp_ratio_pc[f] < ratio_pc[f]:
                #Ajoutez autant de prod que nécéssaire, coupez la commande en nombre de prods
                #Relancez si prod déjà pris
                while temp_ratio_pc[f] < ratio_pc[f]:
                    #print(ind_f_p[f])
                    
                    k = randinlist(ind_f_p[f])[0]
                    #print(k)
                    if k not in temp_p :
                        temp_p.append(ind_f_p[f][k])
                        temp_ratio_pc[f] += 1
                        temp_f.append(f)
                        temp_d.append(demand.iloc[e][list(prod.keys())[f]]/ratio_pc[f])
                        #print(temp_d)
                        #On vérifie si le prod ne produit pas d'autres filières, si oui on associe directement s'il ya une place à remplir
                        for j in range(len(ratio_pc)):
                            if j != f:
                                if(k in ind_f_p[j]) and temp_ratio_pc[j] < ratio_pc[j]:
                                    #print(ind_f_p[j])
                                    temp_p.append(ind_f_p[f][k])
                                    temp_ratio_pc[j] += 1
                                    temp_f.append(j)
                                    temp_d.append(demand.iloc[e][list(prod.keys())[j]]/ratio_pc[j])
                for i in range(len(temp_p)):
                    # print("_________________")
                    # print(data_p.loc[temp_p[i]])
                    # print("_________________")  
                    # print(list(prod.keys())[f])
                    # print("_________________")
                    # print(temp_f[i])

                    values_ind = [e,temp_p[i],temp_f[i],temp_d[i]]
                    r_ind = pd.DataFrame([values_ind] ,columns = ["E","P","F","d"])
                    # values = [data_e.loc[e]["Nom de la structure"],data_p.loc[temp_p[i]]["Nom"],list(prod.keys())[f],temp_f[i]]

                    # r = pd.DataFrame([values] ,columns = ["E","P","F","d"])
                    d = pd.concat([d,r_ind], ignore_index=True)
                
                # d = pd.concat([r,d], ignore_index=True)

    #print(d["d"].loc[d["F"] == 0])

    #print(demand.iloc[e])
    d.to_csv(path+file_d+".csv",sep=";")

def randinlist( l : list, ratio :list = []):
    if ratio == []:
        i = round(random.random()*(len(l)-1))
        sum_r = 1
    elif len(l) == 1:
        i = 0
        sum_r = 1
    else:
        r = random.random()
        stop = False
        i = 0
        sum_r = 0
        # print("l = " + str(l))
        # print("ratio = " + str(ratio))
        # print("r = " +str(r))
        j = 0

        while j < len(l):
            sum_r += ratio[j]
            if sum_r < r:
                if not stop:
                    i+=1
            else:
                stop = True
            j += 1

    return i, sum_r

def gen_O(N:int,prix_mc:float = COUT_METRE_CARRE,surface:int = NB_METRE_CARRE,ecart:float = ECART_PRIX_PLAT, ratio:float = RATIO_AMORTISSEMENT):
    r = np.zeros(N).tolist()
    for i in range(N):
        r[i] = round((surface * ((prix_mc*(1-ecart))+prix_mc*ecart*random.random()*2))*ratio)

    #print(r)
    return r