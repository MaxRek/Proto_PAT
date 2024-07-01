import random as rd
from..struct.solution import Solution
from..struct.sub_data import Sub_data

#entry = paramètre permettant de séléctionner 
# [
#   index_plat : -1 pour tournées sale, 0 à nb plateforme
#   index_type_tournee : 0 pour sales, 1 pour propre
#   index_tournee : 0 à nb de tournee de tel type
#   indexes_affect : (index_sommet à insérer, index_insertion du sommet)
# ]
def N1_intra_rand(x:Solution, entry:list):
    e = [-2,-2,-2,[-2,-2]]
    if entry[0] == -2:
        i = rd.randint(0,len(x.plat))
        if i == 0:
            e[0] = -1
        else:
            e[0] = i-1
    else:
        e[0] = entry[0]

    # print("---------------------------------------------")
    # if e[0] != -1:
    #     print("Plateforme numero " + str(x.plat[e[0]].numero)+ " choisi, "+str(len(x.plat[e[0]].tournees[0]))+" tournées de collecte, "+str(len(x.plat[e[0]].tournees[1]))+" tournées de livraison")
    # else:
    #     print("Transformateur choisi, "+str(len(x.sales))+" tournées de collecte")
    # print("---------------------------------------------")

    #si index_type_tournée non déterminé, affectation aléatoire entre 0 pour collecte et 1 pour livraison
    #si index_plat = Transformateur, 0 assigné
    if entry[1] == -2:
        if e[0] == -1:
            e[1] = 0
        else:
            e[1] = round(rd.random())
    else:
        e[1] = entry[1]

    #si index_tournée non déterminé, affectation à une tournée de type index_type_tournee
    if entry[2] == -2:
        if e[0] == -1:
            #Vérification cas extreme : il n'y a qu'une tournée de sales, et il n'y a qu'un seul sommet à visiter
            if len(x.sales) == 1:
                if x.sales[0].size == 1:
                    print("Erreur : il n'y a qu'une tournée d'un seul point à visiter pour le sale, algo non adapté")
                    return ValueError
            e[2] = rd.choice(list(range(len(x.sales))))
            while x.sales[e[2]].size == 1:
                e[2] = rd.choice(list(range(len(x.sales))))
        else:
            if len(x.plat[e[0]].tournees[e[1]]) == 1:
                if x.plat[e[0]].tournees[e[1]].size == 1:
                    print("Erreur : il n'y a qu'une tournée d'un seul point à visiter pour H"+str(entry[0])+" Tournée type "+str(entry[1])+" tournée numéro "+str(entry[2])+", algo non adapté")
                    return ValueError
            e[2] = rd.choice(list(range(len(x.plat[e[0]].tournees[e[1]]))))
            while x.plat[e[0]].tournees[e[1]][e[2]].size == 1:
                e[2] = rd.choice(list(range(len(x.plat[e[0]].tournees[e[1]]))))
    else:
        e[2] = entry[2]
    
    if entry[3][0] == -2:
        if e[0] == -1:
            e[3][0] = rd.choice(list(range(x.sales[e[2]].size)))
            e[3][1] = e[3][0]
            while e[3][1] == e[3][0]:
                e[3][1] = rd.choice(list(range(x.sales[e[2]].size)))
        else:
            print(x.plat[e[0]].tournees[e[1]][e[2]].size)
            e[3][0] = rd.choice(list(range(x.plat[e[0]].tournees[e[1]][e[2]].size)))
            e[3][1] = e[3][0]
            while e[3][1] == e[3][0]:
                e[3][1] = rd.choice(list(range(x.plat[e[0]].tournees[e[1]][e[2]].size)))
    else:
        e[3] = entry[3]
    return e

