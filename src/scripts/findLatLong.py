import pandas as pd
import numpy as np
import urllib.parse
import json
import requests
import os

#path = "in/data/"
#file = "Établissements.csv"
#file = "Fournisseurs.csv"

# Importe le fichier.csv pour le cas du Projet d'Alimentation Territoriale
# Ajoute les colonnes "x", "y" au csv si nécéssaire
# Met à jour selon la recherche via nominatim, n'est pas efficace à 100%

def replaceLatLong(path: str, file:str):
    data = pd.read_csv(path+file, sep = ";",na_values="NaN")
    if not set(["x","y"]).issubset(data.columns):
        data["x"]= np.nan
        data["y"]= np.nan
    failed_indexes = [] 
    for index,row in data.iterrows():
        try:
            address = row["Adresse"] +", "+row["Commune"]
            url = 'https://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(address) +'&format=json'
            response = requests.get(url).json() 
            data.at[index,"x"] = response[0]["lat"]
            data.at[index,"y"] = response[0]["lon"]
        except:
            print("Erreur, address = "+address)
            failed_indexes.append(index)
    print("Failed at : " + str(failed_indexes))
    if data.shape[0] == len(failed_indexes):
        print("pas de modification")
    else:
        if "old_"+file in os.listdir(path):
            os.remove(path+"old_"+file)
        os.rename(path+file,path+"old_"+file)
        data.to_csv(path+file, sep=";")