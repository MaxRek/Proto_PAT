from..struct.solution import Solution
from..struct.sub_data import Sub_data
from..struct.plateforme import Plateforme
from..struct.tournee import Tournee
import copy
# from numpy import random as rd
import time
from ..tools import rand_ind_in_list, reduct_LnfPT, calc_LnfPT_c, get_fs_prod_ind_qt, get_sum_qt_c_l_by_d
from .Neighboorhoods_gen import *


#INSERTION intra_tournee
#entry = paramètre permettant de séléctionner 
# [
#   index_plat : -2 pour tournées sale, 0 à nb plateforme
#   index_type_tournee : 0 pour sales, 1 pour propre
#   index_tournee : 0 à nb de tournee de tel type
#   indexes_affect : (index_sommet à insérer, index_insertion du sommet)
# ]
def N1_intra(x:Solution, data:Sub_data, entry:list = [-1,-1,-1,[-1,-1]]):
    #si index_plat non déterminé, assignation à une plat ouverte ou transf    
    if entry[0] == -1 or entry[1] == -1 or entry[2] == -1 or entry[3][0] == -1:
        e = N1_intra_rand(x,entry)
    else:
        e = copy.deepcopy(entry)
    # print(entry)     
    # print(e)

    xp = copy.deepcopy(x)
    #Dans le cadre de la collecte sale
    if e[0] == -2:
        t0 = xp.sales[e[2]]
        t0.reinsert(e[3][0],e[3][1])
        # x.sales[e[2]].print_tournee()
        # t0.print_tournee()
    else:
        t0 = xp.plat[e[0]].tournees[e[1]][e[2]]
        t0.reinsert(e[3][0],e[3][1])
        # x.plat[e[0]].tournees[e[1]][e[2]].print_tournee()
        # t0.print_tournee()

    return xp

#INSERTION inter_tournee
#entry = paramètre permettant de séléctionner 
# [
#   index_plat : -2 pour tournées sale, 0 à nb plateforme
#   index_type_tournee : 0 pour sales, 1 pour propre
#   indexes_tournee : (0 à nb de tournee de tel type, 0 à nb de tournee de tel type)
#   index_affect : (index_sommet à ré-insérer, index où réinsérer sommet)
# ]
def N1_inter(x:Solution, data:Sub_data, entry = [-1,-1,[-1,-1],[-1,-1]]):
    if entry[0] == -1 or entry[1] == -1 or entry[2][0] == -1 or entry[2][1] == -1 or entry[3] == -1:
        e = N1_inter_rand(x,entry)
    else:
        e = copy.deepcopy(entry)
    print(entry)     
    print(e)

    xp = copy.deepcopy(x)
    if e[0] == -2:

        t0 = xp.sales[e[2][0]]
        t1 = xp.sales[e[2][1]]
        x.sales[e[2][0]].print_tournee()
        x.sales[e[2][1]].print_tournee()

        s = t0.pop(e[3][0])
        t1.insert_sommet(s,e[3][1])

        deleted = xp.sales[e[2][0]].size == 0
        if deleted:
            xp.sales.pop(e[2][0])
        # print("La tournée a été supprimée : "+str(deleted))
        
        if not deleted:
            if e[1] == 0: #Tournée de collecte
                t0.calc_load(reduct_LnfPT(xp.plat[e[0]].Lfptn,data.C))
            else: #Tournée de livraison
                t0.load = sum(get_sum_qt_c_l_by_d(data.d, t0.order,data.F))
            t0.print_tournee()
        if e[1] == 0: #Tournée de collecte
            t1.calc_load(reduct_LnfPT(xp.plat[e[0]].Lfptn,data.C))
        else: #Tournée de livraison
            t1.load = sum(get_sum_qt_c_l_by_d(data.d, t1.order,data.F))
        # t1.print_tournee()
        if(t0.load > data.Q or t1.load > data.Q):
            print("Insertion impossible pour points "+str(e[3])+" de tournée "+str(e[2][0])+" à "+str(e[2][1]))
            xp = x
    else:
        t0 = xp.plat[e[0]].tournees[e[1]][e[2][0]]
        t1 = xp.plat[e[0]].tournees[e[1]][e[2][1]]
        x.plat[e[0]].tournees[e[1]][e[2][0]].print_tournee()
        x.plat[e[0]].tournees[e[1]][e[2][1]].print_tournee()
        
        # t0.print_tournee()
        # t1.print_tournee()
        s = t0.pop(e[3][0])
        t1.insert_sommet(s, e[3][1])

        #Verifiez si la tounrée 0 n'est pas vide apres avoir pris un sommet
        deleted = xp.plat[e[0]].tournee_post_del_point(e[1],e[2][0])
        print("La tournée a été supprimée : "+str(deleted))
        
        if not deleted:
            if e[1] == 0: #Tournée de collecte
                t0.calc_load(reduct_LnfPT(xp.plat[e[0]].Lfptn,data.C))
            else: #Tournée de livraison
                t0.load = sum(get_sum_qt_c_l_by_d(data.d, t0.order,data.F))
            # t0.print_tournee()
        if e[1] == 0: #Tournée de collecte
            t1.calc_load(reduct_LnfPT(xp.plat[e[0]].Lfptn,data.C))
        else: #Tournée de livraison
            t1.load = sum(get_sum_qt_c_l_by_d(data.d, t1.order,data.F))
        # t1.print_tournee()
        
        
        if t1.load > data.Q:
            print("Insertion impossible pour points "+str(e[3])+" de tournée "+str(e[2][0])+" à "+str(e[2][1]))
            xp = x

    return xp

