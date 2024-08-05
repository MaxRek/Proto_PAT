from .plateforme import Plateforme
from .tournee import Tournee
from ..algorithm.CAW import CAW_F
from ..tools import get_sum_qt_c_l_by_d,reduct_LnfPT
import random as rd
from bisect import insort

class Solution:
    sales:list[Tournee]
    plat:list[Plateforme]

    def __init__(self) -> None:
        self.sales = []
        self.plat = []

    #Vérification si la solution est admissible
    def verif_solution(self,C:int, N:int,Q:float):
        b = True
        #Vérification que tous les clients soient affectés à une plateforme minimum
        #Récupération de quel client est affecté à quel plateforme.
        ind_c = []
        for p in range(len(self.plat)):
            for c in self.plat[p].cli_affect:
                if c not in ind_c:
                    insort(ind_c, c)
                else:
                    print("Erreur : client c"+str(c)+" affecté à au moins deux plateformes")
                    b = False
        
        #Tous les clients sont affectés,
        if ind_c == list(range(N,C)):
            a = 0
            # print("ok")
        #Tous les clients ne sont pas affectés
        else:
            print("Tous les clients ne sont pas affectés : ")
            print(ind_c)
            print(list(range(N,C)))    
            b = False

        #Pour chaque plateforme, vérification que les producteurs soient bien affectés + tournée de collecte propres
        for p in self.plat:
            #Récupération des quantités/points à visiter pour les producteurs
            temp_LnfPT = reduct_LnfPT(p.Lfptn,C)
            temp_pt = p.verif_all_pt_visited()
            #Pas de producteur visité en double
            if temp_pt[0]: 
                #Pas de producteur manquants/supplémentaires à ceux affectés
                if sorted(temp_LnfPT[0]) == sorted(temp_pt[1]):
                    #Quantité à collecter non respectée
                    if sum(temp_LnfPT[1]) == sum(temp_pt[2]):
                        #Récupération des quantités/points à visiter pour les clients
                        temp_c = p.verif_all_c_visited()
                        if temp_c[0]:
                            #Pas de clients en double
                            if sorted(p.cli_affect) == sorted(temp_c[1]):
                                #Quantité livrée inférieure/supérieure à celle collectée
                                if (sum(temp_pt[2]) + p.xT*Q) != sum(temp_c[2]):
                                    print("Erreur : Somme des quantités livrés dans les tournées != somme quantités collectés")
                                    print("xT = "+ str(p.xT))
                                    print(temp_c[2])
                                    print(temp_pt[2])
                                    print(sum(temp_c[2]))
                                    print(sum(temp_pt[2]))
                                    b = False
                            else:
                                print("Erreur : Tous les clients visités dans les tournées != Clients affectés à la plateforme")
                                print(sorted(p.cli_affect))
                                print(sorted(temp_c[1]))
                                b = False
                        else:
                            print("Erreur : Un client est visité plusieurs fois")
                            b = False
                    else:
                        print("Erreur : La quantité à récupérer par la plateforme != La quantité récupérée par les tournées")
                        print(sum(temp_LnfPT[1]))
                        print(sum(temp_pt[2]))
                        print(temp_LnfPT[1])
                        print(temp_pt[2])
                        b = False
                else:
                    print("Erreur : Les points de collecte à visiter par la plateforme != points de collecte visités par les tournées != points de collecte affectés à la plateforme")
                    print("Points affectés à la plateforme : \n" + str(sorted(p.pt_affect)))
                    print("Points visités dans toutes les tournées : \n" + str(sorted(temp_pt[1])))
                    b = False
            else:
                print("Erreur : Un point de collecte est visité plusieurs fois par la plateforme "+str(p.numero))
                print(sum(temp_LnfPT[1]))
                print(sum(temp_pt[2]))
                print(temp_LnfPT[1])
                print(temp_pt[2])
                b = False  
        if b:
            print("La solution est correcte")
        return b
    
    # METHODE DEPRECIEE, NE PAS UTILISER
    #Ajoute les visites manquantes de clients et de producteurs pour produits propres nécéssaires pour valider solution
    #Se fait post affectation d'un client à une plateforme
    def repair_solution_post_N6(self, data):
        
        unaffected_cli = list(range(data.N, data.C))
        for p in self.plat:
            for c in p.cli_affect:
                if c in unaffected_cli:
                    unaffected_cli.remove(c)

        if unaffected_cli != []:
            for c in unaffected_cli:
                insort(self.plat[rd.choice(range(len(self.plat)))].cli_affect,c)

        for p in self.plat:
            p.repair(data)
    
    #calcul de la valeur objectif pour les plateformes et toutes les tournées (+ sales)
    def calc_func_obj(self,O:list, c:list):
        obj = 0
        sum_temp = [0,0]
        #calcul obj pour chaque tournée sales
        for t in self.sales:
            obj += t.calc_obj_tournee(c)
        #calcul obj pour chaque plateforme ouverte
        for p in self.plat:
            temp = p.calc_obj_plat_tournee(O,c)
            sum_temp[0] += temp[0]
            sum_temp[1] += temp[1]

        return [obj, sum_temp[1], sum_temp[0]]         

    #Ajout de client à une plateforme si elle est ouverte
    def add_client_to_plat(self,index:int, c_l:list, d:dict):
        if index >= 0 and index < len(self.plat):
            for c in c_l:
                self.plat[index].add_client(d,c)
        elif index not in range(self.plat):
            print("Erreur : index inexistant dans Solution.plat : i = "+str(index)+", len = "+str(len(self.plat)))
    
    #Initialisation : Clark and Wright pour produits sales
    def init_CAW_sales(self, c:list, Q:float, T_ind:int, indexes:list, Q_ind:list):
        self.sales = CAW_F(c, Q, T_ind,indexes, Q_ind)

    #Initialisation : Clark and Wright pour collecte produits propres
    def init_CAW_cp(self, c:list, Q:float, C:int):
        for i in self.plat:
            temp = reduct_LnfPT(i.Lfptn,C)
            i.tournees[0] = CAW_F(c, Q, i.numero, temp[0], temp[1])

    #Initialisation : Clark and Wright pour livraison produits propres
    def init_CAW_lp(self, c:list, Q:float, d:dict, f:int):
        for i in self.plat:
            i.tournees[1] = CAW_F(c, Q, i.numero, i.cli_affect, get_sum_qt_c_l_by_d(d,i.cli_affect,f))
    
    #fonctions d'affichages/sauvegarde de la solution
    def print_sales(self, index:int = -1):
        if(index >= 0 and index < len(self.sales)):
            print(self.sales[index])
        else:
            print(self.sales)
            
    def print_plateforme(self, index:int):
        try:
            if(index >= 0 and index < len(self.plat)):
                self.plat[index].print_plateforme()
        except:
            print("Erreur : index inexistant dans Solution.plat : i = "+str(index)+", len = "+str(len(self.plat)))

    def print_all_plateformes(self):
        for i in range(len(self.plat)):
            self.plat[i].print_plateforme()
        print("_________________")
        
    def print_sales(self):
        print("Tournées collecte sales : ")
        for i in self.sales:
            i.print_tournee()
        print("_________________")

    def soluce_sales_to_map(self, locations:list, T_ind:int):
        roads =[]
        sommets = {}

        for i in range(len(self.sales)):
            roads.append(self.sales[i].get_full_order())
            for s in roads[i]:
                if s not in list(sommets.keys()):
                    if s == T_ind:
                        sommets[s] = ("T",locations[s])
                    else:
                        sommets[s] = ("P", locations[s])

        return (sommets, roads)
        
    def soluce_propre_to_map(self, locations:list, T_ind:int):
        sommets = {}
        roads = []

        for p in self.plat:
            sommets[p.numero] = ("N", locations[p.numero])
            for c in p.cli_affect:
                sommets[c] = ("C", locations[c])
            for pt in p.pt_affect:
                if pt not in list(sommets.keys()):
                    sommets[pt] = ("P", locations[pt])
            for t in p.tournees[0]:
                roads.append(t.get_full_order())
            for t in p.tournees[1]:
                roads.append(t.get_full_order())

        if T_ind in list(sommets.keys()):
            sommets[T_ind] = ("T",sommets[T_ind][1])
        
        return (sommets, roads)
    
    def soluce_to_dict(self):
        dict_soluce = {}
        tournees_sales = []
        for t in self.sales:
            tournees_sales.append(t.tournee_to_dict())
        dict_soluce["sales"] = tournees_sales
        dict_soluce["plateformes"] = []
        for p in self.plat:
            dict_soluce["plateformes"].append(p.plateforme_to_dict())
        return dict_soluce
    
    def dict_to_solution(self,d_s : dict):
        self.sales = []
        for d_t in d_s["sales"]:
            t = Tournee(0)
            t.dict_to_tournee(d_t)
            self.sales.append(t)
        for d_p in d_s["plateformes"]:
            p = Plateforme(-1)
            p.dict_to_plateforme(d_p)
            self.plat.append(p)

