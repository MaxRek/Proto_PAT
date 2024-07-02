from..struct.solution import Solution
from..struct.sub_data import Sub_data
from...entity.aff import Aff
from..algorithm.Neighboorhoods import *
from..algorithm.Neighboorhoods_next import *
import datetime


def GVNS(path:str, data:Sub_data, x : Solution, lim_calc:int, lim_perturb:int,benchmark:dict):
    #Verification avant lancement d'algorithme
    if x.verif_solution(data.C,data.N,data.Q):
        
        #Initialion objet pour enregistrer les cartes
        aff = Aff()

        #Sauvegarde initiale
        temp = x.soluce_propre_to_map(data.locations, data.T-1)
        aff.save_soluce(path+"/init_p",temp[0],roads = temp[1])
        aff.clean_M()
        temp = x.soluce_sales_to_map(data.locations, data.T-1)
        aff.save_soluce(path+"/init_s",temp[0],roads = temp[1])
        aff.clean_M()

        print("[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]")
        print("Debut d'algorithme")
        print("Limite de calcul : "+str(lim_calc))
        nb_perturbations = 0
        k = 0

        #Boucle effectuant tous les itérations
        while nb_perturbations < lim_perturb:

            print("______________________________________________")
            print("Nb actuel de perturbations effectues : "+str(nb_perturbations))

            liste_plat=[list(range(data.N)),[]]
            for p in range(len(x.plat)):
                liste_plat[0].remove(x.plat[p].numero)
                liste_plat[1].append([x.plat[p].numero,p])
                            
            #Pour le propre, si on modifie une plateforme
            #On définit les fonctions qu'on peut utiliser : On en peut pas fermer la dernière plateforme ouverte
            fonctions = [N5_Add,N5_Swap]
            # prob = [1/3,2/3]
            moves = [[],[]]
            if len(x.plat)>1:
                #Si il y a plus d'une plateforme, nous pouvons en fermer une, intégration de N5_del + les éventuelles mouvements
                fonctions.append(N5_Del)
                # prob = [1/5,3/5,1/5]
                moves.append([])
                #Toutes plateformes peuvent être fermées, nous n'avons pas de métriques pour pouvoir en couper certaines
                for p in liste_plat[1]:
                    moves[2].append([p[1]])

            obj_x = x.calc_func_obj(data.O,data.c)
            sum_obj = obj_x[1] + obj_x[2]
            O = obj_x[2]

            #Si le coût d'ouverture des plateformes ouvertes dans le mouvement n'est pas strictement inférieur
            #  à la valeur objectif de la solution actuelle, le mouvement est coupé  
            for p in liste_plat[0]:
                #Dans le cadre de l'ouverture d'une nouvelle plateforme                
                if O + data.O[p] < sum_obj:
                    moves[0].append([p])
                #Dans le cadre d'un swap de plateforme ouverte
                for x_plat in liste_plat[1]:
                    if O - data.O[x_plat[0]] + data.O[p] < sum_obj:
                        moves[1].append([x_plat[1],p])
            print("Nombre de plateforme actuel : "+ str(len(x.plat)))

            # # Affichage des mouvements possibles 
            # print(liste_plat)
            # print(data.O)
            # print(moves)
            # print(sum_obj)
            
            #Définition de k possible, reintialisation si k dépasse
            k_max = len(fonctions)
            if k >= k_max:
                k = 0
            
            # #Ancienne boucle choisissant au hasard le n5 séléctionné (add,swap ou del si possible)
            # rand = rd.random()
            # i = 0
            # sum_prob = prob[i]
            # stop = False
            # while not stop and i < len(prob):
            #     sum_prob += prob[i+1]
            #     if sum_prob > rand:
            #         stop = True
            #     else:
            #         i+= 1

            #Analyse de moves, au cas où il n'existe plus de mouvements considérés comme intéréssant
            #Premier cas, il n'y a pas d'ouverture intéréssant ou de swap intéréssant
            if len(moves[0]) == 0 and len(moves[1]) == 0:
                #s'il est possible de fermer une plateforme,  il y a forcément un choix possible
                if len(moves) == 3:
                    k = 2 
                #sinon ,il n'est plus possible de perturber sans erreur, nous interrompons l'algorithme
                else:
                    print("Plus de perturbations intéréssantes avec n5, arrêt forcé de l'algorithme")
                    # # Affichage des coûts d'ouverture et de la fonction objectif actuelle
                    # print(data.O)
                    # print(str(obj_x) + " = " + str(sum_obj)
                    return x
            else:
                #Second cas, si la liste désignée est vide, nous passons à la liste suivante, un des deux n'a pas de choix possibles, 
                if len(moves[k]) == 0:
                    k += 1    
                    #Si nous dépassons la liste, nous revenons au premier choix
                    if k == k_max:
                        k = 0

            #Add, swap ou del est possible, nous modifions selon les choix que nous avons retenus
            xp = fonctions[k](x,data,rd.choice(moves[k]))
            print("Nombre de plateforme exploré : "+ str(len(xp.plat)))

            #Nous incrémentons k par la suite
            k += 1
            
            #Si il y a plus d'une plateforme si on ouvre/supprime une plateforme, nous affecter les clients à la plateforme la plus proche
            #S'il n'y a qu'une seule plateforme, la réaffectation n'est pas nécéssaire 
            if len(xp.plat) > 1:
                xpp = N6_reaffect(xp, data)
            else:
                xpp = xp       
            
            #Pour le sale, on perturbe une ou des tournées, vérification qu'il y a bien plusieurs tournées pour appliquer tous les voisinages :
            for i in range(5):
                if len(xpp.sales) > 1:
                    fonctions_s = [[N1_intra,N1_inter],[N2_intra,N2_inter],[N3_intra,N3_inter],[N4_intra,N4_inter]]
                    ks = rd.choice(range(len(xpp.sales)))
                    ks_t = rd.randint(0,1)
                else:
                    fonctions_s = [[N1_intra],[N2_intra],[N3_intra],[N4_intra]]
                    ks = rd.choice(range(len(xpp.sales)))
                    ks_t = 0
                    
                e = GVNS_s_e(ks,ks_t)
                xpp.sales = fonctions_s[ks][ks_t](xp,data,e).sales

            

            #notes pour benchmark ( nb de plateforme pour l'itération + la valeur objectif initial + le k utilisé)
            obj_pre = xpp.calc_func_obj(data.O,data.c)
            benchmark["pre_z"].append(obj_pre)
            benchmark["nb_plat"].append(len(xpp.plat))
            benchmark["k_VNS"].append((i))          

            #Sauvegarde pré VND 
            name = "VNS_"+str(nb_perturbations)+"_pre_loc_z"+str(obj_pre)
            temp = xpp.soluce_propre_to_map(data.locations, data.T-1)
            aff.save_soluce(path+"/"+name+"_p",temp[0],roads = temp[1])
            aff.clean_M()
            temp = xpp.soluce_sales_to_map(data.locations, data.T-1)
            aff.save_soluce(path+"/"+name+"_s",temp[0],roads = temp[1])
            aff.clean_M()

            #Recherche locale + temps de calcul
            time_start = datetime.datetime.now()
            xppp = VND(path, data, xpp, lim_calc, nb_perturbations, benchmark)
            benchmark["time"].append((datetime.datetime.now()-time_start).seconds)
            print("- - - - - - - - - - - - - - - - - - - - -")

            #Valeurs objectifs de solution initiale + solution perturbée améliorée
            obj1 = x.calc_func_obj(data.O,data.c)
            obj2 = xppp.calc_func_obj(data.O,data.c)
            benchmark["z"].append(obj2)
            print(str(obj1) + " > " +str(obj2))
            print(str(sum_obj) + " > "+str(sum(obj2[1:3])))
            
            #La solution sale améliorée est-elle meilleure que celle enregistrée ?
            if obj_x[0] > obj2[0]:
                #La solution est meilleure, enregistrement et modification de k
                print("xppp sales meilleur Solution dans voisinage de x")
                x.sales = xppp.sales

            #La solution propre améliorée est-elle meilleure que celle enregistrée ?
            if sum_obj > sum(obj2[1:3]):
                #La solution est meilleure, enregistrement et modification de k
                print("xppp propre meilleur Solution dans voisinage de x")
                x.plat = xppp.plat
            
            # Passage à perturbation suivante
            nb_perturbations += 1

        print("Nb de perturbations max atteint, fin d'algo")
        print("[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]")
        
        
        #Sauvegarde post recherche
        obj_best = x.calc_func_obj(data.O,data.c)
        print("Meilleur solution = "+str(obj_best))
        name = "Best_soluce_"+str(obj_best)
        temp = x.soluce_propre_to_map(data.locations, data.T-1)
        aff.save_soluce(path+"/"+name+"_p",temp[0],roads = temp[1])
        aff.clean_M()
        temp = x.soluce_sales_to_map(data.locations, data.T-1)
        aff.save_soluce(path+"/"+name+"_s",temp[0],roads = temp[1])
        aff.clean_M()
            
    return x