#SWAP intra_tournee
#entry = paramètre permettant de séléctionner 
# [
#   index_plat : -2 pour tournées sale, 0 à nb plateforme
#   index_type_tournee : 0 pour sales, 1 pour propre
#   index_tournee : 0 à nb de tournee de tel type
#   indexes_affect : (index_sommet à swap, index_sommet à swap)
# ]

def N2_intra(x:Solution, data:Sub_data, entry = [-1,-1,-1,[-1,-1]]):
    if entry[0] == -1 or entry[1] == -1 or entry[2] == -1 or entry[3][0] == -1:
        e = N2_intra_rand(x,entry)
    else:
        e = copy.deepcopy(entry)
    # print(entry)     
    # print(e)
    xp = copy.deepcopy(x)

    if e[0] == -2:
        t0 = xp.sales[e[2]]
        t0.swap_two_s_order(e[3][0],e[3][1])
        # x.sales[e[2]].print_tournee()
        # t0.print_tournee()
    else:
        t0 = xp.plat[e[0]].tournees[e[1]][e[2]]
        t0.reinsert(e[3][0],e[3][1])
        # x.plat[e[0]].tournees[e[1]][e[2]].print_tournee()
        # t0.print_tournee()

    return xp

#SWAP inter_tournee
#entry = paramètre permettant de séléctionner 
# [
#   index_plat : -2 pour tournées sale, 0 à nb plateforme
#   index_type_tournee : 0 pour sales, 1 pour propre
#   index_tournee : (0 à nb de tournee de tel type,0 à nb de tournee de tel type)
#   indexes_affect : (index_sommet à swap dans tournée 1, index_sommet à swap dans tournée 2)
# ]
def N2_inter(x:Solution, data:Sub_data, entry = [-1,-1,[-1,-1],[-1,-1]]):
    if entry[0] == -1 or entry[1] == -1 or entry[2][0] == -1 or entry[3][0] == -1:
        e = N2_inter_rand(x,entry)
    else:
        e = copy.deepcopy(entry)
    # print(entry)     
    # print(e)
    
    xp = copy.deepcopy(x)
    
    if e[0] == -2:
        t0 = xp.sales[e[2][0]]
        t1 = xp.sales[e[2][1]]
        # t0.print_tournee()
        # t1.print_tournee()

        temp = t0.order[e[3][0]]
        t0.order[e[3][0]] = t1.order[e[3][1]]
        t1.order[e[3][1]] = temp

        fs= get_fs_prod_ind_qt(data.rev_d)
        t0.calc_load(fs)
        t1.calc_load(fs)
    else:
        t0 = xp.plat[e[0]].tournees[e[1]][e[2][0]]
        t1 = xp.plat[e[0]].tournees[e[1]][e[2][1]]
        # t0.print_tournee()
        # t1.print_tournee()

        temp = t0.order[e[3][0]]
        t0.order[e[3][0]] = t1.order[e[3][1]]
        t1.order[e[3][1]] = temp

        if e[1] == 0: #Tournée de collecte
            t0.calc_load(reduct_LnfPT(xp.plat[e[0]].Lfptn,data.C))
            t1.calc_load(reduct_LnfPT(xp.plat[e[0]].Lfptn,data.C))
        else: #Tournée de livraison
            t0.load = sum(get_sum_qt_c_l_by_d(data.d, t0.order,data.F))
            t1.load = sum(get_sum_qt_c_l_by_d(data.d, t1.order,data.F))

    # t0.print_tournee()
    # t1.print_tournee()
           
    if t0.load > data.Q or t1.load > data.Q:
        # print("Swap impossible pour points "+str(e[3])+" de tournée "+str(e[2][0])+" à "+str(e[2][1]))
        xp = x
        # if(e[0] == -2):
        #     xp.sales[e[2][0]].print_tournee()
        #     xp.sales[e[2][1]].print_tournee()
        # else:
        #     xp.plat[e[0]].tournees[e[1]][e[2][0]].print_tournee()
        #     xp.plat[e[0]].tournees[e[1]][e[2][1]].print_tournee()

    return xp

