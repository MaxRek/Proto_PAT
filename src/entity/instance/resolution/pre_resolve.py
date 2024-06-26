from ..instance import Instance
from ..instance import Dec
from .struct.sub_data import Sub_data
from.tools import sub_matrix

import numpy as np

def reduction(inst:Instance):
    indexes_loc = [[],[]]
    sub_tsp = []

    #Récupération des clients ayant passé commande
    indexes_loc[0] = list(inst.data.d.keys())

    for i in range(len(indexes_loc[0])):
        indexes_loc[0][i] = int(indexes_loc[0][i])

    #Récupération des producteurs qui ont au moins une commande
    for i in range(len(indexes_loc[0])):
        for j in inst.data.d[i].keys():
            #print(j)
            if(j not in indexes_loc[1]):
                indexes_loc[1].append(int(j))
                #print(inst.data.d[i][j])
                for f in inst.data.d[i][j]:
                    if f[0] == 0:
                        sub_tsp.append(j)
           # for f in range(len(inst.data.d[i][j])):
    indexes_loc[0] = sorted(indexes_loc[0])
    indexes_loc[1] = sorted(indexes_loc[1])
    # print(indexes_loc)
    # print(sub_tsp)


    #Adaptation de D pour ne récupérer que les clients des producteurs visités
    #D_{p,c}
    sub_D = np.zeros((len(indexes_loc[1]),len(indexes_loc[0])),dtype=int).tolist()
    for i in range(len(indexes_loc[0])):
        for j in range(len(indexes_loc[1])):#print(j)
            if(j in inst.data.d[i].keys()):
                sub_D[j][i] = 1

    #Modif de d pour refléter nouveau indices
    new_d = {}
    for i in inst.data.d.keys():
        i_c = i + inst.data.N
        new_d[i_c] = {}
        for j in inst.data.d[i].keys():
            j_c = inst.data.N+len(indexes_loc[0]) + indexes_loc[1].index(j)
            new_d[i_c][j_c] = []
            for k in inst.data.d[i][j]:
                new_d[i_c][j_c].append(k)
    
    #print(new_d)

    #adaptation de c pour réduire la matrice de coût uniquement à ceux qui nous intéressent
    #c_{i,j} 

    #Rassemblement des indexes
    sum_ind = list(range(inst.data.N))
    for i in indexes_loc[0]:
        sum_ind.append(i+inst.data.N)
    for i in indexes_loc[1]:
        sum_ind.append(i+inst.data.N+inst.data.C)
    
    sum_ind.append(inst.data.N+inst.data.C+inst.data.P)

    #print(str(len(inst.data.c)) + " "+ str(len(inst.data.c[0])))
    sub_c = sub_matrix(inst.data.c, sum_ind)
    #print(str(len(sub_c)) + " "+ str(len(sub_c)))
    

    sdata = Sub_data(inst.data.N,len(indexes_loc[0]),len(indexes_loc[1]),inst.data.F,sub_tsp, inst.data.Q, inst.data.O, sub_D, new_d, sub_c, indexes_loc, inst.data.df)
    sdec = Dec(len(indexes_loc[0]),inst.data.N,len(indexes_loc[1]), 1, inst.data.F, inst.data.K)

    # for i in i.data.d.keys():
    #     if 
    #     for j in i:

    return sdata, sdec


