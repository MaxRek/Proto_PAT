import numpy as np

class Dec:

    xnc:list
    xnp:list
    w:np.matrix
    y:list
    L:list
    l:list
    AFP:list
    AFS:np.matrix
    T:list

    def __init__(self, c:int, n:int, p:int, k:int, f:int, f_p:int) -> None:
        
        #x_{i,j}^k
        self.xnc = list()
        self.xnp = list()
        for i in range(k):
            self.xnc.append(np.zeros((n+c,n+c)))
            self.xnp.append(np.zeros((n+p,n+p)))

        #w_{c,n}
        self.w = np.zeros((c,n))

        #y_n
        self.y = np.zeros(n)

        #L_{p,n}
        self.L = list()
        self.L.append(np.zeros((p,n)))
            
        #l_{p,n}^{k,f}
        self.l = list()
        for i in range(k):
            self.l.append(list())
            for j in range(f):
                self.l[i].append(np.zeros((p,n)))

        #AFP_k
        self.AFP = np.zeros(k)

        #AFS_{k,f}
        self.AFS = np.zeros((k,f))

        #T_{f,f'}^n
        self.T = np.zeros((n,f_p))



    def print_x(self):
        for i in range(len(self.xnc)):
            print("____________________________________\nVehicule " + str(i))
            print("Collecte")
            print(self.xnc[i])
            print("Livraison")
            print(self.xnp[i])

    def print_y(self):
        print("Plateformes ouvertes : ")
        print(self.y)

    def print_w(self):
        print("Assignations de clients aux plateformes : ")
        print(self.w)
    
    def print_L(self):
        print("Assignations de fournisseurs aux plateformes : ")
        print(self.L)

    def print_l(self):
        for i in range(len(self.l)):
            print("____________________________________\n Chargement du Véhicule " + str(i)+ " :")
            for j in range(len(self.l[i])):
                print("Chargement du produit " + str(j) + " :")
                print(self.l[i][j])

    def print_AFP(self):
        vec = []
        for i in range(len(self.AFP)):
            if self.AFP[i] == 1:
                vec.append(i)
        print("Vehicules assignes pour produits propres : "+str(vec))

    def print_AFS(self):
        vec = []
        for i in range(len(self.AFS)):
            for j in range(len(self.AFS[i])):
                if self.AFP[i] == 1:
                    vec.append(i)
            print("Vehicules assignes pour produit " +str(j)+ " : "+str(vec))
                
    def print_T(self):
        for i in range(len(self.T)):
            print("Quantites de produit "+str(len(self.T[i]))+" transforme par plateforme "+str(i)) 

    def print_dec(self):
        self.print_y()
        print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
        self.print_w()
        print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
        self.print_L()
        print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
        self.print_AFP()
        self.print_AFS()
        print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
        self.print_l()
        print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
        self.print_x()
        print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
        self.print_T()




