import pandas as pd

from src.constant import FIELDS_F
from src.constant import FIELDS_E
from src.constant import PATH_DATA
from src.constant import PATH_FILE_F
from src.constant import PATH_FILE_E

class Df:
    F:pd.DataFrame
    E:pd.DataFrame

    def __init__(self) -> None:
        self.data = pd.DataFrame()

    def load_csv(self):
        self.F = pd.read_csv(PATH_DATA+PATH_FILE_F, sep = ";", na_values="NaN", usecols=FIELDS_F)
        self.E = pd.read_csv(PATH_DATA+PATH_FILE_E, sep = ";", na_values="NaN", usecols=FIELDS_E)

    