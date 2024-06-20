from ...aff import Aff
from .struct.sub_data import Sub_data
from .init_solution import init_solution
from .algorithm.GVNS import GVNS
import os
import datetime

import numpy as np

def control(path:str,data: Sub_data, nb_calc : int = 20000, nb_perturb:int = 100):
    s = init_solution(data)

    if "benchmark" not in os.listdir(path):
        os.mkdir(path+"/benchmark")
    
    
    now = datetime.datetime.now()
    path_bench = path+"/benchmark/"+str(now.month)+"_"+str(now.day)+" "+str(now.hour)+"-"+str(now.minute)
    benchmark = {
        "pre_z":[],
        "z" :[],
        "time": [],
        "nb_modifs": [],
        "fini": []
    }
    os.mkdir(path_bench)
    


    # aff = Aff()
    GVNS(path_bench,data, s, nb_calc, nb_perturb,benchmark)
