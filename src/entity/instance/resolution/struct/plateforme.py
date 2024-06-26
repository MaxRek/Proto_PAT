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

    def set_numero(self,n:int):
        self.numero = n
        for t in self.tournees[0]:
            t.origin = n
        for t in self.tournees[1]:
            t.origin = n

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

        #Si t reste faux, c'est que c n'a pas été trouvé
        if not t:
            bisect.insort(self.cli_affect,c)
            for p in get_p_c_by_d(d, c):
                self.add_pt(p)

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

        #Si t reste faux, c'est que pt n'a pas été trouvé
        if not t:
            bisect.insort(self.pt_affect,pt)

    def repair(self, data:Sub_data):
        temp_c_l_p = self.verif_all_c_visited()
        #Vérification que les clients de la plateforme sont bien tous visités, si il y en a en trop,  
        unwanted_c_l = []
        missing_c_l = []
        for c in self.cli_affect:
            if c not in temp_c_l_p[1]:
                missing_c_l.append(c)
        for c in range(len(temp_c_l_p[1])):
            if temp_c_l_p[1][c] not in self.cli_affect:
                unwanted_c_l.append((temp_c_l_p[1][c],temp_c_l_p[3][c]))

        #Si des clients en trop sont dans des tournées, on les enlève.
        if unwanted_c_l != []:
            for c in unwanted_c_l:
                i = 0
                founded = False

                while not founded and i <len(self.tournees[1]):
                #Suppression des sommets, 
                    if c in self.tournees[1][i].order:
                        founded = True
                    else:
                        i+=1

                if founded:         
                    b = self.tournee_del_point(1,i,c)
                    if b:
                        self.tournees[1][i].calc_load(temp_reduce)
            # for i in self.tournees[1]:
            #     i.print_tournee()
            #Mise à jour des quantités dans les tournées

            for t in self.tournees[1]:
                t.calc_load((t.order,get_sum_qt_c_l_by_d(data.d, t.order, data.F)))
        
        #Si des clients manquent dans les tournées, on les ajoute à la fin d'une tournée pouvant l'accueillir, sinon on crée une tournée spécifiquement pour lui
        if missing_c_l != []:
            for c in missing_c_l:
                found = False
                i = 0
                qt = sum(get_sum_qt_c_by_d(data.d, c, data.F))
                while not found and i < len(self.tournees[1]):
                    if self.tournees[1][i].load + qt <= data.Q:
                        self.tournees[1][i].best_insert(data.c, c)
                        self.tournees[1][i].load += qt
                        found = True
                    else:
                        i += 1
                if not found:
                    new_t = Tournee(self.numero)
                    new_t.add_point([c],[qt])
                    self.tournees[1].append(new_t)

        #Réaffectation des producteurs à visiter
        self.calc_LnfPT_c(data.d, data.C, data.F, data.T,data.T, data.Q)
        temp_reduce = reduct_LnfPT(self.Lfptn, data.C)
        self.pt_affect = temp_reduce[0]
        temp_pt_l_p = self.verif_all_pt_visited()
        #Vérification que les points de collecte pour la plateforme soient bien tous visités, si il y en a en trop,  

        unwanted_pt_l = []
        missing_pt_l = []
        for p in self.pt_affect:
            if p not in temp_pt_l_p[1]:
                missing_pt_l.append(p)
        for p in range(len(temp_pt_l_p[1])):
            if temp_pt_l_p[1][p] not in self.pt_affect:
                unwanted_pt_l.append((temp_pt_l_p[1][p],temp_pt_l_p[3][p]))
        
        #Si des producteurs en trop sont dans des tournées, on les enlève.
        if unwanted_pt_l != []:
            for pt in unwanted_pt_l:
                i = 0
                founded = False

                while not founded and i <len(self.tournees[0]):
                #Suppression des sommets, 
                    if pt in self.tournees[0][i].order:
                        founded = True
                    else:
                        i+=1

                if founded:         
                    b = self.tournee_del_point(0,i,pt)  
                    if b:
                        self.tournees[0][i].calc_load(temp_reduce)
            
        #Si des producteurs manquent dans les tournées, on les ajoute à la fin d'une tournée pouvant l'accueillir, sinon on crée une tournée spécifiquement pour lui
        
        if missing_pt_l != []:
            for p in missing_pt_l:
                found = False
                i = 0
                qt = temp_reduce[1][temp_reduce[0].index(p)]
                while not found and i < len(self.tournees[0]):
                    if self.tournees[0][i].load + qt <= data.Q:
                        self.tournees[0][i].best_insert(data.c, p)
                        self.tournees[0][i].calc_load(temp_reduce)
                        found = True
                    else:
                        i += 1
                if not found:
                    new_t = Tournee(self.numero)
                    new_t.add_point([p],[qt])
                    self.tournees[0].append(new_t)
        
    #Calcul les quantités à récupérer chez les différents dépôts de produits propres 
    #(producteurs/transformateur) pour la liste de clients c_l
    #Indique aussi si il faut aller voir le transformateur
    def calc_LnfPT_c(self,d:dict, C:int, f:int, pt:int, T:int, Q:int):
        self.Lfptn = np.zeros((T-C,f)).tolist()
        sum_fs = 0
        for c in self.cli_affect:
            for prod in d[c].keys():
                for value in d[c][prod]:
                    if value[0] == 0:
                        sum_fs += value[1]
                    else:
                        self.Lfptn[prod-C][value[0]] += value[1]
        t = 0
        if sum_fs > 0:
            self.xT = math.floor(sum_fs/Q)

            if sum_fs > Q:
                sum_fs = sum_fs - self.xT*Q
                self.pt_affect.append(T-1)
            self.Lfptn[-1][0] = sum_fs

    def tournee_post_del_point(self,t_type:int, i:int):
        r = False
        if self.tournees[t_type][i].size == 0:
            self.tournees[t_type].pop(i)
            r = True
        return r
    
    def tournee_del_point(self, t:int, i:int ,s:int):
        self.tournees[t][i].del_point([s])
        r = self.tournee_post_del_point(t,i)
        return r

    #but de vérification, retourne tous les producteurs visités lors des tournées et les quantités des tournées
    def verif_all_pt_visited(self):
        ind_pt=[]
        qt_pt=[]
        ind_pt_t=[]
        b = True
        for t in range(len(self.tournees[0])):
            for sommet in self.tournees[0][t].order:
                if sommet not in ind_pt:
                    ind_pt.append(sommet)
                    ind_pt_t.append(t)
                else:
                    print("Erreur : PT"+str(sommet)+ " visités plus d'une fois")
                    b = False
            qt_pt.append(self.tournees[0][t].load)
        return (b, ind_pt, qt_pt, ind_pt_t)
    
    #but de vérification, retourne tous les clients visités lors des tournées et les quantités des tournées
    def verif_all_c_visited(self):
        ind_c=[]
        qt_c=[]
        ind_c_t=[]
        b = True
        for t in range(len(self.tournees[1])):
            for sommet in self.tournees[1][t].order:
                if sommet not in ind_c:
                    ind_c.append(sommet)
                    ind_c_t.append(t)
                else:
                    print("Erreur : c"+str(sommet)+ " visités plus d'une fois")
                    b = False
            qt_c.append(self.tournees[1][t].load)
        return (b, ind_c, qt_c, ind_c_t)
    
    def calc_obj_plat_tournee(self,O:list, c:list):
        O = O[self.numero]
        #print(O[self.numero])
        xp = 0
        for t in self.tournees[0]:
            xp += t.calc_obj_tournee(c)
        for t in self.tournees[1]:
            xp += t.calc_obj_tournee(c)
<<<<<<< HEAD
=======
        xp += c[self.numero][-1]*2
>>>>>>> 128b04c27bac72640f8707943aae53d22733e6c4
        return [O,xp]

    def get_cli(self):
        return self.cli_affect
    
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

