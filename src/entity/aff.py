import folium
import json
from .etablissement import Etablissement
from .fournisseur import Fournisseur
from .df import Df
from src.constant import COLOR_PIN_F
from src.constant import COLOR_PIN_E
from src.constant import FIELDS_F
from src.constant import FIELDS_E



class Aff:
    M:folium.Map
    location:tuple
    z_start:float
    df:Df
    roads:list

    def __init__(self, loc:tuple, z_st:float):
        self.df = Df()
        self.F = list[Fournisseur]
        self.location = loc
        self.z_start = z_st
        self.M = folium.Map(self.location, zoom_start = self.z_start, control_scale = True, tiles = "openstreetmap")

    def add_point(self,data_to_add:Df, color_f:str = COLOR_PIN_F, color_e:str = COLOR_PIN_E):
        if data_to_add.E.shape[0] > 0:
            for row in data_to_add.E.iterrows():
                try:
                    folium.Marker(
                        location=list(row[1][FIELDS_E[1:3]]),
                        popup=row[1][FIELDS_E[0]],
                        icon=folium.Icon(color=color_e)
                    ).add_to(self.M)
                except:
                    print("Erreur affichage Etablissement : ")
                    print(row[1])
        if data_to_add.F.shape[0] > 0:
            for row in data_to_add.F.iterrows():
                try:
                    folium.Marker(
                        location=list(row[1][FIELDS_F[1:3]]),
                        popup=row[1][FIELDS_F[0]],
                        icon=folium.Icon(color=color_f)
                    ).add_to(self.M)
                except:
                    print("Erreur affichage Etablissement : ")
                    print(row[1])
