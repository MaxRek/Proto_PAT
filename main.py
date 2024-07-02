import sys
import pandas as pd
import numpy as np
sys.path.insert(0, '')
from src.scripts.findLatLong import replaceLatLong
from src.scripts.demandFiller import demandFiller_Dcf, demandFiller_Dcpf,gen_O
from src.constant import PATH_DATA, PATH_FILE_E, SUB_DEMAND, PATH_IN, PATH_OUT, PATH_INSTANCE
from src.resolution.pre_resolve import reduction
from src.resolution.init_solution import init_solution
from src.resolution.resolve import control

from src.entity.aff import Aff
from src.entity.instance.instance import Instance
#from src.resolution.check import check_before_resolve

truc = Aff()
truc.df.load_csv(path=PATH_IN+"/"+PATH_INSTANCE+"/didactic/",e_name="e",f_name="f",n_name="n",t_name="t")
# truc.add_point(truc.df)
# truc.M.save("Map_PAT_t.ht#ml")
# truc.df.load_csv("in/instance/didactic/","e","f","n")

Prod = {"S":["Legumes"],"P":["Viandes","Legumineuses","Laitages"]}
# quantité calculée à l'année, donc pour les semaines (scolaires) = /36, 
mult = 1/36*0.2
#probabilité qu'un producteur propose une autre filière de produits. 0 = n'en propose pas d'autres, 1 = tous les prod vont tout proposer 
multi_f = 0.4
#ratio_p pour indiquer donner une affectation par filière pour un producteur (la somme doit être égal à 1)
ratio_p = [0.4,0.4,0.1,0.1]
#ratio_pc pour indiquer une approximation du nombre de producteurs chez qui la cantine commande pour une fillière de produit (que des nombres entiers >= 1)
ratio_pc = [2,1,1,1]

instance = Instance(truc.df, 4,4,1,2500,[4,5,6,5],np.zeros(20).tolist(),np.zeros(20).tolist(),np.zeros(20).tolist(),prod=Prod)
instance.name = "didactic"

#demandFiller_Dcpf(PATH_IN+"/"+PATH_INSTANCE+"/",instance.name+"/e",instance.name+"/f", instance.name+"/d",mult = mult, multi_f=multi_f, ratio_p=ratio_p, ratio_pc= ratio_pc)
instance.load_instance()
instance.data.Q = 1200
#print(instance.data.d)
instance.save_instance()

control(PATH_OUT,instance)

#print(len(instance.data.c))
# instance.data.gen_c()
# instance.save_instance()
# print(instance.data.d)
# print(reduction(instance)[0].d)
# print(str(instance.data.N) + " "+ str(instance.data.C)+ " "+ str(instance.data.P) + " " + str(instance.data.P+instance.data.C+instance.data.N) + " " +str(len(instance.data.c)))

# print(reduction(instance)[0].rev_d)

#instance.load_data_prod(Prod,ratio)
#instance.data.load_Dd(instance.name,"d")

#instance.data.print_d()
#instance.data.save_d(instance.name,"bababa")
# instance.load_instance()
# print(check_before_resolve(instance))

#instance.data.O = gen_O(instance.data.N)

