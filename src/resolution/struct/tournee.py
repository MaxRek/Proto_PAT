class Tournee:
    order:list
    origin:int
    size:int
    load:float

    def __init__(self, o:int) -> None:
        self.origin = o
        self.order = []
        self.size = 0
        self.load = 0

    #Methode pour ajouter des sommets à une tournée avec les quantités associées
    def add_point(self,points:list,QT_recup:list,ind:int = -1):
        # Modification de l'ordre
        s = len(points)
        
        # Ajout des sommets à la fin de la tournée si non spécifiée 
        if ind == -1:
            #Parcours des sommets à ajouter
            for i in range(s):
                self.order.insert(self.size,points[i])
                self.size += 1
                self.load += QT_recup[i]
        #Si l'index spécifié est correcte, ajout des sommets à l'index
        elif ind >= 0 and ind < len(self.order):
            for i in range(s):
                self.order.insert(ind,points)
                self.size += 1
                self.load += QT_recup[i]
        else:
            print("Erreur : ind n'est pas une valeur correcte : "+str(ind))

    #Methode non utilisée
    # Suppresion de numéro de sommets à la tournée 
    def del_point(self, points:list):
        for point in points:
            if point in self.order:
                self.order.remove(point)
                self.size -= 1                    

    # Calcul de la quantité selon une réduction de LfnPT (indexes + quantités associées)
    def calc_load(self, reduce_LfnPT:tuple):
        self.load = 0
        for i in self.order:
            if i in reduce_LfnPT[0]:
                self.load += reduce_LfnPT[1][reduce_LfnPT[0].index(i)]

    # Insertion d'un sommet à l'index spécifié
    def insert_sommet(self, s:int, i:int):
        self.size += 1
        self.order.insert(i,s)

    #Mouvement d'insertion N1_intra: 
    def reinsert(self, i:int, j:int):
        # Pop du sommet i dans la tournée, puis ajout à place j la tournée
        s = self.order.pop(i)
        self.order.insert(j,s)

    #Mouvement d'insertion N1_intra
    #pop un sommet dans l'ordre
    def pop(self, i:int):
        self.size -= 1
        s = self.order.pop(i)
        return s 
    
    #Methode non utilisée
    #ajoute un sommet dans la meilleure connexion (i,j) possible 
    def best_insert(self, c:list, s:int):
        order = self.get_full_order()
        costs = []
        #Entre point d'origine et premier sommet visités :
        for i in range(len(order)-1):
            costs.append(c[order[i]][s] + c[s][order[i+1]])
        #print(costs)
        #print(sorted(range(len(costs)), key=lambda k: costs[k], reverse=True))
        return self.insert_sommet(s,sorted(range(len(costs)), key=lambda k: costs[k], reverse=True)[0])

    #Mouvement de swap N2_intra
    def swap_two_s_order(self,i:int,j:int):
        #Swap de deux sommets
        temp = self.order[i]
        self.order[i] = self.order[j]
        self.order[j] = temp

    #Mouvement de EXTENDED OR_OPT N3_intra
    def extended_or_opt(self, seq:list, i:int):
        #récupération de la séquence
        sommets = self.order[seq[0]:seq[1]+1]

        #supression de la séquence
        for s in sommets:
            self.order.pop(seq[0])

        #Modification de l'index si i est > fin de seq sinon erreur index possible
        if i > seq[-1]:
            i = i - len(range(seq[0],seq[1]))

        #Réinsertion des sommets dans l'ordre
        for j in range(len(sommets)):
            self.order.insert(i,sommets[-1*(j+1)])

    #Mouvement de EXTENDED OR_OPT N3_inter et INVERSE OR_OPT N4_inter
    def insert_seq_or_opt(self, seq:list, i:int):
        for j in range(len(seq)):
            self.order.insert(i,seq[-1*(j+1)])
            self.size += 1

    #Mouvement de INVERSE OR_OPT N4_intra
    def inverse_or_opt(self, seq:list, i:int):
        #récupération de la séquence
        sommets = self.order[seq[0]:seq[1]+1]
        
        #supression de la séquence
        for s in sommets:
            self.order.pop(seq[0])

        #Modification de l'index si i est > fin de seq sinon erreur index possible
        if i > seq[-1]:
            i = i - len(range(seq[0],seq[1]))

        #Réinsertion des sommets dans l'ordre
        for j in range(len(sommets)):
            self.order.insert(i,sommets[j])

    #Méthode pour récupérer l'ordre avec le numéro de plateforme au début et fin
    def get_full_order(self):
        order = [self.origin]
        for sommet in self.order:
            order.append(sommet)
        order.append(self.origin)
        return order

    #Méthode pour calculer fonction objectif de la tournée
    def calc_obj_tournee(self, c:list):
        obj = 0
        obj += c[self.origin][self.order[0]] + c[self.origin][self.order[-1]]
        for i in range(len(self.order)-1):
            obj += c[self.order[i]][self.order[i+1]]
        return obj
    
    #Methodes d'affichage + sauvegarde

    def print_tournee(self):
        print("Tournee origine "+str(self.origin)+", taille "+str(self.size)+", load "+str(self.load)+ ", order = "+str(self.order))


    def tournee_to_dict(self):
        tournee_dict = {}
        tournee_dict["origin"] = self.origin
        tournee_dict["order"] = self.order
        tournee_dict["size"] = self.size
        tournee_dict["load"] = self.load
        return tournee_dict
    
    def dict_to_tournee(self, d_t:dict):
        self.origin = d_t["origin"]
        self.order = d_t["order"]
        self.size =  d_t["size"]
        self.load = d_t["load"] 
    

        
