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
        if len(o) != n and len(d) != c and len(d[0]) != f and len(S) != p and len(t) != n and len(t[0]) != fs and fp < fs :
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
        else:
            print("Erreur d'initialisation, problème impossible")
        