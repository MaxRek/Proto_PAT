import numpy as np
from src.entity.instance import *


def sub_matrix(M : list, indexes : list):
    len_ind = len(indexes)
    new_M = np.zeros((len_ind,len_ind)).tolist()
    for i in range(len_ind):
        for j in range(len_ind):
            new_M[i][j] = M[indexes[i]][indexes[j]]

    return new_M

#Suite de fonctions utilisés pour le calcul

#qt = quantités
#p = producteur
#f = filière de produit
#c = client
#n = plateforme

#d = donnée D_{p,f}^n => "c" -> "p" -> "f,qt"
#rev_d = donnée crée : "p" -> "c",("f,qt")

#Récupère toutes les quantités envoyées par un producteur p
def get_sum_qt_p_by_d(d:dict, p:int, f:int):
    sum = np.zeros(f).tolist()
    for key in d.keys():
        if p in d[key].keys():
            for values in d[key][p]:
                sum[values[0]] += values[1]
    return sum

#Retourne les quantités à récupérer chez un producteur au total
def get_sum_qt_p_by_rev_d(rev_d:dict, p:int, f:int):
    sum = np.zeros(f).tolist()
    
    for key in rev_d[p].keys():
        for values in rev_d[p][key]:#print(rev_d[p][i][1][0])
            sum[values[0]] += values[1]

    return sum

#Récupère toutes les quantités demandés par un client c
def get_sum_qt_c_by_d(d:dict, c:int, f:int):
    sum = np.zeros(f).tolist()
    for key in d[c]:
        for values in d[c][key]:
            sum[values[0]] += values[1]
    return sum

#Récupère toutes les quantités demandés par une liste de client c_ml
def get_sum_qt_c_l_by_d(d:dict, c_l:list, f:int):
    Qts = np.zeros(len(c_l)).tolist()
    for i in range(len(c_l)):
        Qts[i] = sum(get_sum_qt_c_by_d(d,c_l[i],f)) 
    return Qts

#Calcul les quantités à récupérer chez les différents dépôts de produits propres 
#(producteurs/transformateur) pour la liste de clients c_l
#Indique aussi si il faut aller voir le transformateur
# def calc_LnfPT_c(d:dict, c_l:list, C:int, pt:int,f:int):
#     LnfPT = np.zeros((pt,f)).tolist()
#     sum_fs = 0
#     for c in c_l:
#         for prod in d[c].keys():
#             for value in d[c][prod]:
#                 if value[0] == 0:
#                     sum_fs += value[1]
#                 else:
#                     LnfPT[prod-C][value[0]] += value[1]
#     t = 0
#     if sum_fs > 0:
#         LnfPT[-1][0] = sum_fs
#         t = 1
#     return (LnfPT, t)

#Calcul les quantités à récupérer chez les différents dépôts de produits propres 
#(producteurs/transformateur) pour la liste de clients c_l
#Indique aussi si il faut aller voir le transformateur
def calc_LnfPT_c(d:dict, c_l:list, C:int, pt:int,f:int):
    LnfPT = np.zeros((pt,f)).tolist()
    sum_fs = 0
    for c in c_l:
        for prod in d[c].keys():
            for value in d[c][prod]:
                if value[0] == 0:
                    sum_fs += value[1]
                else:
                    LnfPT[prod-C][value[0]] += value[1]
    t = 0
    if sum_fs > 0:
        LnfPT[-1][0] = sum_fs
        t = 1
    return (LnfPT, t)

#Reduire LnfPT selon les producteurs à visiter, et les quantités propres associées
def reduct_LnfPT(Lfptn:list, C:int):
    indexes = []
    qts = []
    for i in range(len(Lfptn)):
        sum_prod = sum(Lfptn[i])
        if sum_prod > 0:
            indexes.append(i+C)
            qts.append(sum_prod)
    return(indexes, qts)
            
#Verifie qu'un point de récolte ne dépasse pas la capacité Q des véhicules
def verif_LnfPT(LnfPT:list, Q:int):
    b = True
    i = 0
    #print(len(LnfPT))
    while b and i < len(LnfPT):
        j = 0
        #print(len(LnfPT[i]))
        while b and j < len(LnfPT[i]):
            if LnfPT[i][j] > Q:
                b = False
            j += 1
        i += 1
    return b

#Additionne deux listes de quantités à récupérer LnfPT
def add_LnfPT(L1:list, L2:list):
    l_r = []
    if len(L1) == len(L2):
        if len(L1[0]) == len(L2[0]):
            for i in range(len(L1)):
                l_r.append([])
                for j in range(len(L1[0])):
                    l_r[i].append(L1[i][j] + L2[i][j])
    else:
        print("Erreur de taille entre L1 et L2")
        
    return l_r

#Déterminer la quantité de produits propres à collecter 
#pour une plateforme aux points de collecte (retiens les sommets où récupérer)
def cumul_qt_PT_by_LnfPT(LnfPT:list):
    qt_PT = np.zeros(len(LnfPT)).tolist()
    indexes_pt = []
    for pt in range(len(LnfPT)):
        for f in range(len(LnfPT[pt])):
            qt_PT[pt] += LnfPT[pt][f]
            if(f == len(LnfPT[pt])-1):
                if qt_PT[pt] > 0:
                    indexes_pt.append(pt)
    return (qt_PT,indexes_pt)


#Retourne la somme des produits sales à récupérer au total (pour transformateur)
def get_sum_qt_fs(rev_d:dict):
    sum_fs = 0
    for key in rev_d.keys():
        for key2 in rev_d[key].keys():
            for values in rev_d[key][key2]:
                if(values[0] == 0):
                    #print(j[1][0][1])
                    sum_fs += values[1]
    return sum_fs