#entry = paramètre permettant de séléctionner 
# [
#   index_plat : -1 pour tournées sale, 0 à nb plateforme
#   index_type_tournee : 0 pour sales, 1 pour propre
#   index_tournee : (0 à nb de tournee de tel type, 0 à nb de tournee de tel type)
#   indexes_affect : (index_sommet à insérer, index_insertion du sommet)
# ]
def N1_inter_rand(x:Solution, entry:list):
    e = [-2,-2,[-2,-2],[-2,-2]]
    if entry[0] == -2:
        i = rd.randint(0,len(x.plat))
        if i == 0:
            e[0] = -1
        else:
            e[0] = i-1
    else:
        e[0] = entry[0]

    # print("___________________________________")
    # if e[0] != -1:
    #     print("Plateforme numero " + str(x.plat[e[0]].numero)+ " choisi, "+str(len(x.plat[e[0]].tournees[0]))+" tournées de collecte, "+str(len(x.plat[e[0]].tournees[1]))+" tournées de livraison")
    # else:
    #     print("Transformateur choisi, "+str(len(x.sales))+" tournées de collecte")
    # print("___________________________________")

    #si index_type_tournée non déterminé, affectation aléatoire entre 0 pour collecte et 1 pour livraison
    #si index_plat = Transformateur, 0 assigné
    if entry[1] == -2:
        if e[0] == -1:
            e[1] = 0
        else:
            e[1] = round(rd.random())
    else:
        e[1] = entry[1]

    #si index_tournée non déterminé, affectation à une tournée de type index_type_tournee
    if entry[2][0] == -2:
        if e[0] == -1:
            #Vérification cas extreme : il n'y a qu'une tournée de sales, et il n'y a qu'un seul sommet à visiter
            if len(x.sales) == 1:
                if x.sales[0].size == 1:
                    print("Erreur : il n'y a qu'une tournée d'un seul point à visiter pour le sale, algo non adapté")
                    return ValueError
            else:
                e[2][0] = rd.choice(list(range(len(x.sales))))
                e[2][1] = e[2][0]
                while e[2][1] == e[2][0]:
                    e[2][1] = rd.choice(list(range(len(x.sales))))
        else:
            if len(x.plat[e[0]].tournees[e[1]]) == 1:
                if x.plat[e[0]].tournees[e[1]].size == 1:
                    print("Erreur : il n'y a qu'une tournée d'un seul point à visiter pour H"+str(entry[0])+" Tournée type "+str(entry[1])+" tournée numéro "+str(entry[2])+", algo non adapté")
                    return ValueError
            else:
                e[2][0] = rd.choice(list(range(len(x.plat[e[0]].tournees[e[1]]))))
                e[2][1] = e[2][0]
                while e[2][1] == e[2][0]:
                    e[2][1] = rd.choice(list(range(len(x.plat[e[0]].tournees[e[1]]))))
    else:
        e[2] = entry[2]
    
    if entry[3] == -2:
        if e[0] == -1:
            e[3] = rd.choice(list(range(x.sales[e[2][0]].size)))
        else:
            e[3] = rd.choice(list(range(x.plat[e[0]].tournees[e[1]][e[2][0]].size)))
    else:
        e[3] = entry[3]
    return e