#EXTENDED OR_OPT intra_tournee
#entry = paramètre permettant de séléctionner 
# [
#   index_plat : -2 pour tournées sale, 0 à nb plateforme
#   index_type_tournee : 0 pour sales, 1 pour propre
#   index_tournee : 0 à nb de tournee de tel type
#   indexes_affect : ([index_debut seq, index_fin seq], index où inserer seq)
# ]
def N3_intra(x:Solution, data:Sub_data, entry = [-1,-1,-1,[[-1,-1],-1]]):
    if entry[0] == -1 or entry[1] == -1 or entry[2] == -1 or entry[3][0][0] == -1 or entry[3][0] == -1 :
        e = N3_intra_rand(x,entry)
    else:
        e = copy.deepcopy(entry)
    print(entry)     
    print(e)

    xp = copy.deepcopy(x)
    if e[0] == -2:
        t0 = xp.sales[e[2]]

        t0.extended_or_opt(e[3][0], e[3][1])
        x.sales[e[2]].print_tournee()
        t0.print_tournee()
    else:
        t0 = xp.plat[e[0]].tournees[e[1]][e[2]]
        t0.extended_or_opt(e[3][0], e[3][1])
        x.plat[e[0]].tournees[e[1]][e[2]].print_tournee()
        t0.print_tournee()
    return xp

