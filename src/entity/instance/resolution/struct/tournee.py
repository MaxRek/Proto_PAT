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
            for point in range(s):
                self.order.insert(self.size,points[point])
                self.size += 1
                self.load += QT_recup[point]
        elif ind >= 0 and ind < len(self.order):
            self.order.insert(ind,points)
            self.size += s
        else:
            print("Erreur : ind n'est pas une valeur correcte : "+str(ind))

    def del_point(self, points:list):
        s = 0
        if point != self.origin:
            for point in points:
                if point in self.order:
                    self.order.remove(point)
                    self.size -= 1

                    

    def print_tournee(self):
        print(str(self.order) + " " + str(self.load))
        
    def get_load(self):
        return self.load

    def get_full_order(self):
        order = [self.origin]
        for sommet in self.order:
            order.append(sommet)
        order.append(self.origin)
        return order

    def print_tournee(self):
        print("Tournee origine "+str(self.origin)+", taille "+str(self.size)+", capacity "+str(self.load)+ ", order = "+str(self.order))

    def calc_obj_tournee(self, c:list):
        obj = 0
        print("_______")
        obj += c[self.origin][self.order[0]] + c[self.origin][self.order[-1]]
        print(str(c[self.origin][self.order[0]]) + " " + str(c[self.origin][self.order[-1]]))
        for i in range(len(self.order)-1):
            obj += c[self.order[i]][self.order[i+1]]
            print(c[self.order[i]][self.order[i+1]])
        print("_______")
        print(obj)
        print("_______")


        return obj