#SWAP intra_tournee
#entry = paramètre permettant de séléctionner 
# [
#   index_plat : -1 pour tournées sale, 0 à nb plateforme
#   index_type_tournee : 0 pour sales, 1 pour propre
#   index_tournee : 0 à nb de tournee de tel type
#   indexes_affect : (index_sommet à swap, index_sommet à swap)
# ]
def N2_intra_rand(x:Solution, entry:list):
    e = [-2,-2,-2,[-2,-2]]
    if entry[0] == -2:
        i = rd.randint(0,len(x.plat))
        if i == 0:
            e[0] = -1
        else:
            e[0] = i-1
    else:
        e[0] = entry[0]

    # print("---------------------------------------------")
    # if e[0] != -1:
        # print("Plateforme numero " + str(x.plat[e[0]].numero)+ " choisi, "+str(len(x.plat[e[0]].tournees[0]))+" tournées de collecte, "+str(len(x.plat[e[0]].tournees[1]))+" tournées de livraison")
    # else:
        # print("Transformateur choisi, "+str(len(x.sales))+" tournées de collecte")
    # print("---------------------------------------------")

    #si index_type_tournée non déterminé, affectation aléatoire entre 0 pour collecte et 1 pour livraison
    #si index_plat = Transformateur, 0 assigné
    if entry[1] == -2:
        if e[0] == -1:
            e[1] = 0
        else:
            e[1] = round(rd.random())
    else:
        e[1] = entry[1]

    #si index_tournée non déterminé, affectation à une tournée de type index_type_tournee
    if entry[2] == -2:
        if e[0] == -1:
            #Vérification cas extreme : il n'y a qu'une tournée de sales, et il n'y a qu'un seul sommet à visiter
            if len(x.sales) == 1:
                if x.sales[0].size == 1:
                    print("Erreur : il n'y a qu'une tournée d'un seul point à visiter pour le sale, algo non adapté")
                    return ValueError
            e[2] = rd.choice(list(range(len(x.sales))))
            while x.sales[e[2]].size == 1:
                e[2] = rd.choice(list(range(len(x.sales))))
        else:
            if len(x.plat[e[0]].tournees[e[1]]) == 1:
                if x.plat[e[0]].tournees[e[1]].size == 1:
                    print("Erreur : il n'y a qu'une tournée d'un seul point à visiter pour H"+str(entry[0])+" Tournée type "+str(entry[1])+" tournée numéro "+str(entry[2])+", algo non adapté")
                    return ValueError
            e[2] = rd.choice(list(range(len(x.plat[e[0]].tournees[e[1]]))))
            while x.plat[e[0]].tournees[e[1]][e[2]].size == 1:
                e[2] = rd.choice(list(range(len(x.plat[e[0]].tournees[e[1]]))))
    else:
        e[2] = entry[2]
    
    if entry[3][0] == -2:
        if e[0] == -1:
            e[3][0] = rd.choice(list(range(x.sales[e[2]].size)))
            e[3][1] = e[3][0]
            while e[3][1] == e[3][0]:
                e[3][1] = rd.choice(list(range(x.sales[e[2]].size)))
        else:
            e[3][0] = rd.choice(list(range(x.plat[e[0]].tournees[e[1]][e[2][0]].size)))
            e[3][1] = e[3][0]
            while e[3][1] == e[3][0]:
                e[3][1] = rd.choice(list(range(x.plat[e[0]].tournees[e[1]][e[2]].size)))
    else:
        e[3] = entry[3]
    return e

#SWAP inter_tournee
#entry = paramètre permettant de séléctionner 
# [
#   index_plat : -1 pour tournées sale, 0 à nb plateforme
#   index_type_tournee : 0 pour sales, 1 pour propre
#   index_tournee : (0 à nb de tournee de tel type,0 à nb de tournee de tel type)
#   indexes_affect : (index_sommet à swap, index_sommet à swap)
# ]

