from ..struct.tournee import Tournee
import numpy as np

def CAW_F(c:list, Q:float, dep:int ,indexes:list, Q_ind:list):
    #initialisation des tournées
    r = list[Tournee]()
    for i in range(len(indexes)):
        r.append(Tournee(dep))
        r[i].add_point([indexes[i]],[Q_ind[i]])
        #.add_point([indexes[i]],[Q_ind[i]])
        #r[i].print_tournee()

    # print(dep)
    # print(indexes)

    #tant que chaque sommet n'est pas affectée
    stop = False    
    while not stop:
        stop = True
        S = []
        i_S = []

        for i in range(len(r)-1):
            for j in range(i+1,len(r)):
                # print(str(i) + " " +str(j) + " " + str(r[i].order[-1]) + " " + str(r[j].order[-1]) + " "  + str(c[r[i].origin][r[i].order[-1]+1]) + " " + str(c[r[j].origin][r[j].order[-1]+1]) + " " + str(c[r[i].order[-1]+1][r[j].order[-1]+1]))
                S.append(c[r[i].origin][r[i].order[-1]] + c[r[j].origin][r[j].order[-1]] - c[r[i].order[-1]][r[j].order[-1]])
                i_S.append((i,j))

        order_i_S = sorted(range(len(S)), key=lambda k: S[k], reverse=True)
        # print(order_i_S)
        b = False
        i = 0
        while not b and i < len(order_i_S):
            b = False
            # print(i_S)

            # print(indexes)
            # print(i)       
            # print(order_i_S)
            # print(order_i_S[i])
            # print(i_S[order_i_S[i]])
            

            # print(len(r))
            r1 = r[i_S[order_i_S[i]][0]]
            r2 = r[i_S[order_i_S[i]][1]]
            if(r1.load + r2.load <= Q):
                b = True
            else:
                i+= 1

        if b :
            stop = False
            temp_sub_Q = []
            for sommet in r2.order:
                temp_sub_Q.append(Q_ind[indexes.index(sommet)])
            r1.add_point(r2.order, temp_sub_Q)
            r.pop(i_S[order_i_S[i]][1])
        # else:
        #     print("pas de changement, fin d'algo")

    # for m in range(len(r)):
    #     r[m].print_tournee()

    return r

    