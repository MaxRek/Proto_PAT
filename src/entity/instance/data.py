import numpy as np

class Data:
    N:int
    C:int
    P:int
    K:int
    F:int
    Fs:int
    Fp:int
    Q:int
    O:list
    d:np.matrix
    S:np.matrix
    c:np.matrix
    t:np.matrix

    def __init__(self, n:int,c:int,p:int,k:int,f:int,fp:int,fs:int,q:int,o:list,d:np.matrix,S:np.matrix,ct:np.matrix,t:np.matrix) -> None:
        # if len(o) != n and len(d) != c and len(d[0]) != f and len(S) != p and len(t) != n and len(t[0]) != fs and fp < fs :
            self.N = n
            self.C = c
            self.P = p
            self.K = k
            self.F = f
            self.Fs = fs
            self.Fp = fp
            self.Q = q
            self.O = o
            self.d = d
            self.S = S
            self.c = ct
            self.t = t
        # else:
        #     print("Erreur d'initialisation, problème impossible")
        
    def save_data(self, path, name):
        writer = open(path+name+".txt",'w')
        writer.write(str(self.N)+"\n")
        writer.write(str(self.C)+"\n")
        writer.write(str(self.P)+"\n")
        writer.write(str(self.K)+"\n")
        writer.write(str(self.F)+"\n")
        writer.write(str(self.Fs)+"\n")
        writer.write(str(self.Fp)+"\n")
        writer.write(str(self.Q)+"\n")
        writer.write(str(self.O)+"\n")
        writer.write(str(self.d.tolist())+"\n")
        writer.write(str(self.S.tolist())+"\n")
        writer.write(str(self.c.tolist())+"\n")
        writer.write(str(self.t.tolist()))
        writer.close()