#EXTENDED OR_OPT inter_tournee
#entry = paramètre permettant de séléctionner 
# [
#   index_plat : -2 pour tournées sale, 0 à nb plateforme
#   index_type_tournee : 0 pour sales, 1 pour propre
#   index_tournee : (0 à nb de tournee de tel type, 0 à nb de tournee de tel type)
#   indexes_affect : ([index_debut seq, index_fin seq], index où inserer seq dans t2)
# ]
def N3_inter(x:Solution, data:Sub_data, entry = [-1,-1,[-1,-1],[[-1,-1],-1]]):
    if entry[0] == -1 or entry[1] == -1 or entry[2][0] == -1 or entry[3][0][0] == -1 or entry[3][0] == -1 :
        e = N3_inter_rand(x,entry)
    else:
        e = copy.deepcopy(entry)
    print(entry)     
    print(e)
    xp = copy.deepcopy(x)
    
    if e[0] == -2:
        t0 = xp.sales[e[2][0]]
        t1 = xp.sales[e[2][1]]
        x.sales[e[2][0]].print_tournee()
        x.sales[e[2][1]].print_tournee()

        seq = t0.order[e[3][0][0]:e[3][0][1]]
        for i in range(e[3][0][1]-e[3][0][0]):
            t0.del_point(seq)
        t1.insert_seq_or_opt(list(reversed(seq)),e[3][1])

        deleted = xp.sales[e[2][0]].size == 0
        if deleted:
            xp.sales.pop(e[2][0])
        print("La tournée a été supprimée : "+str(deleted))
        
        fs= get_fs_prod_ind_qt(data.rev_d)
        t0.calc_load(fs)
        

        if not deleted:
            t0.calc_load(fs)
            t0.print_tournee()
        t1.calc_load(fs)
        t1.print_tournee()

        if(t1.load > data.Q):
            print("Insertion impossible pour points "+str(e[3])+" de tournée "+str(e[2][0])+" à "+str(e[2][1]))
            xp = x
    else:
        t0 = xp.plat[e[0]].tournees[e[1]][e[2][0]]
        t1 = xp.plat[e[0]].tournees[e[1]][e[2][1]]
        x.plat[e[0]].tournees[e[1]][e[2][0]].print_tournee()
        x.plat[e[0]].tournees[e[1]][e[2][1]].print_tournee()
        
        seq = t0.order[e[3][0][0]:e[3][0][1]]
        for i in range(e[3][0][1]-e[3][0][0]):
            t0.del_point(seq)
        t1.insert_seq_or_opt(list(reversed(seq)),e[3][1])

        #Verifiez si la tounrée 0 n'est pas vide apres avoir pris un sommet
        deleted = xp.plat[e[0]].tournee_post_del_point(e[1],e[2][0])
        print("La tournée a été supprimée : "+str(deleted))
        
        if not deleted:
            if e[1] == 0: #Tournée de collecte
                t0.calc_load(reduct_LnfPT(xp.plat[e[0]].Lfptn,data.C))
            else: #Tournée de livraison
                t0.load = sum(get_sum_qt_c_l_by_d(data.d, t0.order,data.F))
            # t0.print_tournee()
        if e[1] == 0: #Tournée de collecte
            t1.calc_load(reduct_LnfPT(xp.plat[e[0]].Lfptn,data.C))
        else: #Tournée de livraison
            t1.load = sum(get_sum_qt_c_l_by_d(data.d, t1.order,data.F))
        # t1.print_tournee()
        
        
        if t1.load > data.Q:
            print("Insertion impossible pour points "+str(e[3])+" de tournée "+str(e[2][0])+" à "+str(e[2][1]))
            xp = x

    return xp

#INVERSE OR_OPT intra_tournee
#entry = paramètre permettant de séléctionner 
# [
#   index_plat : -2 pour tournées sale, 0 à nb plateforme
#   index_type_tournee : 0 pour sales, 1 pour propre
#   index_tournee : (0 à nb de tournee de tel type, 0 à nb de tournee de tel type)
#   indexes_affect : ([index_debut seq, index_fin seq], index où inserer seq dans t2)
# ]
# (Utilise le même générateur que pour N3_intra parce que même structure)
def N4_intra(x:Solution, data:Sub_data, entry = [-1,-1,-1,[[-1,-1],-1]]):
    if entry[0] == -1 or entry[1] == -1 or entry[2] == -1 or entry[3][0][0] == -1 or entry[3][0] == -1 :
        e = N3_intra_rand(x,entry)
    else:
        e = copy.deepcopy(entry)
    # print(entry)     
    # print(e)

    xp = copy.deepcopy(x)
    if e[0] == -2:
        t0 = xp.sales[e[2]]
        t0.inverse_or_opt(e[3][0], e[3][1])
        # x.sales[e[2]].print_tournee()
        # t0.print_tournee()
    else:
        t0 = xp.plat[e[0]].tournees[e[1]][e[2]]
        t0.inverse_or_opt(e[3][0], e[3][1])
        # x.plat[e[0]].tournees[e[1]][e[2]].print_tournee()
        # t0.print_tournee()
    return xp

