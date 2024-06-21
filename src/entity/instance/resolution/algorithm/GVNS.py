from..struct.solution import Solution
from..struct.sub_data import Sub_data
from....aff import Aff
from..algorithm.Neighboorhoods import *
from..algorithm.Neighboorhoods_next import *
import datetime


def GVNS(path:str, data:Sub_data, x : Solution, lim_calc:int, lim_perturb:int,benchmark:dict):
    if x.verif_solution(data.C,data.N,data.Q):
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
        while nb_perturbations < lim_perturb:
            print("______________________________________________")
            print("Nb actuel de perturbations effectues : "+str(nb_perturbations))
            k = 0
            
            while k < k_max and nb_perturbations < lim_perturb:
                if nb_perturbations < lim_perturb:
                    print("Voisinage exploré k : "+str(k))
                    if k == 0:
                        #On définit les fonctions qu'on peut utiliser : On en peut pas fermer la dernière plateforme ouverte
                        fonctions = [N5_Add,N5_Swap]
                        prob = [1/3,2/3]
                        if len(x.plat)>1:
                            fonctions.append(N5_Del)
                            prob = [1/5,3/5,1/5]
                        rand = rd.random()
                        i = 0
                        sum_prob = 0
                        stop = False
                        while not stop and i < len(prob):
                            sum_prob += prob[i]
                            if sum_prob > rand:
                                stop = True
                            else:
                                i+= 1
                        
                        xp = fonctions[i](x,data)
                    else:
                        xp = copy.deepcopy(x)

                    #Même si on ouvre/supprime/swap une plateforme, nous décidons au hasard de réaffecter les clients aux plateformes    
                    #S'il n'y a qu'une seule plateforme, la réaffectation n'est pas nécéssaire
                    fonctions = [N6_one,N6_some,N6_all]
                    prob = [1/5,3/5,1/5]
                    rand = rd.random()
                    j = 0
                    sum_prob = prob[j]
                    stop = False
                    while not stop and j+1 < len(prob):
                        sum_prob += prob[j+1]
                        if sum_prob > rand:
                            stop = True
                        else:
                            j+= 1
                    xpp = fonctions[j](xp,data)
                    benchmark["nb_plat"].append(len(xpp.plat))
                    if k == 0:
                        benchmark["k_VNS"].append((i,j))
                    else:
                        benchmark["k_VNS"].append((-1,j))

                    #Sauvegarde pré VND
                    obj_pre = xpp.calc_func_obj(data.O,data.c)
                    benchmark["pre_z"].append(obj_pre)

                    name = "VNS_"+str(nb_perturbations)+"_pre_loc_z"+str(sum(obj_pre))
                    temp = xpp.soluce_propre_to_map(data.locations, data.T-1)
                    aff.save_soluce(path+"/"+name+"_p",temp[0],roads = temp[1])
                    aff.clean_M()
                    temp = xpp.soluce_sales_to_map(data.locations, data.T-1)
                    aff.save_soluce(path+"/"+name+"_s",temp[0],roads = temp[1])
                    aff.clean_M()

                    time_start = datetime.datetime.now()
                    xppp = VND(path, data, xpp, lim_calc, nb_perturbations, benchmark)
                    time_stop = datetime.datetime.now()-time_start
                    print(time_stop)
                    benchmark["time"].append(time_stop.seconds)
                    # xppp.print_all_plateformes()
                    obj1 = x.calc_func_obj(data.O,data.c)
                    obj2 = xppp.calc_func_obj(data.O,data.c)
                    benchmark["z"].append(obj2)

                    if sum(obj1) > sum(obj2):
                        print("xpp meilleur Solution dans voisinage de x")
                        x = xpp
                        k = 0
                    else:
                        xp = x
                        k += 1
                    nb_perturbations += 1
                else:
                    k = k_max    

        print("Limite de calcul atteinte")
        print("[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]")

            
    return x

def VND(path, data:Sub_data, x : Solution, lim_calc:int, nb_perturb:int, benchmark:list):
    k_max = 4
    fonctions = [[N1_intra,N1_inter],[N2_intra,N2_inter],[N3_intra,N3_inter],[N4_intra,N4_inter]]
    print("___________________________________")
    print("Début algo VND")
    count_calc = 0
    aff = Aff()
    nb_modif = 0
    benchmark["modif_k"].append([])
    while count_calc < lim_calc:
        k = 0
        entry = [-1]

        while k < k_max and count_calc < lim_calc:
            print("___________________________________")
            print("Nb actuel de calcul effectues : "+str(count_calc))
            if count_calc < lim_calc:
                print("Voisinage exploré k : "+str(k))
                founded = True
                while founded and count_calc < lim_calc:
                    #print(entry)

                    temp = next_voisin(x, k, entry)
                    entry = temp[1]
                    # if type(entry[2])==int:
                    #     print(entry)

                    # elif entry[2] == 1:
                    #     print(entry)

                    # print(entry)
            
                    #Si un voisin a été trouvé,on explore la solution
                    founded = temp[2]
                    if founded:
                        if type(temp[1][2]) == int:
                            xp = fonctions[k][0](temp[0],data,temp[1])
                        else:
                            xp = fonctions[k][1](temp[0],data,temp[1])
                        obj_1 = xp.calc_func_obj(data.O,data.c)
                        print(str(x.calc_func_obj(data.O,data.c)) + " > " +str(obj_1))
                        if x.calc_func_obj(data.O,data.c) > obj_1:
                            print("xp meilleur Solution dans voisinage de x")
                            nb_modif += 1
                            benchmark["modif_k"][-1].append([entry[0],entry[1], k])
                            #Enregistrement solution
                            name = "VNS_"+str(nb_perturb)+"_VND_"+str(count_calc)+"_z"+str(obj_1)
                            temp = x.soluce_propre_to_map(data.locations, data.T-1)
                            aff.save_soluce(path+"/"+name+"_p",temp[0],roads = temp[1])
                            aff.clean_M()
                            temp = x.soluce_sales_to_map(data.locations, data.T-1)
                            aff.save_soluce(path+"/"+name+"_s",temp[0],roads = temp[1])
                            aff.clean_M()

                            x = xp
                            k = 0
                        #Si la modification a eu lieu dans les circuits propre d'une plateforme, nous modifions l'entrée pour recommencer l'exploration sur N1 de cette plateforme
                            if entry[0] == -2:
                                entry = [-1]
                            else:
                                entry = [entry[0],0,0,[0,0]]
                        else:
                            xp = x
                    #Sinon on change de voisinage
                    else:
                        k += 1
                        entry = [-1]
                    count_calc += 1
                    print("Nb actuel de calcul effectues : "+str(count_calc))

                print("Founded terminé ? : "+str(founded))
                #x.print_all_plateformes()
                k += 1                      
            else:
                k = k_max
                
            count_calc += 1

        

        if count_calc < lim_calc:
            benchmark["non_fini"].append(False)
        else:
            benchmark["non_fini"].append(True)
        benchmark["nb_modifs"].append(nb_modif)
        count_calc = lim_calc
    return x
