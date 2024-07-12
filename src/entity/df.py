import pandas as pd
import copy

from src.constant import A_FIELDS_F
from src.constant import A_FIELDS_E
from src.constant import A_FIELDS_N
from src.constant import A_FIELDS_T

from src.constant import PATH_DATA
from src.constant import PATH_FILE_F
from src.constant import PATH_FILE_E
from src.constant import PATH_FILE_N
from src.constant import PATH_FILE_T

from src.constant import PATH_IN
from src.constant import COMMUNES

class Df:
    F:pd.DataFrame
    E:pd.DataFrame
    N:pd.DataFrame
    T:pd.DataFrame

    def __init__(self) -> None:
        self.F = pd.DataFrame()
        self.E = pd.DataFrame()
        self.N = pd.DataFrame()
        self.T = pd.DataFrame()


    def load_csv(self, path:str = PATH_IN+"/"+PATH_DATA, e_name:str = PATH_FILE_E, f_name:str = PATH_FILE_F, n_name:str = PATH_FILE_N, t_name:str = PATH_FILE_T):
        self.load_csv_E(path, e_name)
        self.load_csv_F(path, f_name)
        self.load_csv_N(path, n_name)
        self.load_csv_T(path, t_name)

    def load_csv_E(self, path:str = PATH_IN+"/"+PATH_DATA, e_name:str = PATH_FILE_E):
        temp_E = pd.read_csv(path+"/"+e_name+".csv", sep = ";", na_values="NaN")
        
        temp_E = copy.deepcopy(temp_E.loc[temp_E["Commune"].isin(COMMUNES)])
        found = False
        i = 0
        while not found and i < len(A_FIELDS_E):
            stop = False
            j = 0
            while j < len(A_FIELDS_E[i]) and not stop:
                if A_FIELDS_E[i][j] in temp_E.columns:
                    j += 1
                else:
                    stop = True
            if stop:
                i += 1
            else:
                found = True
        if found:
            self.E = copy.deepcopy(temp_E[A_FIELDS_E[i]])
        else:
            print("E : Colonnes non trouvées")
            print(temp_E.columns)
        return i

    def load_csv_F(self, path:str = PATH_IN+"/"+PATH_DATA, f_name:str = PATH_FILE_F):
        temp_F = pd.read_csv(path+"/"+f_name+".csv", sep = ";", na_values="NaN")
        temp_F = copy.deepcopy(temp_F.loc[temp_F["Commune"].isin(COMMUNES)])
        found = False
        i = 0
        while not found and i < len(A_FIELDS_F):
            stop = False
            j = 0
            while j < len(A_FIELDS_F[i]) and not stop:
                if A_FIELDS_F[i][j] in temp_F.columns:
                    j += 1
                else:
                    stop = True
            if stop:
                i += 1
            else:
                found = True
        if found:
            self.F = copy.deepcopy(temp_F[A_FIELDS_F[i]])
        else:
            print("F : Colonnes non trouvées")
            print(temp_F.columns)
        return i

    def load_csv_N(self, path:str = PATH_IN+"/"+PATH_DATA, n_name:str = PATH_FILE_N):
        temp_N = pd.read_csv(path+"/"+n_name+".csv", sep = ";", na_values="NaN")

        found = False
        i = 0
        while not found and i < len(A_FIELDS_N):
            stop = False
            j = 0
            while j < len(A_FIELDS_N[i]) and not stop:
                if A_FIELDS_N[i][j] in temp_N.columns:
                    j += 1
                else:
                    stop = True
            if stop:
                i += 1
            else:
                found = True
        if found:
            self.N = copy.deepcopy(temp_N[A_FIELDS_N[i]])
        else:
            print("N : Colonnes non trouvées")
            print(temp_N.columns)
        return i

    def load_csv_T(self, path:str = PATH_IN+"/"+PATH_DATA, t_name:str = PATH_FILE_T):
        temp_T = pd.read_csv(path+"/"+t_name+".csv", sep = ";", na_values="NaN")
        #temp_T = copy.deepcopy(temp_T.loc[temp_T["Commune"].isin(COMMUNES)])

        found = False
        i = 0
        while not found and i < len(A_FIELDS_T):
            stop = False
            j = 0
            while j < len(A_FIELDS_T[i]) and not stop:
                if A_FIELDS_T[i][j] in temp_T.columns:
                    j += 1
                else:
                    stop = True
            if stop:
                i += 1
            else:
                found = True
        if found:
            self.T = copy.deepcopy(temp_T[A_FIELDS_T[i]])

        else:
            print("T : Colonnes non trouvées")
            print(temp_T.columns)
        return i

    def save_df(self, path:str, e_name:str, f_name:str, n_name:str, t_name:str):
        self.F.to_csv(path+"/"+f_name+".csv", sep = ";")
        self.E.to_csv(path+"/"+e_name+".csv", sep = ";")
        self.N.to_csv(path+"/"+n_name+".csv", sep = ";")
        self.T.to_csv(path+"/"+t_name+".csv", sep = ";")

    def get_coords_N(self):
        return self.N[["y","x"]]
    
    def get_coords_E(self):
        return self.E[["y","x"]]

    def get_coords_F(self):
        return self.F[["y","x"]]
    
    def get_coords_T(self):
        return self.T[["y","x"]]

    def get_coords(self):
        return [self.get_coords_N(),self.get_coords_E(),self.get_coords_F()]
    
    