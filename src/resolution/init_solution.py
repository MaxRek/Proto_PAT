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
    # print(data.N)
    # print(data.C)
    # print(data.P)
    # print(data.T)

    s.plat.append(Plateforme(choice(list(range(data.N)))))
    s.add_client_to_plat(0,range(data.N,data.C),data.d)
    s.plat[0].calc_LnfPT_c(data.d, data.C, data.F, data.T,data.T, data.Q)

    sum_fs = np.zeros(data.F).tolist()
    for i in s.plat[0].Lfptn:
        for j in range(data.F):
            sum_fs[j] += i[j]
    #print(sum_fs)
    #print(cumul_qt_PT_by_LnfPT(s.plat[0].Lfptn))
    temp = get_fs_prod_ind_qt(data.rev_d)
    s.init_CAW_sales(data.c, data.Q, data.T-1,temp[0],temp[1])
    #s.print_all_plateformes()
    #s.print_sales()
    #print(get_p_cl_by_d(data.d, s.plat[0].cli_affect))
    #print(s.plat[0].Lfptn)
    s.init_CAW_cp(data.c, data.Q, data.C)
    #print(get_sum_qt_c_l_by_d(data.d, s.plat[0].cli_affect,data.F))
    s.init_CAW_lp(data.c, data.Q, data.d, data.F)

    #s.plat[0].print_plateforme()
    s.verif_solution(data.C,data.N,data.Q)
    #print(s.calc_func_obj(data.O,data.c))

    return s
