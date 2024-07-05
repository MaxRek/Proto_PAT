from ...entity.df import Df

import numpy as np

class Sub_data :
    N:int
    C:int
    P:int
    T:int
    index:list
    F:int
    TSp:list
    Q:int
    O:list
    D:list
    d:dict
    rev_d:dict
    c:list
    locations:list


    def __init__(self, n:int, C:int, p:int, f:int, tsp :list, Q:int, O:list ,D:list, d:dict, c:list, ind:list, df:Df) -> None:
        self.N = n
        self.C = C+self.N
        self.P = p+self.C
        self.T = 1+self.P

        self.F = f
        self.TSp = tsp
        self.Q = Q
        self.O = O
        self.D = D
        self.d = d
        self.c = c
        self.index = ind
        self.locations = []
        for i in range(df.N.shape[0]):
            self.locations.append((df.N.iloc[i]["x"],df.N.iloc[i]["y"]))

        for i in range(df.E.shape[0]):
            if(i in ind[0]):
                self.locations.append((df.E.iloc[i]["x"],df.E.loc[i]["y"]))

        print(df.F)
        print(ind[1])
        for i in range(df.F.shape[0]):
            if(i in ind[1]):
                print(i)
                self.locations.append((df.F.iloc[i]["x"],df.F.loc[i]["y"]))

        for i in range(df.T.shape[0]):
            self.locations.append((df.T.iloc[i]["x"],df.T.loc[i]["y"]))

        self.rev_d = {}
        for key in self.d.keys():
            # print(int(key))
            for key2 in self.d[key]:
                #print(key2)
                if key2 not in self.rev_d:
                    self.rev_d[key2] = {}
                if key not in self.rev_d[key2]:
                    self.rev_d[key2][key] = []
                for value in self.d[key][key2]:
                    self.rev_d[key2][key].append(value)
        #print(len(self.locations))

