import numpy as np
from ..tools import get_p_c_by_d
import bisect
import math

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
        xT = 0

    def set_numero(self,n:int):
        self.numero = n
        for t in self.tournees[0]:
            t.origin = n
        for t in self.tournees[1]:
            t.origin = n

    def add_client(self, d:list, c:int):
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
            if sum_fs > Q:
                self.xT = math.floor(sum_fs/Q)
                sum_fs = sum_fs - self.xT*Q
                self.pt_affect.append(T-1)
            self.Lfptn[-1][0] = sum_fs

    def tournee_post_del_point(self,t_type:int, i:int):
        r = False
        if self.tournees[t_type][i].size == 0:
            self.tournees[t_type].pop(i)
            r = True
        return r

    #but de vérification, retourne tous les producteurs visités lors des tournées et les quantités des tournées
    def verif_all_pt_visited(self):
        ind_pt=[]
        qt_pt=[]
        b = True
        for t in self.tournees[0]:
            for sommet in t.order:
                if sommet not in ind_pt:
                    ind_pt.append(sommet)
                else:
                    print("Erreur : PT"+str(sommet)+ " visités plus d'une fois")
                    b = False
            qt_pt.append(t.load)
        return (b, ind_pt, qt_pt)
    
    #but de vérification, retourne tous les clients visités lors des tournées et les quantités des tournées
    def verif_all_c_visited(self):
        ind_c=[]
        qt_c=[]
        b = True
        for t in self.tournees[1]:
            for sommet in t.order:
                if sommet not in ind_c:
                    ind_c.append(sommet)
                else:
                    print("Erreur : c"+str(sommet)+ " visités plus d'une fois")
                    b = False
            qt_c.append(t.load)
        return (b, ind_c, qt_c)
    
    def calc_obj_plat_tournee(self,O:list, c:list):
        obj = 0
        obj += O[self.numero]
        #print(O[self.numero])
        for t in self.tournees[0]:
            obj += t.calc_obj_tournee(c)
        for t in self.tournees[1]:
            obj += t.calc_obj_tournee(c)
        return obj


    def get_cli(self):
        return self.cli_affect
    
    def print_plateforme(self):
        print(str(self.numero) + " , cli : "+str(self.cli_affect))
        print("prod : "+str(self.pt_affect)+", Lnfpt = "+str(self.Lfptn))
        print("Tournees collecte : ")
        for i in self.tournees[0]:
            i.print_tournee()
        print("Tournées livraison : ")
        for i in self.tournees[1]:
            i.print_tournee()
        print("xT = "+str(self.xT))