#INVERSE OR_OPT inter_tournee
#entry = paramètre permettant de séléctionner 
# [
#   index_plat : -2 pour tournées sale, 0 à nb plateforme
#   index_type_tournee : 0 pour sales, 1 pour propre
#   index_tournee : (0 à nb de tournee de tel type, 0 à nb de tournee de tel type)
#   indexes_affect : ([index_debut seq, index_fin seq], index où inserer seq dans t2)
# ]
def N4_inter(x:Solution, data:Sub_data, entry = [-1,-1,[-1,-1],[[-1,-1],-1]]):
    if entry[0] == -1 or entry[1] == -1 or entry[2][0] == -1 or entry[3][0][0] == -1 or entry[3][0] == -1 :
        e = N3_inter_rand(x,entry)
    else:
        e = copy.deepcopy(entry)
    print(entry)     
    print(e)
    xp = copy.deepcopy(x)
    
    if e[0] == -2:
        t0 = xp.sales[e[2][0]]
        t1 = xp.sales[e[2][1]]
        # x.sales[e[2][0]].print_tournee()
        # x.sales[e[2][1]].print_tournee()

        seq = t0.order[e[3][0][0]:e[3][0][1]]
        for i in range(e[3][0][1]-e[3][0][0]):
            t0.del_point(seq)
        t1.insert_seq_or_opt(list(reversed(seq)),e[3][1])

        deleted = xp.sales[e[2][0]].size == 0
        if deleted:
            xp.sales.pop(e[2][0])
        # print("La tournée a été supprimée : "+str(deleted))
        
        fs= get_fs_prod_ind_qt(data.rev_d)
        t0.calc_load(fs)

        if not deleted:
            t0.calc_load(fs)
            # t0.print_tournee()
        t1.calc_load(fs)
        # t1.print_tournee()

        if(t1.load > data.Q):
            # print("Insertion impossible pour points "+str(e[3])+" de tournée "+str(e[2][0])+" à "+str(e[2][1]))
            xp = x
    else:
        t0 = xp.plat[e[0]].tournees[e[1]][e[2][0]]
        t1 = xp.plat[e[0]].tournees[e[1]][e[2][1]]
        # x.plat[e[0]].tournees[e[1]][e[2][0]].print_tournee()
        # x.plat[e[0]].tournees[e[1]][e[2][1]].print_tournee()
        
        seq = t0.order[e[3][0][0]:e[3][0][1]]

        for i in range(e[3][0][1]-e[3][0][0]):
            t0.del_point(seq)
        t1.insert_seq_or_opt(list(reversed(seq)),e[3][1])

        #Verifiez si la tounrée 0 n'est pas vide apres avoir pris un sommet
        deleted = xp.plat[e[0]].tournee_post_del_point(e[1],e[2][0])
        print("La tournée a été supprimée : "+str(deleted))
        
        if not deleted:
            if e[1] == 0: #Tournée de collecte
                t0.calc_load(reduct_LnfPT(xp.plat[e[0]].Lfptn,data.C))
            else: #Tournée de livraison
                t0.load = sum(get_sum_qt_c_l_by_d(data.d, t0.order,data.F))
            # t0.print_tournee()
        if e[1] == 0: #Tournée de collecte
            t1.calc_load(reduct_LnfPT(xp.plat[e[0]].Lfptn,data.C))
        else: #Tournée de livraison
            t1.load = sum(get_sum_qt_c_l_by_d(data.d, t1.order,data.F))
        # t1.print_tournee()
        
        
        if t1.load > data.Q:
            print("Insertion impossible pour points "+str(e[3])+" de tournée "+str(e[2][0])+" à "+str(e[2][1]))
            xp = x

    return xp

#DEL PLATFORME
#entry = paramètre permettant de séléctionner 
# [
#   index_plat_a_ouvrir : index de plat ouverte,
# ]
def N5_Add(x:Solution, data:Sub_data, entry = [-1]):
    if entry[0] == -1:
        e = N5_add_rand(x,data.N,entry)
    else:
        e = copy.deepcopy(entry)
    xp = copy.deepcopy(x)
    xp.plat.append(Plateforme(e[0]))

    return xp

