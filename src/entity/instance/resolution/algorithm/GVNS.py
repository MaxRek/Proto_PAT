from..struct.solution import Solution
from..struct.sub_data import Sub_data
from..algorithm.Neighboorhoods import *

def GVNS(data:Sub_data, x : Solution, lim_calc:int):
    if x.verif_solution(data.C,data.N,data.Q):
        print("[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]v")
        print("Debut d'algorithme")
        print("Limite de calcul : "+str(lim_calc))
        count_calc = 0
        k_max = 5
        while count_calc < lim_calc:
            print("______________________________________________")
            print("Nb actuel de calcul effectues : "+str(count_calc))
            k = 0
            
            while k < k_max:
                if count_calc < lim_calc:
                    print("Voisinage exploré k : "+str(k))
                    xp = N4_intra(x,data)
                    temp = VND(data, xp, count_calc, lim_calc)
                    xpp = temp[0]
                    count_calc = temp[1]
                    if x.calc_func_obj(data.O,data.c) > xpp.calc_func_obj(data.O,data.c):
                        print("xpp meilleur Solution dans voisinage de x")
                        x = xpp
                        k = 0
                    else:
                        k += 1
                    count_calc += 1
                else:
                    k = k_max    
        print("Limite de calcul atteinte")
        print("[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]")

            
    return x

def VND(data:Sub_data, x : Solution, count_calc:int ,lim_calc:int):
    k_max = 5
    print("___________________________________")
    print("Début algo VND")
    
    while count_calc < lim_calc:
        k = 0
        
        while k < k_max:
            
            print("___________________________________")
            print("Nb actuel de calcul effectues : "+str(count_calc))
            if count_calc < lim_calc:
                print("Voisinage exploré k : "+str(k))
                e_N2_er = [-1,-1,[-1,-1],[-1,-1]]
                e_N3_ra = [-1,-1,-1,[[-1,-1],-1]]
                e_N3_er = [-1,-1,[-1,-1],[[-1,-1],-1]]
                e_N5 = [-1,-1]
                # xp = N2_inter(x,data, entry=e_N2_er)
                #xp = N4_intra(x,data, entry=e_N3_ra)
                #xp = N4_inter(x,data, entry=e_N3_er)
                xp = N5(x,data,e_N5)
                print(str(x.calc_func_obj(data.O,data.c)) + " > " + (str(xp.calc_func_obj(data.O,data.c))))
                
                if x.calc_func_obj(data.O,data.c) > xp.calc_func_obj(data.O,data.c):
                    print("xp meilleur Solution dans voisinage de x")
                    x = xp
                    k = 0
                else:
                    print("Nouveau voisinage de x")
                    k += 1
                count_calc += 1
            else:
                k = k_max

    return (x, count_calc)

def new_voisin(x):
    return x