def VND(path, data:Sub_data, x : Solution, lim_calc:int, nb_perturb:int, benchmark:list):

    #Initialisation : - Fonctions utilisés ([Intra,Inter])
    fonctions = [[N1_intra,N1_inter],[N2_intra,N2_inter],[N3_intra,N3_inter],[N4_intra,N4_inter]]
    k_max = len(fonctions)
    
    #Objet pour enregistrer cartes
    aff = Aff()
    
    #limite pour lim_calc
    count_calc = 0
    
    #Benchmark
    nb_modif = 0

    print("___________________________________")
    print("Début algo VND")
    
    #Initialisation des variables plateforme et structures de voisinage
    p = -1
    k = 0

    #Benchmark : modification effectué à retenir
    benchmark["modif_k"].append([])

    #Début itération par plateforme, nous traitons chaque plateforme l'une apres l'autre
    #Puisque k 
    while p < len(x.plat) and count_calc < lim_calc:
        #Init k, et entrée pour générateur
        entry = [p]
        # # Affichage : <plateforme> <nb_plat>, <k> <nb_k>, <it_calc> <# de calculs maximum>
        #print("p =  " + str(p) + ", len(x.plat) = "+ str(len(x.plat)) + ", k = " +str(k) + ", k_max = "+str(k_max)+ ", count_calc = "+str(count_calc)+", lim_calc = "+str(lim_calc))#+", entry = "+str(entry))
        if count_calc < lim_calc:
            
            #Exploration du voisinage k
            founded = True
            #Tq il y a un voisin à observer + budget de calcul disponible
            while founded and count_calc < lim_calc:
                # # Affichage :  <entrée pour générateur>, <plateforme> <nb_plat>, <k> <nb_k>, <it_calc> <# de calculs maximum>
                #print("entry = "+str(entry)+ ", p =  " + str(p) + ", len(x.plat) = "+ str(len(x.plat)) + ", k = " +str(k) + ", k_max = "+str(k_max)+ ", count_calc = "+str(count_calc)+", lim_calc = "+str(lim_calc))#)

                # Récupération du voisin suivant, temp = [<Solution>, <entrée pour générateur>, <voisin suivant trouvé ?>]
                temp = next_voisin(x, k, entry)
                entry = temp[1]

                #Si un voisin a été trouvé, génération du voisin
                founded = temp[2]
                if founded and entry[0] == p:
                    #Vérification si le mouvement est intra/inter tournée
                    if type(temp[1][2]) == int:
                        xp = fonctions[k][0](temp[0],data,temp[1])
                    else:
                        xp = fonctions[k][1](temp[0],data,temp[1])
                    
                    #Calcul de la fonc obj et si le voisin a une meilleure fonction objectif, remplacement par celui çi
                    obj_1 = xp.calc_func_obj(data.O,data.c)
                    if x.calc_func_obj(data.O,data.c) > obj_1:
                        #print("MODIFICATION SOLUTION K = "+str(k))
                        #Benchmark, nb de modif pour la recherche locale incrémenté + modif individuelle enregistrée 
                        nb_modif += 1
                        benchmark["modif_k"][-1].append([entry[0],entry[1], k])

                        # #Enregistrement solution en carte
                        # name = "VNS_"+str(nb_perturb)+"_VND_"+str(count_calc)+"_z"+str(obj_1)
                        # temp = xp.soluce_propre_to_map(data.locations, data.T-1)
                        # aff.save_soluce(path+"/"+name+"_p",temp[0],roads = temp[1])
                        # aff.clean_M()
                        # temp = xp.soluce_sales_to_map(data.locations, data.T-1)
                        # aff.save_soluce(path+"/"+name+"_s",temp[0],roads = temp[1])
                        # aff.clean_M()

                        #La solution retenue devient la nouvelle solution de base (première descente), reinitialisation de k
                        x = xp
                        k = 0
                        # L'entrée du générateur est réinitialisé dans le circuit où était le générateur (plateforme)
                        # Entrée correspondant à l'initialisation pour le voisinage k1 intra-route
                        entry = [p,entry[1],0,[0,0]]
                    else:
                        #La fonction obj du voisin généré n'est pas meilleure, nous reinitialisons xp (peut causer bug si non effectué)
                        xp = x

                #Un voisin n'a pas été trouvée pour ce voisinage k, changement de voisinage k en sortir de boucle
                else:
                    #puisque le générateur change initialement de plateforme, nous devons observer si la plateforme a été modifiée. 
                    #Si oui, c'est que le voisinage k a été exploré, nous refixons l'entrée sur la plateforme, et nous incrémentons k
                    if entry[0] != p:
                        entry = [p]
                        k = k + 1
                    
                    #Si toutes les structures de voisinage ont été visitées, nous passons à la plateforme suivante 
                    if k == k_max:
                        p += 1
                        entry = [p]
                        k = 0

                #Incrémentation nombre de calcul
                count_calc += 1

            #print("ARRIVEE NOUVEAU VOISINAGE")

    # Benchmark : Algorithme ayant atteint la fin de son exploration 
    if count_calc < lim_calc:
        print("Voisinage complétement exploré")
        benchmark["non_fini"].append(False)
    # Benchmark : Algorithme n'ayant pas terminé son exploration
    else:
        print("Voisinage non exploré")
        benchmark["non_fini"].append(True)
    
    # Benchmark : Nb de modification effectué lors de cette recherche locale
    benchmark["nb_modifs"].append(nb_modif)

    name = "VNS_"+str(nb_perturb)+"_VND_"+str(count_calc)+"_z"+str(obj_1)
    temp = x.soluce_propre_to_map(data.locations, data.T-1)
    aff.save_soluce(path+"/"+name+"_p",temp[0],roads = temp[1])
    aff.clean_M()
    temp = x.soluce_sales_to_map(data.locations, data.T-1)
    aff.save_soluce(path+"/"+name+"_s",temp[0],roads = temp[1])
    aff.clean_M()
    
    return x

def GVNS_s_e(k:int, k_t:int):
    if k == 0 or k == 1:
        if k_t == 0:
            e = [-1,0,-2,[-2,-2]]
        else:
            e = [-1,0,[-2,-2],[-2,-2]]
    elif k == 2 or k == 3:
        if k_t == 0:
            e = [-1,0,-2,[[-2,-2],-2]]
        else:
            e = [-1,0,[-2,-2],[[-2,-2],-2]]
    return e