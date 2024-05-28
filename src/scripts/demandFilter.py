import pandas as pd
import numpy as np
import os
from src.constant import COMMUNES,DOMAINES

def demandFilter(path : str, file_to_filter : str, file_to_save : str):
    datAll = pd.read_csv(path+file_to_filter+".csv", sep = ";",na_values="NaN")

    #Nettoyage des données, concentration sur les Communes selectionnés
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

    demand = data.loc[(data["Domaine"].isin(DOMAINES)) &(
        (data["Type de restauration"] == "Production et consommation sur place") |
        (data["Type de restauration"] == "Production pour consommation sur place et livraisons à des restaurants satellites")|
        (data["Type de restauration"] == "Production pour livraisons à des restaurants satellites"))
        & (data["Nombre de repas par jour"] > 0)]

    if file_to_save+".csv" in os.listdir(path):
        os.remove(path+file_to_save+".csv")
    demand.to_csv(path+file_to_save+".csv", sep=";")