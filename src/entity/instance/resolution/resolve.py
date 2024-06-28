from ...aff import Aff
from .struct.sub_data import Sub_data
from .init_solution import init_solution
import datetime
import os
from .algorithm.GVNS import GVNS
from .benchmark import *

import numpy as np

def control(path:str,data: Sub_data, nb_calc : int = 10000, nb_perturb:int = 5):
    print(path)
    print(data)
    
    s = init_solution(data)

    if "benchmark" not in os.listdir(path):
        os.mkdir(path+"/benchmark")
    
    now = datetime.datetime.now()
    path_bench = path+"/benchmark/"+str(now.month)+"_"+str(now.day)+" "+str(now.hour)+"-"+str(now.minute)
    os.mkdir(path_bench)
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

    
    # aff = Aff()
    GVNS(path_bench,data, s, nb_calc, nb_perturb,benchmark)
    path_stats = path_bench+"/stats"
    os.mkdir(path_stats)
    names = [path_stats+"/pre_post",path_stats+"/pre",path_stats+"/post", path_stats+"/graph"]

    with open(path_stats+"/benchmark.txt",'w') as f:
        f.write(str(benchmark))

    plot_time(benchmark["time"],benchmark["non_fini"], path_stats+"/time")
    all_bar_obj(benchmark["z"],benchmark["pre_z"],benchmark["non_fini"],names)
