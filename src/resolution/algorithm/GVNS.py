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

        print("[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]v")
        print("Debut d'algorithme")
        print("Limite de calcul : "+str(lim_calc))
        nb_perturbations = 0
        k_max = 2

        #Boucle effectuant tous les itérations
        while nb_perturbations < lim_perturb:
            print("______________________________________________")
            print("Nb actuel de perturbations effectues : "+str(nb_perturbations))
            k = 0
            
            #Boucles effectuant les itérations et variant les k
            while k < k_max and nb_perturbations < lim_perturb:
                print("Voisinage exploré k : "+str(k))
                
                #Selon k
                
                #Si on modifie une plateforme
                if k == 0:
                    #On définit les fonctions qu'on peut utiliser : On en peut pas fermer la dernière plateforme ouverte
                    fonctions = [N5_Add,N5_Swap]
                    prob = [1/3,2/3]
                    if len(x.plat)>1:
                        fonctions.append(N5_Del)
                        prob = [1/5,3/5,1/5]
                    rand = rd.random()
                    i = 0
                    sum_prob = prob[i]
                    stop = False
                    while not stop and i < len(prob):
                        sum_prob += prob[i+1]
                        if sum_prob > rand:
                            stop = True
                        else:
                            i+= 1
                    
                    xp = fonctions[i](x,data)
                
                #Sinon on copie juste la solution
                else:
                    xp = copy.deepcopy(x)
                
                # #Affichage de la modification
                #xp.print_all_plateformes()
                

                #Si il y a plus d'une plateforme si on ouvre/supprime/swap une plateforme, nous affecter les clients à la plateforme la plus proche
                #S'il n'y a qu'une seule plateforme, la réaffectation n'est pas nécéssaire
                
                if len(xp.plat) > 1:
                    xpp = N6_reaffect(xp, data)
                else:
                    xpp = copy.deepcopy(xp)

                #notes pour benchmark ( nb de plateforme pour l'itération + la valeur objectif initial + le k utilisé)
                obj_pre = xpp.calc_func_obj(data.O,data.c)
                benchmark["pre_z"].append(obj_pre)
                benchmark["nb_plat"].append(len(xpp.plat))
                if k == 0:
                    benchmark["k_VNS"].append((i))
                else:
                    benchmark["k_VNS"].append((-1))

                #Sauvegarde pré VND 
                name = "VNS_"+str(nb_perturbations)+"_pre_loc_z"+str(sum(obj_pre))
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

                #Valeurs objectifs de solution initiale + solution perturbée améliorée
                obj1 = x.calc_func_obj(data.O,data.c)
                obj2 = xppp.calc_func_obj(data.O,data.c)
                benchmark["z"].append(obj2)

                print(str(sum(obj1)) + " > "+str(sum(obj2)))
                
                #La solution améliorée est-elle meilleure que celle enregistrée ?
                if sum(obj1) > sum(obj2):
                    #La solution est meilleure, enregistrement et modification de k
                    print("xppp meilleur Solution dans voisinage de x")
                    x = xppp
                    k = 0
                else:
                    #La solution n'est pas meilleure, nous recommençons avec valeur de k supérieur
                    k += 1
                
                # Passage à perturbation suivante
                nb_perturbations += 1

        print("Nb de perturbations max atteint, fin d'algo")
        print("[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]")

            
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

    #Début itération par plateforme, nous traitons chaque plateforme l'une apres l'autre
    #Puisque k 
    while p < len(x.plat) and count_calc < lim_calc:
        
        #Pour la plateforme, nombre de modifs effectués à retenir
        benchmark["modif_k"].append([])

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
                        print("MODIFICATION SOLUTION")
                        #Benchmark, nb de modif pour la recherche locale incrémenté + modif individuelle enregistrée 
                        nb_modif += 1
                        benchmark["modif_k"][-1].append([entry[0],entry[1], k])

                        #Enregistrement solution en carte
                        name = "VNS_"+str(nb_perturb)+"_VND_"+str(count_calc)+"_z"+str(obj_1)
                        temp = xp.soluce_propre_to_map(data.locations, data.T-1)
                        aff.save_soluce(path+"/"+name+"_p",temp[0],roads = temp[1])
                        aff.clean_M()
                        temp = xp.soluce_sales_to_map(data.locations, data.T-1)
                        aff.save_soluce(path+"/"+name+"_s",temp[0],roads = temp[1])
                        aff.clean_M()

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

            print("ARRIVEE NOUVEAU VOISINAGE")

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
    
    return x