def N2_inter_rand(x:Solution, entry:list):
    e = [-2,-2,[-2,-2],[-2,-2]]
    if entry[0] == -2:
        i = rd.randint(0,len(x.plat))
        if i == 0:
            e[0] = -1
        else:
            e[0] = i-1
    else:
        e[0] = entry[0]

    # print("---------------------------------------------")
    # if e[0] != -1:
    #     print("Plateforme numero " + str(x.plat[e[0]].numero)+ " choisi, "+str(len(x.plat[e[0]].tournees[0]))+" tournées de collecte, "+str(len(x.plat[e[0]].tournees[1]))+" tournées de livraison")
    # else:
    #     print("Transformateur choisi, "+str(len(x.sales))+" tournées de collecte")
    # print("---------------------------------------------")

    #si index_type_tournée non déterminé, affectation aléatoire entre 0 pour collecte et 1 pour livraison
    #si index_plat = Transformateur, 0 assigné
    if entry[1] == -2:
        if e[0] == -1:
            e[1] = 0
        else:
            e[1] = round(rd.random())
    else:
        e[1] = entry[1]

    #si index_tournée non déterminé, affectation à une tournée de type index_type_tournee
    if entry[2][0] == -2:
        if e[0] == -1:
            #Vérification cas extreme : il n'y a qu'une tournée de sales, et il n'y a qu'un seul sommet à visiter
            if len(x.sales) == 1:
                if x.sales[0].size == 1:
                    print("Erreur : il n'y a qu'une tournée d'un seul point à visiter pour le sale, algo non adapté")
                    return ValueError
            else:
                e[2][0] = rd.choice(list(range(len(x.sales))))
                e[2][1] = e[2][0]
                while e[2][1] == e[2][0]:
                    e[2][1] = rd.choice(list(range(len(x.sales))))
        else:
            if len(x.plat[e[0]].tournees[e[1]]) == 1:
                if x.plat[e[0]].tournees[e[1]].size == 1:
                    print("Erreur : il n'y a qu'une tournée d'un seul point à visiter pour H"+str(entry[0])+" Tournée type "+str(entry[1])+" tournée numéro "+str(entry[2])+", algo non adapté")
                    return ValueError
            else:
                e[2][0] = rd.choice(list(range(len(x.plat[e[0]].tournees[e[1]]))))
                e[2][1] = e[2][0]
                while e[2][1] == e[2][0]:
                    e[2][1] = rd.choice(list(range(len(x.plat[e[0]].tournees[e[1]]))))
    else:
        e[2] = entry[2]
    
    if entry[3][0] == -2:
        if e[0] == -1:
            e[3][0] = rd.choice(list(range(x.sales[e[2][0]].size)))
            e[3][1] = rd.choice(list(range(x.sales[e[2][1]].size)))
        else:
            e[3][0] = rd.choice(list(range(x.plat[e[0]].tournees[e[1]][e[2][0]].size)))
            e[3][1] = rd.choice(list(range(x.plat[e[0]].tournees[e[1]][e[2][1]].size)))
    else:
        e[3] = entry[3]
    return e

