from ..df import Df
from .decision import Dec
from .data import Data
import numpy as np
import 


class Instance:
    df:Df
    dec:Dec
    data:Data

    def __init__(self, N:list ,df:Df, K : int, F:int, Fs:int,Q : int, O:list, d:np.matrix, S:np.matrix, t:np.matrix) -> None:
        self.df=df
        C = df.E.shape[0]
        P = df.F.shape[0]
        self.dec = Dec()

