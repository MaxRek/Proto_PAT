from .struct.sub_data import Sub_data
from ..entity.instance import instance
from .init_solution import init_solution
import datetime
import os
from .algorithm.GVNS import GVNS
from .benchmark import *
from src.resolution.pre_resolve import reduction



def control(path:str,inst:instance, nb_calc : int = 200000, nb_perturb:int = 30):

    #Reduction du problème aux sommets concernées
    sub_data = reduction(inst)
    
    #Construction solution initiale
    s = init_solution(sub_data)

    #Dossier pour benchmark, pour l'instance puis pour le test
    if inst.name not in os.listdir(path):
        os.mkdir(path+"/"+inst.name)
    now = datetime.datetime.now()
    path_bench = path+"/"+inst.name+"/"+str(now.month)+"_"+str(now.day)+" "+str(now.hour)+"-"+str(now.minute)
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
    sp = GVNS(path_bench, sub_data, s, nb_calc, nb_perturb,benchmark)
    print(sp.calc_func_obj(sub_data.O,sub_data.c))


    #Ecriture des résultats + graphe
    with open(path_stats+"/benchmark.txt",'w') as f:
        f.write(str(benchmark))
    plot_time(benchmark["time"],benchmark["non_fini"], path_stats+"/time")
    all_bar_obj(benchmark["z"],benchmark["pre_z"],benchmark["non_fini"],names)
