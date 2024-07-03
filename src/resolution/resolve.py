from ..entity.instance.instance import Instance
from .init_solution import init_solution
import datetime
import os
from .tools import updating_solution_to_instance, translate_solution, dict_solution_to_txt
from .algorithm.GVNS import GVNS
from .benchmark import *
from src.resolution.pre_resolve import reduction

def control(path:str,inst:Instance, nb_calc : int = 40, nb_perturb:int = 1):

    #Reduction du problème aux sommets concernées
    sub_data,indexes = reduction(inst)
    
    #Construction solution initiale
    s = init_solution(sub_data)

    #print(s.soluce_to_dict())    

    #Dossier pour benchmark, pour l'instance puis pour le test
    if inst.name not in os.listdir(path):
        os.mkdir(path+"/"+inst.name)
    now = datetime.datetime.now()
    path_bench = path+"/"+inst.name+"/"+str(now.month)+"_"+str(now.day)+" "+str(now.hour)+"-"+str(now.minute)
    os.mkdir(path_bench)
    path_stats = path_bench+"/stats"
    os.mkdir(path_stats)
    names = [path_stats+"/pre_post",path_stats+"/pre",path_stats+"/post", path_stats+"/graph"]
    path_solution = path_bench+"/solution"
    os.mkdir(path_solution)

    #Init benchmark<
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

    #Ecriture des résultats + graphe
    with open(path_stats+"/benchmark.txt",'w') as f:
        f.write(str(benchmark))
    plot_time(benchmark["time"],benchmark["non_fini"], path_stats+"/time")
    all_bar_obj(benchmark["z"],benchmark["pre_z"],benchmark["non_fini"],names)

    to_print = sp.soluce_to_dict()
    with open(path_solution+"/solution.txt","w") as f:
        f.write(str(to_print))

    to_print = updating_solution_to_instance(to_print,indexes, sub_data)
    with open(path_solution+"/solution_updated.txt","w") as f:
        f.write(str(to_print))

    with open(path_solution+"/solution_updated_presented.txt","w") as f:
        f.write(str(dict_solution_to_txt(to_print)))

    to_print = translate_solution(to_print,inst.data.df)
    with open(path_solution+"/solution_translated.txt","w") as f:
        f.write(str(to_print))

    with open(path_solution+"/solution_translated_presented.txt","w") as f:
        f.write(str(dict_solution_to_txt(to_print)))