#EXTENDED OR_OPT intra_tournee
#entry = paramètre permettant de séléctionner 
# [
#   index_plat : -1 pour tournées sale, 0 à nb plateforme
#   index_type_tournee : 0 pour sales, 1 pour propre
#   index_tournee : 0 à nb de tournee de tel type
#   indexes_affect : ([index_debut seq, index_fin seq], index où inserer seq)
# ]
def N3_intra_rand(x:Solution, entry:list = [-2,-2,-2,[[-2,-2],-2]]):
    e = [-2,-2,-2,[[-2,-2],-2]]
    if entry[0] == -2:
        i = rd.randint(0,len(x.plat))
        if i == 0:
            e[0] = -2
        else:
            e[0] = i-1
    else:
        e[0] = entry[0]

    # print("---------------------------------------------")
    # if e[0] != -1:
    #     print("Plateforme numero " + str(x.plat[e[0]].numero)+ " choisi, "+str(len(x.plat[e[0]].tournees[0]))+" tournées de collecte, "+str(len(x.plat[e[0]].tournees[1]))+" tournées de livraison")
    # else:
    #     print("Transformateur choisi, "+str(len(x.sales))+" tournées de collecte")
    # print("---------------------------------------------")

    #si index_type_tournée non déterminé, affectation aléatoire entre 0 pour collecte et 1 pour livraison
    #si index_plat = Transformateur, 0 assigné
    if entry[1] == -2:
        if e[0] == -1:
            e[1] = 0
        else:
            e[1] = round(rd.random())
    else:
        e[1] = entry[1]

    #si index_tournée non déterminé, affectation à une tournée de type index_type_tournee
    if entry[2] == -2:
        if e[0] == -1:
            e[2] = rd.choice(list(range(len(x.sales))))
            while x.sales[e[2]].size < 3:
                e[2] = rd.choice(list(range(len(x.sales))))
        else:
            e[2] = rd.choice(list(range(len(x.plat[e[0]].tournees[e[1]]))))
            while x.plat[e[0]].tournees[e[1]][e[2]].size < 3:
                e[2] = rd.choice(list(range(len(x.plat[e[0]].tournees[e[1]]))))
    else:
        e[2] = entry[2]
    
    if entry[3][0][0] == -2:
        if e[0] == -1:
            print(e)
            e[3][0][0] = rd.choice(list(range(x.sales[e[2]].size-1)))
            e[3][0][1] = e[3][0][0]
            while e[3][0][1] == e[3][0][0]:
                e[3][0][1] = rd.choice(list(range(e[3][0][0],x.sales[e[2]].size)))
                # On assure que la séléction aléatoire ne prenne pas toute la liste
                if e[3][0][0] == 0 and e[3][0][1] == x.sales[e[2]].size-1:
                    e[3][0][0] == e[3][0][1]
        else:
            e[3][0][0] = rd.choice(list(range(x.plat[e[0]].tournees[e[1]][e[2]].size-1)))
            e[3][0][1] = e[3][0][0]
            while e[3][0][1] == e[3][0][0]:
                e[3][0][1] = rd.choice(list(range(e[3][0][0],x.plat[e[0]].tournees[e[1]][e[2]].size)))
                # On assure que la séléction aléatoire ne prenne pas toute la liste
                if e[3][0][0] == 0 and e[3][0][1] == x.plat[e[0]].tournees[e[1]][e[2]].size-1:
                    e[3][0][0] == e[3][0][1]
    else:
        e[3][0] = entry[3][0]
    
    if entry[3][1] == -2 :
        if e[0] == -1:
            # x.sales[e[2]].print_tournee()
            # print(x.sales[e[2]].size)
            # print(i)
            e[3][1] = rd.choice([i for i, j in enumerate(list(range(x.sales[e[2]].size))) if j not in range(e[3][0][0],e[3][0][1])])
        else:
            # x.plat[e[0]].tournees[e[1]][e[2]].print_tournee()
            # print(x.plat[e[0]].tournees[e[1]][e[2]].size)
            #i = [i for i, j in enumerate(list(range(x.plat[e[0]].tournees[e[1]][e[2]].size))) if j not in range(e[3][0][0],e[3][0][1])]
            # print(i)
            e[3][1] = rd.choice([i for i, j in enumerate(list(range(x.plat[e[0]].tournees[e[1]][e[2]].size))) if j not in range(e[3][0][0],e[3][0][1])])
    return e

