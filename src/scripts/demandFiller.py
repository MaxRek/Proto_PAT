import pandas as pd
import numpy as np
import copy
import json
import os
from src.constant import SUB_DEMAND,COMMUNES,DOMAINES

def rowDemandFiller(nbrp : int, quantities : list[int]) -> np.array:
    return nbrp*np.array(quantities)/100

def demandFiller(path : str, file : str):
    columns = ['x', 'y', 'Nom de la structure', 'Nombre de repas par jour']
    datAll = pd.read_csv(path+file+".csv", sep = ";",na_values="NaN")

    #Nettoyage des données, concentration sur les Communes du PAT
    data = datAll.loc[datAll["Commune"].isin(COMMUNES)]
    data = data.dropna(axis=0, subset=["Nombre de repas par jour"])

    #Correction de la colonne du nombre des repas, car présence d'espace
    newColumn = []
    for row in data.iterrows():
        if type(row[1]["Nombre de repas par jour"]) == str:
            value = ""
            for c in row[1]["Nombre de repas par jour"]:
                if(c in ["0","1","2","3","4","5","6","7","8","9"]):
                    value += c
            newColumn.append(int(value))
    data["Nombre de repas par jour"] = newColumn
    
    with(open("in/data/demandFillerRatio.json",'r+')) as f:
        ratios = json.load(f)

    with(open("in/data/demandFiller.json",'r+')) as f:
        demandQuantity = json.load(f)


    quantitiesNames = []
    quantities = []

    if SUB_DEMAND != {}:
        for key in SUB_DEMAND:
            if type(SUB_DEMAND[key]) == list:
                if len(SUB_DEMAND[key]) > 0:
                    if key in demandQuantity.keys():
                        keyTotal = 0
                        for value in SUB_DEMAND[key]:
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
                                print("Erreur : Value dans SUB_DEMAND \""+value+"\" avec aucune quantité affectée.")
                        quantitiesNames.append(key)
                        quantities.append(keyTotal)
                    else:
                        print("Erreur : Key dans SUB_DEMAND \""+key+"\" n'est pas référencé dans les quantités.")
                else:
                    print("Erreur : Key dans SUB_DEMAND \""+key+"\" avec valeur vide")
            else:
                print("Erreur : mauvais typage pour la valeur de key \""+key+"\" dans SUB_DEMAND")
    else:
        print("Erreur : Key dans SUB_DEMAND \""+key+"\" n'est pas référencé dans les quantités.")

    demand = data[columns].loc[(data["Domaine"].isin(DOMAINES)) &(
        (data["Type de restauration"] == "Production et consommation sur place") |
        (data["Type de restauration"] == "Production pour consommation sur place et livraisons à des restaurants satellites")|
        (data["Type de restauration"] == "Production pour livraisons à des restaurants satellites"))
        & (data["Nombre de repas par jour"] > 0)]

    quantitySeries = demand.apply(lambda x : rowDemandFiller(x["Nombre de repas par jour"], quantities),axis=1)
    #quantityFrame = demand.apply(lambda x : rowDemandFiller(x["Nombre de repas par jour"], quantities),axis=1)
    demand[quantitiesNames] = 0
    values = quantitySeries.values

    for i in range((demand.shape[0])-1):
        for j in range(len(values[i])):
            demand.iloc[i,j+4] = values[i][j]

    nameFile = file + "_demand"
    if nameFile+".csv" in os.listdir(path):
        os.remove(path+nameFile+".csv")
    demand.to_csv(path+nameFile+".csv", sep=";")