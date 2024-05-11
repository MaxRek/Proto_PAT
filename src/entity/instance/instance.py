from ..df import Df
from .decision import Dec
from .data import Data
import numpy as np
import os
from src.constant import PATH_IN,PATH_INSTANCE


class Instance:
    df:Df
    dec:Dec
    data:Data
    roads:list
    name:str

    def __init__(self, df:Df, K : int, F:int, Fs:int,Q : int, O:list, d:np.matrix, S:np.matrix, t:np.matrix, ct:np.matrix = np.zeros((1,1))) -> None:
        self.df=df
        self.data=Data(df.N.shape[0], df.E.shape[0], df.F.shape[0], K, F, F-Fs, Fs, Q,O,d,S,ct,t)
        self.dec = Dec()
        self.roads = list()

    def save_instance(self, name:str):
        if PATH_IN in os.listdir():
            os.mkdir(PATH_IN)

        if PATH_INSTANCE in os.listdir(PATH_IN):
            os.mkdir(PATH_IN+PATH_INSTANCE)

        if name not in os.listdir(PATH_IN+PATH_INSTANCE):
            os.mkdir(PATH_IN+PATH_INSTANCE+name)

        self.data.save_data(PATH_IN+PATH_INSTANCE+name+"/","data")
        self.dec.save_dec(PATH_IN+PATH_INSTANCE+name+"/","dec")
        self.df.save_df(PATH_IN+PATH_INSTANCE+name+"/","e","f")
    

        