#EXTENDED OR_OPT inter_tournee
#entry = paramètre permettant de séléctionner 
# [
#   index_plat : -1 pour tournées sale, 0 à nb plateforme
#   index_type_tournee : 0 pour sales, 1 pour propre
#   index_tournee : (0 à nb de tournee de tel type, 0 à nb de tournee de tel type)
#   indexes_affect : ([index_debut seq, index_fin seq], index où inserer seq dans t2)
# ]
def N3_inter_rand(x:Solution, entry:list = [-2,-2,[-2,-2],[[-2,-2],-2]]):
    

    e = [-2,-2,[-2,-2],[[-2,-2],-2]]

    if entry[0] == -2:
        i = rd.randint(0,len(x.plat))
        if i == 0:
            if len(x.sales)>1:
                j = 0
                count = 0
                t = 0
                while j < len(x.sales) and count < 2:
                    if x.sales[j].size >1 :
                        count += 1
                    j+= 1
                t += 1
                if count == 2:
                    e[0] = -1
                else:
                    i = rd.randint(0,len(x.plat))
            else:
                i = rd.randint(0,len(x.plat))
        else:
            if len(x.plat[i-1].tournees[0])>1 or len(x.plat[i-1].tournees[1]) > 1:
                count = 0
                t = 0
                while t < 2 and count < 2:
                    j = 0
                    count = 0
                    while j < len(x.plat[i-1].tournees[t]) and count < 2:
                        if x.plat[i-1].tournees[t][j].size >1 :
                            count += 1
                        j+= 1
                    t += 1
                if count == 2:
                    e[0] = i-1
                else:
                    i = rd.randint(0,len(x.plat))
            else:
                i = rd.randint(0,len(x.plat))
    else:
        e[0] = entry[0]

    # print("---------------------------------------------")
    # if e[0] != -1:
    #     print("Plateforme numero " + str(x.plat[e[0]].numero)+ " choisi (index : "+str(e[0])+"), "+str(len(x.plat[e[0]].tournees[0]))+" tournées de collecte, "+str(len(x.plat[e[0]].tournees[1]))+" tournées de livraison")
    # else:
    #     print("Transformateur choisi, "+str(len(x.sales))+" tournées de collecte")
    # print("---------------------------------------------")

    #si index_type_tournée non déterminé, affectation aléatoire entre 0 pour collecte et 1 pour livraison
    #si index_plat = Transformateur, 0 assigné
    if entry[1] == -2:
        if e[0] == -1:
            e[1] = 0
        else:
            e[1] = round(rd.random())
            if len(x.plat[e[0]].tournees[0])>1 or len(x.plat[e[0]].tournees[1]) > 1:
                if len(x.plat[e[0]].tournees[e[1]])<2:
                    if e[1] == 1 :
                        e[1] = 0
                    else :
                        e[1] = 1
            else:
                print("GEN_Erreur : Type de tournée affectée à une plateforme où on ne peut pas appliquer N3_inter")
                return ValueError
    else:
        if len(x.plat[e[0]].tournees[entry[1]])<2:
            print("Erreur : Mauvaise affectation de type de tournée pour plateforme, essai d'affecter à l'autre type")
            if entry[1] == 1 :
                e[1] = 0
            else:
                e[1] =1
            if len(x.plat[e[0]].tournees[e[1]])<2:
                print("Erreur : Echec réaffectation, plateforme où on ne peut pas appliquer N3_inter")
                return ValueError
        else:
            e[1] = entry[1]

    #si index_tournée non déterminé, affectation à une tournée de type index_type_tournee
    if entry[2][0] == -2:
        if e[0] == -1:
            if len(x.sales) > 1:
                e[2][0] = rd.choice(list(range(len(x.sales))))
                e[2][1] = rd.choice([i for i, j in enumerate(list(range(len(x.sales)))) if j != e[2][0]])
            else:
                print("GEN_Erreur : Mauvaise affectation à la collecte prod sales où il y a une seule tournée")
                return ValueError
        else:
            if len(x.plat[e[0]].tournees[e[1]]) > 1:
                e[2][0] = rd.choice(list(range(len(x.plat[e[0]].tournees[e[1]]))))
                e[2][1] = rd.choice([i for i, j in enumerate(list(range(len(x.plat[e[0]].tournees[e[1]])))) if j != e[2][0]])
            else:
                print("GEN_Erreur : Mauvaise affectation a une plateforme et un type où il y a une seule tournée")
                return ValueError       
    else:
        if entry[0] == -2:
            if len(x.sales) > 1:
                e[2] = entry[2]
            else:
                print("Erreur : Mauvaise affectation à la collecte prod sales où il y a une seule tournée")
        else:
            if len(x.plat[e[0]].tournees[e[1]]) > 1:
                e[2] = entry[2]
            else:
                print("Erreur : Mauvaise affectation a une plateforme et un type où il y a une seule tournée")
                return ValueError    

    if entry[3][0][0] == -2:
        if e[0] == -1:
            # x.sales[e[2][0]].print_tournee()
            if x.sales[e[2][0]].size == 1:
                e[3][0][0] = 0
                e[3][0][1] = 1
            else:
                e[3][0][0] = rd.choice(list(range(x.sales[e[2][0]].size-1)))
                e[3][0][1] = e[3][0][0]
                while e[3][0][1] == e[3][0][0]:
                    e[3][0][1] = rd.choice(list(range(e[3][0][0],x.sales[e[2][0]].size)))
        else:
            # x.plat[e[0]].tournees[e[1]][e[2][0]].print_tournee()
            if x.plat[e[0]].tournees[e[1]][e[2][0]].size == 1:
                e[3][0][0] = 0
                e[3][0][1] = 1
            else:
                e[3][0][0] = rd.choice(list(range(x.plat[e[0]].tournees[e[1]][e[2][0]].size-1)))
                e[3][0][1] = e[3][0][0]
                while e[3][0][1] == e[3][0][0]:
                    e[3][0][1] = rd.choice(list(range(e[3][0][0],x.plat[e[0]].tournees[e[1]][e[2][0]].size)))
    else:
        e[3][0] = entry[3][0]
    
    if entry[3][1] == -2 :
        if e[0] == -1:
            # x.sales[e[2][0]].print_tournee()
            # x.sales[e[2][1]].print_tournee()
            e[3][1] = rd.choice(list(range(x.sales[e[2][1]].size)))
        else:
            # x.plat[e[0]].tournees[e[1]][e[2][0]].print_tournee()
            # x.plat[e[0]].tournees[e[1]][e[2][1]].print_tournee()
            e[3][1] = rd.choice(list(range(x.plat[e[0]].tournees[e[1]][e[2][1]].size)))
    return e


