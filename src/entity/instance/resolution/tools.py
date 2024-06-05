import numpy as np

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

#Déterminer la quantité de produits propres à collecter sur un point de collecte
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

#Récupère les producteurs à visiter pour un client
def get_p_c_by_d(d:dict, c:int):
    #print(list(d[c].keys()))
    for i in d[c].keys():
        for value in d[c][i]:
            if value[1] <= 0:
                
                print("Erreur : commande sans quantités, c = "+str(c)+", p = "+str(i)+"d[c][p] = "+str(value))
    return(list(d[c].keys()))

#Récupère les clients à visiter pour le producteur (debug)
def get_c_p_by_rev_d(rev_d:dict, p:int):
    return(list(rev_d[p].keys()))

#Recupère tous les clients affectés à une plateforme
def get_wc_by_n(wc:list, n:int):
    return(list(i for i,j in enumerate(wc) if j == 1))