def old_check_before_resolve(i : Instance, v:bool = False ):
    b = True
    #Vérification des données en premier
    if i.data.df.E.shape[0]!=i.data.C or i.data.df.F.shape[0]!=i.data.P or i.data.df.N.shape[0]!=i.data.N or i.data.df.T.shape[0]!=i.data.T:
        print("len(E) ("+str(i.data.df.E.shape[0])+") != C ("+str(i.data.C)+"), len(F) ("+str(i.data.df.F.shape[0])+") != P ("+str(i.data.P)+"),len(N) ("+str(i.data.df.N.shape[0])+") != N ("+str(i.data.N)+"), len(T) ("+str(i.data.df.T.shape[0])+") != N ("+str(i.data.T)+")")
        b = False
    verif_p_t = True
    #Vérification des produtis enregistrés
    if i.data.F != i.data.Fs+i.data.Fp:
        print("F ("+str(i.data.F)+") != Fs ("+str(i.data.Fs)+") + Fp ("+str(i.data.Fp)+")")
        b = False
        verif_p_t = False
        print("Verif des rations de transformations impossibles")
    #Verification des couts d'ouvertures (sauf leur prix)
    if len(i.data.O) != i.data.N:
        print("len(O) ("+str(len(i.data.O))+") != N ("+str(i.data.N)+")")
    
    #Verification des demandes
    sum_d_prod = np.zeros(i.data.F)
    sum_d_fs = np.zeros(i.data.Fs)
    verif_d_prod = True

    #Verification que tous les clients ont au moins une commande
    if len(list(i.data.d).keys()) != i.data.C:
        print("len(d) ("+str(len(list(i.data.d).keys()))+") != C ("+str(i.data.C)+")")
        b = False
        verif_d_prod = False
        print("Verifications des quantités impossibles à partir des clients")
    else:
        #Verification qu'il n'y a pas de commandes impossibles
        for key in i.data.d.keys() :
            #Le client existe-il ?
            if key not in range(i.data.C):
                b = False
                verif_d_prod = False
                print("Client n"+str(key)+" n'existe pas (C = "+str(i.data.C+")"))
            else: 
                for key2 in i.data.d[key]:
                    #Le producteur existe-il ?
                    if key2 not in range(i.data):
                        print("Prod n"+str(key2)+" n'existe pas (P = "+str(i.data.P+")"))

                    # else:

                    # for values in i.data.d.
        for j in range(len(i.data.C)):
            if(range(len(i.data.d[j])))!=i.data.F:
                print("len(d["+str(j)+"]) ("+str(len(i.data.d[j]))+") != F ("+str(i.data.F)+")")
                b = False
                verif_d_prod = False
            if verif_d_prod:
                sum_d_client = 0
                for k in range(len(i.data.F)):
                    sum_d_prod[k] += i.data.d[j][k]
                    sum_d_client += i.data.d[j][k] 
                if k < i.data.Fs:
                    sum_d_fs[j] += i.data.d[j][k]
                if sum_d_client > i.data.Q:
                    print("sum(d_c) ("+str(sum_d_client)+") > Q ("+str(i.data.Q)+") : client ne pouvant être livré qu'une seule fois")
        if not verif_d_prod:
            print("Verifications des quantités impossibles à partir des clients")

    #Verification des Stocks
    sum_p_prod = 0
    count_p_prod = np.zeros(i.data.F)
    sum_p_fs = np.zeros(i.data.Fs)
    sum_p_fp = 0
    verif_p_prod = True
    if len(i.data.S) != i.data.P:
        print("len(S) ("+str(len(i.data.S))+") != P ("+str(i.data.P)+")")
        b = False
        verif_p_prod = False
    else:
        for j in range(i.data.P):
            if(len(i.data.S[j]))!=i.data.F:
                print("len(S["+str(j)+"]) ("+str(len(i.data.S[j]))+") != F ("+str(i.data.F)+")")
                b = False
                verif_p_prod = False
            if verif_p_prod:
                for k in range(i.data.F):
                    if i.data.S[j][k] > 0:
                        count_p_prod += 1
                        if k < i.data.Fs:
                            sum_p_fs[k] += i.data.d[j][k]
                        else:
                            sum_p_fp += i.data.d[j][k]     
        if not verif_p_prod:
            print("Verifications des quantités impossibles à partir des producteurs")
   
    
    A = i.data.C+i.data.N+i.data.P
    if len(i.data.c) != A:
        print("len(c) ("+str(len(i.data.c))+") != C+N+P ("+str(i.data.C)+","+str(i.data.N)+","+str(i.data.P)+")")
        b = False
    else:
        for j in range(A):
            if len(i.data.c[j]) != A:
                print("len(d[("+str(j)+")]) ("+str(len(i.data.c[j]))+") != C+N+P ("+str(i.data.C)+","+str(i.data.N)+","+str(i.data.P)+")")
                b = False
            else:
                if i.data.c[j][j] != 0:
                    print("c["+str(j)+"]["+str(j)+"] != 0 ("+str(i.data.c[j][j])+")")
                    b = False
                for k in range(A):
                    if j != k:
                        if(i.data.c[j][k] <= 0):
                            print("c["+str(j)+"]["+str(k)+"] <= 0 ("+str(i.data.c[j][k])+") : boucle possible/doublons possibles")
                            b = False

    #Verification des transformations
    if len(i.data.t) != i.data.N:
        print("len(t) ("+str(len(i.data.t))+") != N ("+str(i.data.N)+")")
        b = False
    else:
        for j in range(i.data.N):
            if len(i.data.t[j]) != i.data.Fs:
                print("len(t["+str(j)+"]) ("+str(len(i.data.t[j]))+")!= Fp ("+str(i.data.Fs)+")")
                b = False
            else:
                for k in range(i.data.Fs):
                    if(i.data.t[j][k] < 0 and i.data.t[j][k]>1 ):
                        print("t["+str(j)+"]["+str(k)+"] >1 ou <0 ("+str(i.data.t[j][k])+") : impossible de transformer négativement/transformer pour plus lourd")
                        b = False

        if verif_d_prod and verif_p_prod and verif_p_t:
            for j in range(len(i.data.F)):
                if sum_d_prod[j] > sum_p_prod[j]:
                    print("sum_d_prod[("+str(j)+")] ("+str(sum_d_prod[j])+") > sum_p_prod[("+str(j)+")] ("+str(sum_p_prod[j])+") : Demande supérieur à l'offre")
                    b = False
                else:
                    #Verif de K
                    K_min = 0
                    #Tous les produits propres livrés divisés par Q:
                    K_min += math.ceil(sum_d_prod/i.data.Q)
                    #Tous les produits sales collectés pour transformation/Q (selon ratio + transport individuel)
                    for k in range(i.data.Fs):
                        K_min += math.ceil((1/i.data.t[k])*sum_p_fs[k]/i.data.Q)
                    #Tous les produits propres collectés/Q
                    K_min += math.ceil(sum_p_fp/i.data.Q)
            if i.data.K < K_min:
                print("K_min ("+str(K_min)+") > K ("+str(i.data.K)+") : nombre de livraisons minimum calculés supérieur à celle indiqué, K = K_min (potentillement insuffisant)")
                i.data.K = K_min
    # #Verification Dec
    # K = i.data.K
    # if len(i.Dec.xnc) != K:
    #     print("len(xnc["+str(len(i.Dec.xnc))+"]) != k ("+str(K)+")")
    # else:
    #     for j in range(len(K)):

    return b