def N5_add_rand(x:Solution, N:int, entry = [-2]):
    e = [-2]

    if entry[0] == -2:
        numero_plat_ouvertes = []
        for i in range(len(x.plat)):
            numero_plat_ouvertes.append(x.plat[i].numero)
        
        e[0] = rd.choice([i for i, j in enumerate(list(range(N))) if j not in numero_plat_ouvertes])
    else:
        e[0] = entry[0]
    
    return e

def N5_del_rand(x:Solution, N:int, entry = [-2]):
    e = [-2]
    if entry[0] == -2:
        e[0] = rd.choice(list(range(len(x.plat))))
    else:
        e[0] = entry[0]
    
    return e

def N5_swap_rand(x:Solution, N:int, entry = [-2,-2]):
    e = [-2,-2]
    if entry[0] == -2:
        e[0] = rd.choice(list(range(len(x.plat))))
    else:
        e[0] = entry[0]

    if entry[1] == -2:
        numero_plat_ouvertes = []
        for i in range(len(x.plat)):
            numero_plat_ouvertes.append(x.plat[i].numero)
        e[1] = rd.choice([i for i, j in enumerate(list(range(N))) if j not in numero_plat_ouvertes])
    else:
        e[1] = entry[1]
    
    return e

def N6_one_rand(x:Solution, C:int, N:int, entry = [-2,-2]):
    e = [-2,-2]
    if entry[0] == -2:
        e[0] = rd.choice(list(range(N,C)))
    else:
        e[0] = entry[0]

    return e

def N6_some_rand(x:Solution, C:int, N:int, entry = [[-2],[-2]]):
    e = [[],[]]
    
    nb = rd.choice(range(2,C-N))
    while(len(e[0]) < nb):
        c = rd.choice(range(C-N))
        if c not in e[0]:
            e[0].append(c+N)
            e[1].append(rd.choice(range(len(x.plat))))
    
    return e

def N6_all_rand(x:Solution, len:int):
    e = []
    for i in range(len):
        e.append(rd.choice(list(range(0,len(x.plat)))))

    return e