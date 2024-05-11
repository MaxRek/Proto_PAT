import pandas as pd
import copy

from src.constant import FIELDS_F
from src.constant import FIELDS_E
from src.constant import FIELDS_N
from src.constant import PATH_DATA
from src.constant import PATH_FILE_F
from src.constant import PATH_FILE_E
from src.constant import PATH_FILE_N
from src.constant import PATH_IN
from src.constant import COMMUNES

class Df:
    F:pd.DataFrame
    E:pd.DataFrame
    N:pd.DataFrame

    def __init__(self) -> None:
        self.data = pd.DataFrame()

    def load_csv(self, path:str = PATH_IN+PATH_DATA, e_name:str = PATH_FILE_E, f_name:str = PATH_FILE_F, n_name:str = PATH_FILE_N):
        temp_F = pd.read_csv(path+f_name+".csv", sep = ";", na_values="NaN", usecols=FIELDS_F)
        temp_E = pd.read_csv(path+e_name+".csv", sep = ";", na_values="NaN", usecols=FIELDS_E)
        temp_N = pd.read_csv(path+n_name+".csv", sep = ";", na_values="NaN", usecols=FIELDS_N)

        print(temp_E.columns)
        print(temp_F.columns)
        self.F = copy.deepcopy(temp_F.loc[temp_F["Commune"].isin(COMMUNES)])
        self.E = copy.deepcopy(temp_E.loc[temp_E["Commune"].isin(COMMUNES)])
        #Les entrepôts peuvent potentiellement être en dehors du territoire
        self.N = temp_N

    def save_df(self, path:str, e_name:str, f_name:str, n_name:str):
        self.F.to_csv(path+f_name, sep = ";")
        self.E.to_csv(path+e_name, sep = ";")
        self.N.to_csv(path+n_name, sep = ";")


    