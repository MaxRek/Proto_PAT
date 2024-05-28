import numpy as np
import json
import copy

class Dec:

    xnc:list
    xnp:list
    xsnp:list
    y:list
    wc:list
    wp:list
    wt:list

    def __init__(self, c:int, n:int, p:int, t:int) -> None:
        
        #x_{i,j}^k
        self.xnc = np.zeros((n+c,n+c),dtype=int).tolist()
        self.xnp = np.zeros((n+p+t,n+p+t),dtype=int).tolist()
        
        #xs
        self.xsnp = copy.copy(self.xnp)

        #y_n
        self.y = np.zeros(n).tolist()

        #wc_{c,n}
        self.wc = np.zeros((c,n),dtype=int).tolist()

        #wp_{p,n}
        self.wp = np.zeros((p,n),dtype=int).tolist()
            
        #wt_{t,n}
        self.wt = np.zeros((t,n),dtype=int).tolist()

    def load_dec(self, path:str, name:str):
        with(open(path+name+".json",'r')) as f:
            loaded = json.load(f)

        self.xnc = loaded["xnc"]
        self.xnp = loaded["xnp"]
        self.xsnp = loaded["xsnp"]
        self.y = loaded["y"]
        self.wc = loaded["wc"]
        self.wp = loaded["wp"]
        self.wt = loaded["wt"]

    def save_dec(self, path:str, name:str):
        to_write = dict()
        to_write["xnc"] = self.xnc
        to_write["xnp"] = self.xnp
        to_write["xsnp"] = self.xsnp
        to_write["y"] = self.y

        to_write["wc"] = self.wc
        to_write["wp"] = self.wp
        to_write["wt"] = self.wt

        with(open(path+name+".json",'w')) as f:
            f.write(json.dumps(to_write,indent=4,sort_keys=True))

    def print_x(self):
            print("Collecte")
            print(self.xnc)
            print("Collecte Sale")
            print(self.xsnp)
            print("Livraison")
            print(self.xnp)

    def print_y(self):
        print("Plateformes ouvertes : ")
        print(self.y)

    def print_w(self):
        print("Assignations de clients aux plateformes : ")
        print(self.w)
    
    
    def print_dec(self):
        self.print_y()
        print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
        self.print_w()
        print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
        self.print_x()


        