#Retourne les indices de producteurs et la quantité de produits sales associées à récupérer pour le transformateur
def get_fs_prod_ind_qt(rev_d:dict):
    indexes = []
    qt = []
    for prod in rev_d.keys():
        sum_qt = 0
        for cli in rev_d[prod].keys():
            for values in rev_d[prod][cli]:
                if values[0] == 0:
                    sum_qt += values[1]
        if sum_qt > 0:
            indexes.append(prod)
            qt.append(sum_qt)
    return (indexes, qt)


#Récupère les producteurs à visiter pour un client
def get_p_c_by_d(d:dict, c:int):
    #print(list(d[c].keys()))
    for i in d[c].keys():
        for value in d[c][i]:
            if value[1] <= 0:
                print("Erreur : commande sans quantités, c = "+str(c)+", p = "+str(i)+"d[c][p] = "+str(value))
    return(list(d[c].keys()))

#Récupère les producteurs à visiter pour une liste de client
def get_p_cl_by_d(d:dict, cl:list):
    p_l = []
    for c in cl:
        temp = get_p_c_by_d(d,c)
        for p in temp:
            if p not in p_l:
                #bisect.insort(p_l, p)
                p_l.append(p)
    return p_l

#Récupère les clients à visiter pour le producteur (debug)
def get_c_p_by_rev_d(rev_d:dict, p:int):
    return(list(rev_d[p].keys()))

#Recupère tous les clients affectés à une plateforme
def get_wc_by_n(wc:list, n:int):
    return(list(i for i,j in enumerate(wc) if j == 1))

#Modifier un dict décrivant une solution en indices lors de résolution en solution avec indices post resolution
def updating_solution_to_instance(d_s : dict, indexes_resolution:list, data):

    for d_t in d_s["sales"]:
        d_t = updating_tournee(d_t, data.C, indexes_resolution[1],data.T-1)

    for d_p in d_s["plateformes"]:
        d_p = updating_plateforme(d_p, indexes_resolution, data.C,data.P,data.T-1)
    return d_s

def updating_tournee(d_t : dict, base:int, indices:list, T:int):
    for sommet in range(len(d_t["order"])): 
        if(d_t["order"][sommet]==T):
            d_t["order"][sommet] = "T"
        else:
            d_t["order"][sommet] = indices[d_t["order"][sommet]-base]
    return d_t

def updating_plateforme(d_p : dict, indices:list, base_c :int, base_pt : int, T:int):
    for c in range(len(d_p["cli_affect"])):
        d_p["cli_affect"][c] = indices[0][d_p["cli_affect"][c]-base_c]
    for p in range(len(d_p["pt_affect"])):
        if d_p["pt_affect"][p] == T:
            d_p["pt_affect"][p] = "T"
        else:
            d_p["pt_affect"][p] = indices[1][d_p["pt_affect"][p]-base_pt]
    for d_t in d_p["tournees"][0]:
        d_t = updating_tournee(d_t, base_pt, indices[1],T)
    for d_t in d_p["tournees"][1]:
        d_t = updating_tournee(d_t, base_c, indices[0],T)
        
def translate_solution(d_s:dict, df):
    for d_t in d_s["sales"]:
        d_t = translate_tournee(d_t, df.F, df.T)
    for d_p in d_s["plateformes"]:
        d_p = translate_plateforme(d_p, df.N, df.E, df.F, df.T)
    return d_s

def translate_tournee(d_t : dict, df_type,T):
    if "Nom de la structure" in df_type.columns:
        name = "Nom de la structure"
    else:
        name = "Nom"
    for sommet in range(len(d_t["order"])): 
        if(d_t["order"][sommet]=="T"):
            d_t["order"][sommet] = T.iloc[0]["Nom de la structure"]
        else:
            d_t["order"][sommet] = df_type.iloc[d_t["order"][sommet]][name]
    return d_t

def translate_plateforme(d_p : dict, df_N, df_E, df_F, df_T):
    d_p["numero"] = df_N.loc[d_p["numero"]]["Nom de la structure"]
    for d_t in d_p["tournees"][0]:
        d_t = translate_tournee(d_t, df_F, df_T)
    for d_t in d_p["tournees"][1]:
        d_t = translate_tournee(d_t, df_E, df_T)
    return d_p

def dict_solution_to_txt(d_s:dict):
    str_s = "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"
    str_s += "Tournees de collecte sale : \n"
    for d_t in d_s["sales"]:
        str_s += dict_tournee_to_txt(d_t, 3)
    str_s += "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"
    str_s += "Plateformes : \n"
    for d_p in d_s["plateformes"]:
        str_s += dict_plateforme_to_txt(d_p, 3)
    return str_s

def dict_plateforme_to_txt(d_p:dict, indent:int):
    str_p = ""
    str_p += indent*" " + "- Plateforme "+str(d_p["numero"])+" avec "+str(d_p["xT"])+" trajet(s) directe(s) avec le transformateur, \n"
    str_p += indent*" " + "   Clients affectes : "+str(d_p["cli_affect"])+"\n"
    str_p += indent*" " + "   Points de prod visites : "+str(d_p["pt_affect"])+"\n"
    str_p += indent*" " + "   Tournees de collecte (propres): \n"
    for d_t in d_p["tournees"][0]:
        str_p += dict_tournee_to_txt(d_t, indent + 5)
    str_p += indent*" " + "   Tournees de livraison: \n"
    for d_t in d_p["tournees"][1]:
        str_p += dict_tournee_to_txt(d_t, indent + 5)
    return str_p

def dict_tournee_to_txt(d_t:dict, indent:int):
    return indent*" " + "- Qt transportee : "+str(d_t["load"])+", "+str(d_t["size"])+" points visites : "+str(d_t["order"])+"\n"
