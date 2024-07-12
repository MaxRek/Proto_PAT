import pandas as pd
import numpy as np
import urllib.parse
import time
import requests
import os

#path = "in/data/"
#file = "Établissements.csv"
#file = "Fournisseurs.csv"

# Importe le fichier.csv pour le cas du Projet d'Alimentation Territoriale
# Ajoute les colonnes "x", "y" au csv si nécéssaire
# Met à jour selon la recherche via nominatim, n'est pas efficace à 100%

def replaceLatLong(path: str, file:str):
    data = pd.read_csv(path+file+".csv", sep = ";",na_values="NaN")
    if not set(["x","y"]).issubset(data.columns):
        data["x"]= 0.0
        data["y"]= 0.0
    failed_indexes = []
    failed_adress = []
    status_code = 0

    for index,row in data.iterrows():
        if data.loc[index,"x"] == 0.0 or data.at[index,"y"] == 0.0:
            if status_code != 403:
                time.sleep(1)

                try:
                    address = row["Adresse"] +", "+row["Commune"]
                    url = 'https://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(address) +'&format=json'
                    response = requests.get(url)
                    print(response.status_code)
                    status_code = response.status_code

                    response_json = response.json()
                    print(response_json)
                    data.at[index,"x"] = response_json[0]["lat"]
                    data.at[index,"y"] = response_json[0]["lon"]
                except:
                    print("Erreur, address = "+row["Adresse"] +", "+row["Commune"])
                    failed_indexes.append(index)
                    failed_adress.append(row["Adresse"] +", "+row["Commune"])
            else:
                failed_indexes.append(index)
                failed_adress.append(row["Adresse"] +", "+row["Commune"])

    if status_code == 403:
        print("L'accès est limité pour cette machine, abandon du requêtage. Veuillez réessayer plus tard.")
    print("Failed at : " + str(failed_indexes))
    print("Adresses : " + str(failed_adress))
    # if data.shape[0] == len(failed_indexes):
    #     print("pas de modification")
    # else:
    #     if "old_"+file+".csv" in os.listdir(path):
    #         os.remove(path+"old_"+file+".csv")
    #     os.rename(path+file+".csv",path+"old_"+file+".csv")
    #     data.to_csv(path+file+".csv", sep=";")
    return data, status_code