from .struct.sub_data import Sub_data
from .init_solution import init_solution
import datetime
import os
from .algorithm.GVNS import GVNS
from .benchmark import *


def control(path:str,name:str,data: Sub_data, nb_calc : int = 40000, nb_perturb:int = 5):

    #Construction solution initiale
    s = init_solution(data)

    #Dossier pour benchmark, pour l'instance puis pour le test
    if name not in os.listdir(path):
        os.mkdir(path+"/"+name)
    now = datetime.datetime.now()
    path_bench = path+"/"+name+"/"+str(now.month)+"_"+str(now.day)+" "+str(now.hour)+"-"+str(now.minute)
    os.mkdir(path_bench)
    path_stats = path_bench+"/stats"
    os.mkdir(path_stats)
    names = [path_stats+"/pre_post",path_stats+"/pre",path_stats+"/post", path_stats+"/graph"]

    #Init benchmark
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

    
    # Debut algorithme
    GVNS(path_bench,data, s, nb_calc, nb_perturb,benchmark)
    
    #Ecriture des résultats + graphe
    with open(path_stats+"/benchmark.txt",'w') as f:
        f.write(str(benchmark))
    plot_time(benchmark["time"],benchmark["non_fini"], path_stats+"/time")
    all_bar_obj(benchmark["z"],benchmark["pre_z"],benchmark["non_fini"],names)
