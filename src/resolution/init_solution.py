from .struct.sub_data import Sub_data
from .struct.solution import Solution
from .struct.plateforme import Plateforme
from .tools import * 
from .algorithm.CAW import CAW_F
import math
import numpy as np
from random import choice

def init_solution(data : Sub_data):
    s = Solution()
    print(data.N)
    print(data.C)
    print(data.P)
    print(data.T)

    #Selection d'une plateforme au hasard pour commencer 
    s.plat.append(Plateforme(choice(list(range(data.N)))))
    s.add_client_to_plat(0,range(data.N,data.C),data.d)
    s.plat[0].calc_LnfPT_c(data.d, data.C, data.F, data.T,data.T, data.Q)
    
    #Initialisation des tournées
    temp = get_fs_prod_ind_qt(data.rev_d)
    s.init_CAW_sales(data.c, data.Q, data.T-1,temp[0],temp[1])
    s.init_CAW_cp(data.c, data.Q, data.C)
    s.init_CAW_lp(data.c, data.Q, data.d, data.F)

    s.print_all_plateformes()

    #Si la solution n'est pas admissible, suppresion de la solution
    if not s.verif_solution(data.C, data.N, data.Q):
        s = False

    return s