#DEL PLATFORME
#entry = paramètre permettant de séléctionner 
# [
#   index_plat_a_fermer : emplacement dans x.plat à pop,
# ]
def N5_Del(x:Solution, data:Sub_data, entry = [-1]):
    if entry[0] == -1:
        e = N5_del_rand(x,data.N,entry)
    else:
        e = copy.deepcopy(entry)
    
    # print(entry)
    # print(e)
    
    xp = copy.deepcopy(x)
    # print("pré del")

    xp.plat.pop(e[0])
    # print("post del")

    xp.repair_solution_post_N6(data)

    # xp.print_plateforme(e[0])

    #xp.print_all_plateformes()
    
    return xp

#SWAP PLATFORME
#entry = paramètre permettant de séléctionner 
# [
#   index_plat_a_fermer : index de plat ouverte,
#   index_plat_a_ouvrir : 0 à numéro de plat à ouvrir,
# ]

def N5_Swap(x:Solution, data:Sub_data, entry = [-1,-1]):
    if entry[0] == -1 or entry[1] == -1:
        e = N5_swap_rand(x,data.N,entry)
    else:
        e = copy.deepcopy(entry)
    xp = copy.deepcopy(x)
    xp.plat[e[0]].set_numero(e[1])

    return xp

#REAFFECTATION CLIENT
#entry = paramètre
# [
#   numero_client à réaffecter
#   numero_plat où réaffecter client
# ]
def N6_one(x:Solution, data:Sub_data, entry = [-1,-1]):
    if entry[0] == -1 or entry[1] == -1:
        e = N6_one_rand(x,data.C,data.N,entry)
    else:
        e = copy.deepcopy(entry)

    # print(entry)
    # print(e)

    xp = copy.deepcopy(x)

    found = False
    i = 0
    
    while not found and i < len(x.plat):
        if e[0] in x.plat[i].cli_affect:
            found = True
        else:
            i += 1

    xp.plat[i].cli_affect.remove(e[0])
    xp.plat[e[1]].add_client(data.d,e[0])

    xp.plat[i].calc_LnfPT_c(data.d, data.C,data.F,data.T,data.T,data.Q)
    xp.plat[i].repair(data)
    if i != e[1]:
        xp.plat[e[1]].calc_LnfPT_c(data.d, data.C,data.F,data.T,data.T,data.Q)
        xp.plat[e[1]].repair(data)

    return xp

#REAFFECTATION LISTE DE CLIENTS
#entry = paramètre
# [
#   [liste de numero_client à réaffecter]
#   [liste où réaffecter num_cli dans premier paramètre]
# # ]
def N6_some(x:Solution, data:Sub_data, entry = [[-1],[-1]]):
    if entry[0] == [-1] or entry[1] == [-1]:
        e = N6_some_rand(x,data.C,data.N,entry)
    else:
        e = copy.deepcopy(entry)
    # print(entry)
    # print(e)
    
    xp = copy.deepcopy(x)

    for s in range(len(entry[0])):
        found = False
        i = 0
<<<<<<< HEAD
=======
        
>>>>>>> a4f7297064ed4200e59a1258fa8d7b653fb79185
        while not found and i < len(x.plat):
            if e[0][s] in xp.plat[i].cli_affect:
                found = True
            else:
                i += 1

        if found:
            xp.plat[i].cli_affect.remove(e[0][s])   
            xp.plat[i].calc_LnfPT_c(data.d, data.C,data.F,data.T,data.T,data.Q)

        xp.plat[e[1][s]].add_client(data.d,e[0][s])

    #xp.print_all_plateformes()
    xp.repair_solution_post_N6(data)

    return xp

#REAFFECTATION ALEATOIRE DE TOUS LES CLIENTS
def N6_all(x:Solution, data:Sub_data):
    xp = copy.deepcopy(x)

    for p in xp.plat:
        p.cli_affect.clear()
        p.pt_affect.clear()
        p.tournees[0].clear()
        p.tournees[1].clear()

    xp.repair_solution_post_N6(data)


    return xp