from .struct.sub_data import Sub_data
from .struct.solution import Solution
from .struct.plateforme import Plateforme
from .tools import * 
from .algorithm.CAW import CAW_F
import math
import numpy as np

def init_solution(data : Sub_data):
    
    s = Solution()

    print(data.N)
    print(data.C)
    print(data.P)
    print(data.T)

    s.plat.append(Plateforme(rand_ind_in_list(list(range(data.N)))))
    s.add_client_to_plat(0,range(data.N,data.C),data.d)
    s.plat[0].calc_LnfPT_c(data.d, data.C, data.F, data.T,data.T, data.Q)

    sum_fs = np.zeros(data.F).tolist()
    for i in s.plat[0].Lfptn:
        for j in range(data.F):
            sum_fs[j] += i[j]
    print(sum_fs)
    print(cumul_qt_PT_by_LnfPT(s.plat[0].Lfptn))
    temp = get_fs_prod_ind_qt(data.rev_d)
    s.init_CAW_sales(data.c, data.Q, data.T-1,temp[0],temp[1])
    #s.print_all_plateformes()
    #s.print_sales()
    #print(get_p_cl_by_d(data.d, s.plat[0].cli_affect))
    print(s.plat[0].Lfptn)
    s.init_CAW_cp(data.c, data.Q, data.C)
    print(get_sum_qt_c_l_by_d(data.d, s.plat[0].cli_affect,data.F))
    s.init_CAW_lp(data.c, data.Q, data.d, data.F)

    s.plat[0].print_plateforme()
    s.verif_solution(data.C,data.N,data.Q)
    print(s.calc_func_obj(data.O,data.c))

    return s




    
    

    # sum_P = np.zeros((data.P-data.C,data.F)).tolist()
    # sum_P2 = np.zeros((data.P-data.C,data.F)).tolist()
    # total_sum_P = np.zeros(data.F).tolist()
    # total_sum_P2 = np.zeros(data.F).tolist()

    # for i in data.rev_d.keys():
    #     sum_P[i-data.C]=get_sum_qt_p_by_rev_d(data.rev_d, i, data.F)
    #     sum_P2[i-data.C] =get_sum_qt_p_by_d(data.d, i, data.F)
    #     for j in range(data.F):
    #         total_sum_P[j] += sum_P[i-data.C][j]
    #         total_sum_P2[j] += sum_P2[i-data.C][j]

    # print(total_sum_P)
    # print(total_sum_P2)
    # print(sum_P)
    # print(sum_P2)
 
    # min_K = math.ceil(max(total_sum_P)/data.Q)+1
    #print(min_K)

    # AVG = np.zeros(data.N).tolist()
    # # print(data.N)
    # # print(data.T)
    # # print(data.T-data.N)
    # max_AVG = 0
    
    # for n in range(data.N):
    #     AVG[n] = sum(data.c[n][data.N:data.T])
    #     AVG[n] = AVG[n]/(data.T-data.N)
    #     if AVG[n] > max_AVG:
    #         max_AVG = AVG[n]

    # min_AVG = np.zeros(min_K)
    # min_AVG = min_AVG + max_AVG
    # min_AVG = min_AVG.tolist()
    # ind_AVG = np.zeros(min_K).tolist()

    # for n in range(data.N):
    #     for o in range(min_K):
    #         if AVG[n] < min_AVG[o] and AVG[n] not in min_AVG[0:o]:
    #             min_AVG[o] = AVG[n]
    #             ind_AVG[o] = n

    # print(min_AVG)
    # print(max_AVG)
    # print(ind_AVG)

    # for i in ind_AVG:
    #     dec.y[int(i)] = 1
        

    #print(get_sum_qt_c_by_d(data.d,data.N+1,data.F))
    # L1 = calc_LnfPT_c(data.d,[data.N+1],data.C,data.T-data.C,data.F)
    # L2 = calc_LnfPT_c(data.d,[data.N+2],data.C,data.T-data.C,data.F)
    
    #print(verif_LnfPT(get_LnfPT_c(data.d,list(range(data.N,data.C)),data.C,data.T-data.C,data.F),data.Q))

    #Calcul du meilleur indice sum_C_{c,n} et récupération des prods 
    # sum_C = np.zeros((data.C-data.N,min_K)).tolist()
    
    # for i in range(data.N,data.C):
    #     for n in range(len(ind_AVG)):
    #         sum_C[int(i-data.N)][n]=data.c[int(i)][ind_AVG[n]]
    #         #Est ce que le client a des produits qu'il faut faire transformer ?
    #         indexes = get_p_c_by_d(data.d, i)
    #         if get_sum_qt_c_by_d(data.d, i, data.F)[0] > 0:
    #             indexes.append(data.T-1)
    #         for k in indexes:
    #             sum_C[int(i-data.N)][n] += data.c[ind_AVG[n]][k]
                
    # for i in range(data.N,data.C):
    #     b = False
    #     #print(i)
    #     # print(sum_C[i-data.N])
    #     n_affect = sum_C[i-data.N].index(min(sum_C[i-data.N]))
    #     # print(n_affect)
    #     while not b:
    #         ln_pre = dec.LnfPT[ind_AVG[n_affect]]
    #         LnfPT = calc_LnfPT_c(data.d,[i], data.C, data.T-data.C,data.F)
    #         ln_post = add_LnfPT(ln_pre,LnfPT[0])
    #        # print(calc_LnfPT_c(data.d,[i], data.C, data.T-data.C,data.F))
    #        # print(ln_post)
    #         if verif_LnfPT(ln_post, data.Q):
    #             dec.wc[ind_AVG[n_affect]][i-data.N] = 1
    #             dec.wt[ind_AVG[n_affect]] = LnfPT[1]
    #             for p in get_p_c_by_d(data.d, i):
    #                 dec.wp[ind_AVG[n_affect]][p-data.C] = 1
    #             dec.LnfPT[ind_AVG[n_affect]] = ln_post
    #             b = True
    #             #print(cumul_qt_PT_by_LnfPT(ln_post))
    #         else:
    #             sum_C[n_affect] = sum_C[n_affect]*100

    #Affectation terminée, construction des tournées
    #Réduction des trajets à la plateforme et aux acteurs concernées.
    #dec.visite_plat_prod()

    # print(data.d[65])
    # print(data.rev_d.keys())
    # print(data.rev_d[19+data.C])
    # print(19+data.C)
    # print(data.N)
    # print(data.C)
    # print(data.P- data.C)
    # for i in ind_AVG:
    #     if(i == 31):
    #         # print("_________________")
    #         #print(dec.LnfPT[i])
    #         # print("_________________")
    #         indexes = [int(i)]
    #         temp_QTs = cumul_qt_PT_by_LnfPT(dec.LnfPT[int(i)])
    #         # print(temp_QTs)
    #         # print("_________________")

    #         QTs = []
    #         for p in temp_QTs[1]:
    #             indexes.append(p+data.C)
    #             QTs.append(temp_QTs[0][p])
    #         # print(QTs)
    #         # print(indexes)
    #     #print(indexes)
        
    #         CAW_F(sub_matrix(data.c,indexes),data.Q,QTs,indexes)

    

    

    
        