from ...aff import Aff
from .struct.sub_data import Sub_data
from .init_solution import init_solution
from .algorithm.GVNS import GVNS
import os
import datetime
from.benchmark import *


import numpy as np

def control(path:str,data: Sub_data, nb_calc : int = 20000, nb_perturb:int = 50):
    s = init_solution(data)

    if "benchmark" not in os.listdir(path):
        os.mkdir(path+"/benchmark")
    
    
    now = datetime.datetime.now()
    path_bench = path+"/benchmark/"+str(now.month)+"_"+str(now.day)+" "+str(now.hour)+"-"+str(now.minute)
    benchmark = {
        "pre_z":[],
        "z" :[],
        "time": [],
        "nb_plat" : [],
        "k_VNS": [],
        "nb_modifs": [],
        "modif_k": [],
        "non_fini": []
    }
    os.mkdir(path_bench)
    
    path_stat = path_bench+"/stats"
    os.mkdir(path_stat)

    names = [path_stat+"/mixte", path_stat+"/pre", path_stat+"/post", path_stat+"/graph"]
    
    # aff = Aff()
    GVNS(path_bench,data, s, nb_calc, nb_perturb,benchmark)
    print(benchmark["pre_z"])
    print(benchmark["z"])
    plot_time(benchmark["time"], benchmark["non_fini"], path_stat+"/time")
    all_bar_obj(benchmark["z"],benchmark["pre_z"],benchmark["non_fini"],names)