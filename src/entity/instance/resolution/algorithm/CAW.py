from ..struct.tournee import Tournee
import numpy as np

def CAW_F(c:list, Q:float, dep:int ,indexes:list, Q_ind:list):
    #initialisation des tournées
    r = list[Tournee]()
    for i in range(len(indexes)):
        r.append(Tournee(dep))
        r[i].add_point([indexes[i]],[Q_ind[i]])

    stop = False
    
    #Debut de l'algorithme
    while not stop:
        stop = True
        #calcul des savings
        S = []
        i_S = []
        for i in range(len(r)-1):
            for j in range(i+1,len(r)):
                S.append(c[r[i].origin][r[i].order[-1]] + c[r[j].origin][r[j].order[-1]] - c[r[i].order[-1]][r[j].order[-1]])
                i_S.append((i,j))
        
        order_i_S = sorted(range(len(S)), key=lambda k: S[k], reverse=True)
        
        b = False
        i = 0
        #Trouver le saving le plus profitable et possible (vérification de capacité)
        while not b and i < len(order_i_S):
            b = False
            r1 = r[i_S[order_i_S[i]][0]]
            r2 = r[i_S[order_i_S[i]][1]]
            if(r1.load + r2.load <= Q):
                b = True
            else:
                i+= 1

        #Il y a eu une modification, on continue d'essayer, sinon on arrête l'algorithme
        if b :
            stop = False
            temp_sub_Q = []
            for sommet in r2.order:
                temp_sub_Q.append(Q_ind[indexes.index(sommet)])
            r1.add_point(r2.order, temp_sub_Q)
            r.pop(i_S[order_i_S[i]][1])      

    return r