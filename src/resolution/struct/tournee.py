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

    def add_point(self,points:list,QT_recup:list,ind:int = -1):
        s = len(points)
        # Modification de l'ordre
        if ind == -1:
            for i in range(s):
                self.order.insert(self.size,points[i])
                self.size += 1
                self.load += QT_recup[i]
        elif ind >= 0 and ind < len(self.order):
            self.order.insert(ind,points)
            self.size += 1
        else:
            print("Erreur : ind n'est pas une valeur correcte : "+str(ind))

    def del_point(self, points:list):
        for point in points:
            if point in self.order:
                self.order.remove(point)
                self.size -= 1                    

    def calc_load(self, reduce_LfnPT:tuple):
        self.load = 0
        for i in self.order:
            if i in reduce_LfnPT[0]:
                self.load += reduce_LfnPT[1][reduce_LfnPT[0].index(i)]

    def insert_sommet(self, s:int, i:int):
        self.size += 1
        self.order.insert(i,s)


    #Mouvement d'insertion N1_intra: 
    def reinsert(self, i:int, j:int):
        s = self.order.pop(i)
        # if j > i:
        #     j -=1
        self.order.insert(j,s)

    #Mouvement d'insertion N1_intra
    #pop un sommet dans l'ordre
    def pop(self, i:int):
        self.size -= 1
        s = self.order.pop(i)
        return s 
    
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
        temp = self.order[i]
        self.order[i] = self.order[j]
        self.order[j] = temp

    #Mouvement de EXTENDED OR_OPT N3_intra
    def extended_or_opt(self, seq:list, i:int):
        sommets = self.order[seq[0]:seq[1]+1]

        for s in sommets:
            self.order.pop(seq[0])

        if i > seq[-1]:
            i = i - len(range(seq[0],seq[1]))

        for j in range(len(sommets)):
            self.order.insert(i,sommets[-1*(j+1)])

    #Mouvement de EXTENDED OR_OPT N3_inter
    def insert_seq_or_opt(self, seq:list, i:int):
        for j in range(len(seq)):
            self.order.insert(i,seq[-1*(j+1)])
            self.size += 1

    #Mouvement de INVERSE OR_OPT N3_intra
    def inverse_or_opt(self, seq:list, i:int):
        sommets = self.order[seq[0]:seq[1]+1]

        for s in sommets:
            self.order.pop(seq[0])

        if i > seq[-1]:
            i = i - len(range(seq[0],seq[1]))

        for j in range(len(sommets)):
            self.order.insert(i,sommets[j])


    def print_tournee(self):
        print(str(self.order) + " " + str(self.load))

    def get_full_order(self):
        order = [self.origin]
        for sommet in self.order:
            order.append(sommet)
        order.append(self.origin)
        return order

    def print_tournee(self):
        print("Tournee origine "+str(self.origin)+", taille "+str(self.size)+", load "+str(self.load)+ ", order = "+str(self.order))

    def calc_obj_tournee(self, c:list):
        obj = 0
        # print("_______")
        obj += c[self.origin][self.order[0]] + c[self.origin][self.order[-1]]
        # print(str(c[self.origin][self.order[0]]) + " " + str(c[self.origin][self.order[-1]]))
        for i in range(len(self.order)-1):
            obj += c[self.order[i]][self.order[i+1]]
            #print(c[self.order[i]][self.order[i+1]])
        # print("_______")
        # print(obj)
        # print("_______")s
        return obj
    
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
    

        
