import numpy as np
from ..tools import get_p_c_by_d, get_sum_qt_c_by_d,get_sum_qt_c_l_by_d,reduct_LnfPT
import bisect
import math
from ..struct.tournee import Tournee
from ..struct.sub_data import Sub_data

class Plateforme:
    numero:int
    cli_affect:list
    pt_affect:list
    Lfptn:list
    xT:int
    tournees:list

    def __init__(self, n:int):
        self.numero = n
        self.cli_affect = []
        self.pt_affect = []
        self.Lfptn = []
        self.tournees = [[],[]]
        self.xT = 0

    #Modification de l'emplacement de plateforme, puis dans les tournées
    def set_numero(self,n:int):
        self.numero = n
        for t in self.tournees[0]:
            t.origin = n
        for t in self.tournees[1]:
            t.origin = n

    #Affectation d'un client à une plateforme, et des producteurs
    def add_client(self, d:dict, c:int):
        i = 0
        b = False
        t = False
        #On recherche si le cli est déjà affecté à la plateforme
        while i < len(self.cli_affect) and not b and not t:
            if(self.cli_affect[i]== c):
                b = True
                t = True
            elif(self.cli_affect[i]>c):
                b = True
            i += 1

        #Si t faux, c, ajout client
        if not t:
            bisect.insort(self.cli_affect,c)
            #affectation des producteurs associés au client
            for p in get_p_c_by_d(d, c):
                self.add_pt(p)

    #Affectation d'un producteur à la plateforme
    def add_pt(self, pt:int):
        i = 0
        b = False
        t = False
        #On recherche si le prod est déjà affecté à la plateforme
        while i < len(self.pt_affect) and not b and not t:
            if(self.pt_affect[i]== pt):
                b = True
                t = True
            elif(self.pt_affect[i]>pt):
                b = True
            i += 1

        #Si t faux, ajout prod
        if not t:
            bisect.insort(self.pt_affect,pt)

    #Reparation des tournées post modification dans les affectations à la plateforme, vérification qu'ils sont bien visités
    def repair(self, data:Sub_data):

        #récupération des clients visités dans les tournées de livraison
        temp_c_l_p = self.verif_all_c_visited()

        #Vérification que les clients de la plateforme sont bien tous visités, et s'il existe des points visités non nécéssaires
        unwanted_c_l = []
        missing_c_l = []

        #Vérification que les clients affectés soient bien visités
        for c in self.cli_affect:
            if c not in temp_c_l_p[1]:
                missing_c_l.append(c)

        #Vérification que les clients visités dans les tournées soient bien ceux affectés
        for c in range(len(temp_c_l_p[1])):
            if temp_c_l_p[1][c] not in self.cli_affect:
                unwanted_c_l.append((temp_c_l_p[1][c],temp_c_l_p[3][c]))

        #Si des clients en trop sont dans des tournées, suppresion des clients.
        if unwanted_c_l != []:
            #Parcours des clients en trop
            for c in unwanted_c_l:
                i = 0
                founded = False

                #récupération de l'index pour chaque client indésirable
                while not founded and i <len(self.tournees[1]):
                    if c in self.tournees[1][i].order:
                        founded = True
                    else:
                        i+=1

                #Suppresion du client visité, et suppresion de la tournée si nécéssaire
                if founded:         
                    b = self.tournee_del_point(1,i,c)

            #Mise à jour des quantités dans les tournées
            for t in self.tournees[1]:
                t.calc_load((t.order,get_sum_qt_c_l_by_d(data.d, t.order, data.F)))
        
        #Si des clients manquent dans les tournées, on les ajoute à la fin d'une tournée pouvant l'accueillir, sinon on crée une tournée spécifiquement pour lui
        if missing_c_l != []:
            #Parcours des clients à ajouter
            for c in missing_c_l:
                found = False
                i = 0
                #récupération des quantités à livrer pour chaque client
                qt = sum(get_sum_qt_c_by_d(data.d, c, data.F))
                #Parcours des tournées existantes
                while not found and i < len(self.tournees[1]):
                    #si la quantité de la tournée + celle du client à ajouter < Q, ajout à cette tournée
                    if self.tournees[1][i].load + qt <= data.Q:
                        self.tournees[1][i].best_insert(data.c, c)
                        self.tournees[1][i].load += qt
                        found = True
                    else:
                        i += 1
                #Si aucune tournée trouvée, création d'une nouvelle tournée
                if not found:
                    new_t = Tournee(self.numero)
                    new_t.add_point([c],[qt])
                    self.tournees[1].append(new_t)

        #Vérification des producteurs à visiter
        self.calc_LnfPT_c(data.d, data.C, data.F, data.T,data.T, data.Q)

        #Réduction aux producteurs à visiter pour les produits propres (+ transformateur)
        temp_reduce = reduct_LnfPT(self.Lfptn, data.C)
        self.pt_affect = temp_reduce[0]

        #Vérification de tous les producteurs visités dans les tournées de collecte
        temp_pt_l_p = self.verif_all_pt_visited()
        
        #Vérification que les points de collecte pour la plateforme soient bien tous visités, et si des producteurs non affectés soient visités
        unwanted_pt_l = []
        missing_pt_l = []

        #Vérification que les producteurs affectés soient bien visités
        for p in self.pt_affect:
            if p not in temp_pt_l_p[1]:
                missing_pt_l.append(p)

        #Vérification que les producteurs visités dans les tournées soient bien ceux affectés
        for p in range(len(temp_pt_l_p[1])):
            if temp_pt_l_p[1][p] not in self.pt_affect:
                unwanted_pt_l.append((temp_pt_l_p[1][p],temp_pt_l_p[3][p]))
        
        #Si des producteurs en trop sont dans des tournées, suppresion du producteur.
        if unwanted_pt_l != []:
            #Parcours des producteurs en trop
            for pt in unwanted_pt_l:
                i = 0
                founded = False

                #récupération de l'index pour chaque producteur indésirable
                while not founded and i <len(self.tournees[0]):
                #Suppression des sommets, 
                    if pt in self.tournees[0][i].order:
                        founded = True
                    else:
                        i+=1

                #Suppresion du producteur visité, et suppresion de la tournée si nécéssaire
                if founded:         
                    b = self.tournee_del_point(0,i,pt)  
                    if b:
                        self.tournees[0][i].calc_load(temp_reduce)
            
        #Si des producteurs manquent dans les tournées, on les ajoute à la fin d'une tournée pouvant l'accueillir, sinon on crée une tournée spécifiquement pour lui
        
        if missing_pt_l != []:
            #Parcours des prod à ajouter
            for p in missing_pt_l:
                found = False
                i = 0
                #récupération des quantités à récupérer pour chaque producteur
                qt = temp_reduce[1][temp_reduce[0].index(p)]
                #Parcours des tournées existantes
                while not found and i < len(self.tournees[0]):
                    #si la quantité de la tournée + celle du prod à récupérer < Q, ajout à cette tournée
                    if self.tournees[0][i].load + qt <= data.Q:
                        self.tournees[0][i].best_insert(data.c, p)
                        self.tournees[0][i].calc_load(temp_reduce)
                        found = True
                    else:
                        i += 1
                #Si aucune tournée trouvée, création d'une nouvelle tournée
                if not found:
                    new_t = Tournee(self.numero)
                    new_t.add_point([p],[qt])
                    self.tournees[0].append(new_t)
        
    #Calcul les quantités à récupérer chez les différents dépôts de produits propres 
    #(producteurs/transformateur) pour la liste de clients c_l
    #Indique aussi si il faut aller voir le transformateur
    def calc_LnfPT_c(self,d:dict, C:int, f:int, pt:int, T:int, Q:int):

        #Création d'une matrice des quantités de produits à récupérer chez les différents producteurs
        self.Lfptn = np.zeros((T-C,f)).tolist()
        #Résumé des quantités de produits sales
        sum_fs = 0

        #Parcours des clients affectés,  
        for c in self.cli_affect:
            #Parcours des producteurs où le client a commandé
            for prod in d[c].keys():
                #Parcours des différents produits commandés
                for value in d[c][prod]:
                    #Si produit sale (A.K.A Légumes), ajout dans résumé des produits sales
                    if value[0] == 0:
                        sum_fs += value[1]
                    #Sinon ajout dans la matrice des quantités
                    else:
                        self.Lfptn[prod-C][value[0]] += value[1]

        #Si des produits sales sont commandés, ajout de la quantité de produtis transformés à récupérer à la légumerie
        if sum_fs > 0:
            self.xT = 0
            self.pt_affect.append(T-1)
            #si la quantité affectée est supérieur à 
            if sum_fs > Q:
                #Calcul du nombre de transports plein entre légumerie et plateforme et soustraction à la quantité à récupérer chez légumerie
                self.xT = math.floor(sum_fs/Q)
                sum_fs = sum_fs - self.xT*Q
            #Affectation de la quantité à récupérer à la légumerie dans une tournée 
            self.Lfptn[-1][0] = sum_fs

    #Vérification si la tournée est à supprimer après suppresion d'un sommet dnas la tournée
    def tournee_post_del_point(self,t_type:int, i:int):
        r = False
        if self.tournees[t_type][i].size == 0:
            self.tournees[t_type].pop(i)
            r = True
        return r
    
    #Suppresion d'un point dans une tournée
    def tournee_del_point(self, t:int, i:int ,s:int):
        self.tournees[t][i].del_point([s])
        r = self.tournee_post_del_point(t,i)
        return r

    #Méthode pour vérification, retourne tous les producteurs visités lors des tournées, leur indexes, et les quantités des tournées
    def verif_all_pt_visited(self):
        ind_pt=[]
        qt_pt=[]
        ind_pt_t=[]
        b = True
        #Parcours tournées de collecte
        for t in range(len(self.tournees[0])):
            #Parcours des sommets dans la tournée
            for sommet in self.tournees[0][t].order:
                #Ajout des nouveaux points visités 
                if sommet not in ind_pt:
                    ind_pt.append(sommet)
                    ind_pt_t.append(t)
                #Erreur : le sommet est visité deux fois dans la collecte
                else:
                    print("Erreur : PT"+str(sommet)+ " visités plus d'une fois")
                    b = False
            qt_pt.append(self.tournees[0][t].load)
        return (b, ind_pt, qt_pt, ind_pt_t)
    
    #Méthode pour vérification, retourne tous les clients visités lors des tournées, leur indexes, et les quantités des tournées
    def verif_all_c_visited(self):
        ind_c=[]
        qt_c=[]
        ind_c_t=[]
        b = True
        #Parcours tournées de livraison
        for t in range(len(self.tournees[1])):
            #Parcours des sommets dans la tournée
            for sommet in self.tournees[1][t].order:
                #Ajout des nouveaux points visités 
                if sommet not in ind_c:
                    ind_c.append(sommet)
                    ind_c_t.append(t)
                #Erreur : le sommet est visité deux fois dans la livraison
                else:
                    print("Erreur : c"+str(sommet)+ " visités plus d'une fois")
                    b = False
            qt_c.append(self.tournees[1][t].load)
        return (b, ind_c, qt_c, ind_c_t)
    
    #Calcul des coûts pour la plateforme, et les tournées
    def calc_obj_plat_tournee(self,O:list, c:list):
        O = O[self.numero]
        #print(O[self.numero])
        xp = 0
        for t in self.tournees[0]:
            xp += t.calc_obj_tournee(c)
        for t in self.tournees[1]:
            xp += t.calc_obj_tournee(c)
        xp += self.xT*c[self.numero][-1]*2
        return [O,xp]


    #Affichage + fonctions de sauvegarde
    def print_plateforme(self):
        print("Plateforme "  +str(self.numero) + " , cli : "+str(self.cli_affect))
        print("prod : "+str(self.pt_affect))
        print("Tournees collecte : ")
        for i in self.tournees[0]:
            i.print_tournee()
        print("Tournées livraison : ")
        for i in self.tournees[1]:
            i.print_tournee()
        print("xT = "+str(self.xT))

    def plateforme_to_dict(self):
        dict_plat = {}
        dict_plat["numero"] = self.numero
        dict_plat["xT"] = self.xT       
        dict_plat["cli_affect"] = self.cli_affect
        dict_plat["pt_affect"] = self.pt_affect
        dict_plat["tournees"] = []
        for i in range(2):
            tournees = []
            for t in self.tournees[i]: 
                tournees.append(t.tournee_to_dict())
            dict_plat["tournees"].append(tournees)
        return dict_plat

    def dict_to_plateforme(self, d_p:dict):
        self.numero = d_p["numero"]
        self.xT = d_p["xT"]
        self.cli_affect = d_p["cli_affect"]
        self.pt_affect = d_p["pt_affect"]
        for i in range(2):
            for d_t in d_p["tournees"][i]: 
                t = Tournee(0)
                t.dict_to_tournee(d_t)
                self.tournees[i].append(t)
