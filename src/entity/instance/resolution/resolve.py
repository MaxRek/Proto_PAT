from ...aff import Aff
from .struct.sub_data import Sub_data
from .init_solution import init_solution
from .algorithm.GVNS import GVNS
from .benchmark import *
import os
import datetime
from .struct.solution import Solution
from .struct.plateforme import Plateforme

from.benchmark import *



import numpy as np

def control(path:str,data: Sub_data, nb_calc : int = 40000, nb_perturb:int = 30):
    s = init_solution(data)

    # sp = Solution()
    # for i in range(data.N):
    #     p = Plateforme(i)
    #     sp.plat.append(p)
    # for c in range(data.N, data.C):
    #     sp.plat[0].add_client(data.d, c)

    # aff = Aff()

    # temp = sp.soluce_propre_to_map(data.locations, data.T-1)
    # aff.save_soluce("propre",temp[0],roads = temp[1])
    # aff.clean_M()

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
    
    # aff = Aff()
    GVNS(path_bench,data, s, nb_calc, nb_perturb,benchmark)
    print(benchmark)
    path_stats = path_bench+"/stats"
    names = [path_stats+"/pre_post",path_stats+"/pre",path_stats+"/post", path_stats+"/graph"]

    os.mkdir(path_stats)
    with open(path_stats+"/benchmark.txt",'w') as f:
        f.write(str(benchmark))

    plot_time(benchmark["time"],benchmark["non_fini"], path_stats+"/time")
    all_bar_obj(benchmark["z"],benchmark["pre_z"],benchmark["non_fini"],names)
    print(benchmark)