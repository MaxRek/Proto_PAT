from..struct.solution import Solution
from copy import deepcopy

def next_voisin(x : Solution,k:int, entry:list = [-2]):
    #initialisation si entry n'est pas donné
    if entry[0] == -2:    
        entry = [-1]
    
    #Choix du voisin à aller récupérer
    if k == 0:
        #Si première fois qu'on explore selon ce type de voisinage, adaptation d'entry.
        if len(entry) == 1:
            entry = [entry[0],0,0,[0,0]]
        if entry[0] == -1:
            temp = N1_sales(x,entry)
        else:
            temp = N1_plat(x,entry[0],entry)
    elif k == 1:
        if len(entry) == 1:
            entry = [entry[0],0,0,[0,0]]
        if entry[0] == -1:
            temp = N2_sales(x,entry)
        else:
            temp = N2_plat(x,entry[0],entry)

    elif k == 2 or k == 3:
        if len(entry) == 1:
            entry = [entry[0],0,0,[[0,0],0]]
        if entry[0] == -1:
            temp = N34_sales(x,entry)
        else:
            temp = N34_plat(x,entry[0],entry)    

    return temp

def N1_sales(x:Solution,entry:list):
    #Debut itération, on varie sur les valeurs dans entry
    # INTRA EXPLORATION 
    next_found = False
    e = deepcopy(entry)
    i = 0
    while not next_found and entry[0] == -1:
        #Dans l'exploration des tournées de produits sales
        if type(e[2])==int:  
            #La tournée exploré peut avoir une réinsertion, sinon on itère sur la tournée suivante
            if e[2] < len(x.sales):
                #Si e[3][0] est dans la range -1, on essaye d'avancer e[3][1], sinon on change de tournée
                if e[3][0] in range(x.sales[e[2]].size-1):
                    #Si on peut avancer e[3][1], on le fait, sinon on avance
                    if e[3][1]+1 in range(e[3][0],x.sales[e[2]].size):
                        e[3][1] += 1
                        next_found = True

                    else:
                        e[3][0] += 1
                        e[3][1] = e[3][0]

                else:
                    e[2] += 1
                    e[3] = [0,0]
            else:
                    #Il est possible d'itérer sur plusieurs tournées
                    if len(x.sales) > 1:
                        e[2] = [0,1]
                        e[3] = [0,0]
                    else:
                        e = [0,0,0,[0,0]]

        #INTER EXPLORATION     
        elif type(e[2])== list:
            
            #Il a déjà été vérifié qu'il existe deux tournées, on ne vérifie plus la longueur de chaque tournée
            #Aussi contrairement à INTRA, on doit essayer chaque sommet d'une tournée vers les autres tournées.
            # print(x.sales[e[2][0]].size)
            # print(x.sales[e[2][1]].size)
            if e[2][0]< len(x.plat):
                if e[2][1] < len(x.plat) and e[2][1] != e[2][0]:
                    #On modifie l'index de destination dans la tournée de destination, sinon dans l'origine, et sinon on modifie la tournée de destination
                    if e[3][1] + 1 in range(x.sales[e[2][1]].size):
                        e[3][1] += 1
                        next_found = True
                    else:
                        if e[3][0] +1 in range(x.sales[e[2][0]].size):
                            e[3][0] += 1
                            e[3][1] = -1
                        else:
                            e[2][1] += 1
                            e[3] = [0,-1]
                else:
                    #Si il y a une tournée en plus, on itère dessus, sinon on change tournée d'origine
                    if e[2][1] == e[2][0]:
                        e[2][1] += 1
                    else:
                        e[2][0] = e[2][0] + 1
                        e[2][1] = 0
                        e[3] = [0,-1] 
                #fin d'itération pour la collecte sale, nous passons aux plateformes
            else:
                e = [0,0,0,[0,0]]
                
        i += 1
    #print(next_found)
    #print("______________")
    return [x, e, next_found]

def N1_plat(x:Solution, p:int, entry:list):
    next_found = False
    e = deepcopy(entry)
    #Exploration des plateformes, INTRA
    while not next_found and e[0] == p:
        if type(e[2]) == int:
            if e[0] == p:
                #itération sur les Tournées de collecte ou de livraison
                if e[1] < 2:
                    #print(len(x.plat[e[0]].tournees[e[1]]))
                    #La tournée explorée existe
                    if e[2] < len(x.plat[e[0]].tournees[e[1]]):
                        #print(x.plat[e[0]].tournees[e[1]][e[2]].size)
                        #Si e[3][0] est dans la range -1, on essaye d'avancer e[3][1], sinon on change de tournée
                        if e[3][0] in range(x.plat[e[0]].tournees[e[1]][e[2]].size-1):
                            #Si on peut avancer e[3][1], on le fait, sinon on avance
                            if e[3][1]+1 in range(e[3][0],x.plat[e[0]].tournees[e[1]][e[2]].size):
                                e[3][1] += 1
                                next_found = True

                            else:
                                e[3][0] += 1
                                e[3][1] = e[3][0]
                        else:
                            e[2] += 1
                            e[3] = [0,-1]
                    else:
                        e[1]+= 1
                        e[2]=0
                        e[3] = [0,-1]
                else:
                    #On vérifie si on ne peut pas bouger selon plusieurs plateformes
                    e[1] = 0
                    if len(x.plat[e[0]].tournees[e[1]]) > 1:
                        e[2] = [0,1]
                        e[3] = [0,-1]
                    else:
                        e[0] += 1
                        e[2] = [0,1]
                        e[3] = [0,-1]
                
            
        #INTER EXPLORATION     
        elif type(e[2])== list :
            #Il a déjà été vérifié qu'il existe deux tournées, on ne vérifie plus la longueur de chaque tournée
            #Aussi contrairement à INTRA, on doit essayer chaque sommet d'une tournée vers les autres tournées.
            if e[0] < len(x.plat):
                if e[1] < 2:
                    if e[2][0] < len(x.plat[e[0]].tournees[e[1]]):
                        if e[2][1] < len(x.plat[e[0]].tournees[e[1]]) and e[2][1] != e[2][0]:
                        #On modifie l'index de destination dans la tournée de destination, sinon dans l'origine, et sinon on modifie la tournée de destination
                            if e[3][1] + 1 in range(x.plat[e[0]].tournees[e[1]][e[2][1]].size):
                                e[3][1] += 1
                                next_found = True
                            else:
                                if e[3][0] +1 in range(x.plat[e[0]].tournees[e[1]][e[2][0]].size):
                                    e[3][0] += 1
                                    e[3][1] = 0
                                else:
                                    e[2][1] += 1
                                    e[3] = [0,-1]
                        else:
                            #Si il y a une tournée en plus, on itère dessus, sinon on change tournée d'origine
                            if e[2][1] == e[2][0]:
                                e[2][1] += 1
                                e[3] = [0,-1]
                            else:
                                if e[2][1] not in range(len(x.plat[e[0]].tournees[e[1]])):
                                    e[2][0] += 1
                                    e[2][1] = 0
                                    e[3] = [0,-1]
                    else:
                        e[1] += 1
                        e[2][0] = 0
                        e[2][1] = 1
                        e[3] = [0,-1]
                else:
                    e[0]+= 1
                    e[1] = 0
                    e[2] = 0
                    e[3] = [0,0]
            else:
                e[0]+= 1
                e[1] = 0
                e[2] = 0
                e[3] = [0,0]

    return [x, e, next_found]

def N2_sales(x:Solution, entry:list):
    #Debut itération, on varie sur les valeurs dans entry
    # INTRA EXPLORATION 
    next_found = False
    e = deepcopy(entry)
    i = 0
    while not next_found and entry[0] == -1:
        #Dans l'exploration des tournées de produits sales
        if type(e[2])==int:  
            #La tournée exploré peut avoir une réinsertion, sinon on itère sur la tournée suivante
            if e[2] < len(x.sales):
                #Si e[3][0] est dans la range -1, on essaye d'avancer e[3][1], sinon on change de tournée
                if e[3][0] in range(x.sales[e[2]].size-1):
                    #Si on peut avancer e[3][1], on le fait, sinon on avance
                    if e[3][1]+1 in range(e[3][0],x.sales[e[2]].size):
                        e[3][1] += 1
                        next_found = True

                    else:
                        e[3][0] += 1
                        e[3][1] = e[3][0]

                else:
                    e[2] += 1
                    e[3] = [0,0]
            else:
                    #Il est possible d'i
                    # térer sur plusieurs tournées
                    if len(x.sales) > 1:
                        e[2] = [0,1]
                        e[3] = [0,0]
                    else:
                        e[0] += 1
                        e[2] = 0
                        e[3] = [0,0]

        #INTER EXPLORATION     
        elif type(e[2])== list:
            
            #Il a déjà été vérifié qu'il existe deux tournées, on ne vérifie plus la longueur de chaque tournée
            #Aussi contrairement à INTRA, on doit essayer chaque sommet d'une tournée vers les autres tournées.
            # print(x.sales[e[2][0]].size)
            # print(x.sales[e[2][1]].size)
            if e[2][0]< len(x.plat):
                if e[2][1] < len(x.plat) and e[2][1] != e[2][0]:
                    #On modifie l'index de destination dans la tournée de destination, sinon dans l'origine, et sinon on modifie la tournée de destination
                    if e[3][1] + 1 in range(x.sales[e[2][1]].size):
                        e[3][1] += 1
                        next_found = True
                    else:
                        if e[3][0] +1 in range(x.sales[e[2][0]].size):
                            e[3][0] += 1
                            e[3][1] = -1
                        else:
                            e[2][1] += 1
                            e[3] = [0,-1]
                else:
                    #Si il y a une tournée en plus, on itère dessus, sinon on change tournée d'origine
                    if e[2][1] == e[2][0]:
                        e[2][1] += 1
                    else:
                        e[2][0] = e[2][0] + 1
                        e[2][1] = 0
                        e[3] = [0,-1] 
                #fin d'itération pour la collecte sale, nous passons aux plateformes
            else:
                e = [0,0,0,[0,0]]
                
        i += 1
    #print(next_found)
    #print("______________")
    return [x, e, next_found]

def N2_plat(x:Solution, p:int ,entry:list):
    next_found = False
    e = deepcopy(entry)

    #Exploration des plateformes, INTRA
    while not next_found and e[0] == p:
        if type(e[2]) == int:
            if e[0] < len(x.plat):
                #itération sur les Tournées de collecte ou de livraison
                if e[1] < 2:
                    #print(len(x.plat[e[0]].tournees[e[1]]))
                    #La tournée explorée existe
                    if e[2] < len(x.plat[e[0]].tournees[e[1]]):
                        #print(x.plat[e[0]].tournees[e[1]][e[2]].size)
                        #Si e[3][0] est dans la range -1, on essaye d'avancer e[3][1], sinon on change de tournée
                        if e[3][0] in range(x.plat[e[0]].tournees[e[1]][e[2]].size-1):
                            #Si on peut avancer e[3][1], on le fait, sinon on avance
                            if e[3][1]+1 in range(e[3][0],x.plat[e[0]].tournees[e[1]][e[2]].size):
                                e[3][1] += 1
                                next_found = True

                            else:
                                e[3][0] += 1
                                e[3][1] = e[3][0]
                        else:
                            e[2] += 1
                            e[3] = [0,-1]
                    else:
                        e[1]+= 1
                        e[2]=0
                        e[3] = [0,-1]
                else:
                    #On vérifie si on ne peut pas bouger selon plusieurs plateformes
                    e[1] = 0
                    if len(x.plat[e[0]].tournees[e[1]]) > 1:
                        e[2] = [0,1]
                        e[3] = [0,-1]
                    else:
                        e[0] += 1
                        e[2] = [0,1]
                        e[3] = [0,-1]
                
            
        #INTER EXPLORATION     
        elif type(e[2])== list:
            #Il a déjà été vérifié qu'il existe deux tournées, on ne vérifie plus la longueur de chaque tournée
            #Aussi contrairement à INTRA, on doit essayer chaque sommet d'une tournée vers les autres tournées.
            if e[0] < len(x.plat):
                if e[1] < 2:
                    if e[2][0] < len(x.plat[e[0]].tournees[e[1]]):
                        if e[2][1] < len(x.plat[e[0]].tournees[e[1]]) and e[2][1] != e[2][0]:
                        #On modifie l'index de destination dans la tournée de destination, sinon dans l'origine, et sinon on modifie la tournée de destination
                            if e[3][1] + 1 in range(x.plat[e[0]].tournees[e[1]][e[2][1]].size):
                                e[3][1] += 1
                                next_found = True
                            else:
                                if e[3][0] +1 in range(x.plat[e[0]].tournees[e[1]][e[2][0]].size):
                                    e[3][0] += 1
                                    e[3][1] = 0
                                else:
                                    e[2][1] += 1
                                    e[3] = [0,-1]
                        else:
                            #Si il y a une tournée en plus, on itère dessus, sinon on change tournée d'origine
                            if e[2][1] == e[2][0]:
                                e[2][1] += 1
                                e[3] = [0,-1]
                            else:
                                if e[2][1] not in range(len(x.plat[e[0]].tournees[e[1]])):
                                    e[2][0] += 1
                                    e[2][1] = 0
                                    e[3] = [0,-1]
                    else:
                        e[1] += 1
                        e[2][0] = 0
                        e[2][1] = 1
                        e[3] = [0,-1]
                else:
                    e[0]+= 1
                    e[1] = 0
                    e[2] = 0
                    e[3] = [0,0]
            else:
                e[0]+= 1
                e[1] = 0
                e[2] = 0
                e[3] = [0,0]

    return [x, e, next_found]

def N34_sales(x:Solution, entry:list):
    #Debut itération, on varie sur les valeurs dans entry
    # INTRA EXPLORATION 
    next_found = False
    e = deepcopy(entry)
    while not next_found and e[0] == -1:
        # print(e)

        #Dans l'exploration des tournées de produits sales
        if type(e[2])==int:  
            #Si e[3][0] est dans la range -1, on essaye d'avancer e[3][1], sinon on change de tournée
            if e[2] < len(x.sales):
                if e[3][0][0] < x.sales[e[2]].size-1:
                    #Si on peut avancer e[3][1], on le fait, sinon on avance la seq
                    if e[3][1]+1 in range(x.sales[e[2]].size):
                        if e[3][1] + 1 not in range(e[3][0][0],e[3][0][1]):
                            e[3][1] += 1
                            next_found = True
                        else:
                            e[3][1] = e[3][0][1]
                    else:
                        if e[3][0][1]+1 < x.sales[e[2]].size:
                            e[3][0][1] += 1
                            
                        else:
                            e[3][0][0] += 1 
                            e[3][0][1] = e[3][0][0] +1
                        e[3][1] = 0
                else:
                    # print(e)
                    if(len(x.sales) > 1):
                        e[2] = [e[2],0]
                        e[3] = [[0,1],0]
                    else:
                        e[2] += 1
                        e[3] = [[0,1],0]
                        if e[2] == len(x.sales):
                            e = [0,0,0,[[0,1],-1]]
                        

        #INTER EXPLORATION     
        elif type(e[2])== list:
            
            #Il a déjà été vérifié qu'il existe deux tournées, on ne vérifie plus la longueur de chaque tournée
            #Aussi contrairement à INTRA, on doit essayer chaque sommet d'une tournée vers les autres tournées.
            # print(x.sales[e[2][0]].size)
            # print(x.sales[e[2][1]].size)
            if e[2][0]< len(x.sales):
                if e[2][1] < len(x.sales) and e[2][1] != e[2][0]:
                    if e[3][0][0] < x.sales[e[2][0]].size-1:
                        #Si on peut avancer e[3][1], on le fait, sinon on avance la seq
                        if e[3][1]+1 in range(x.sales[e[2][1]].size):
                            e[3][1] += 1
                            next_found = True
                        else:
                            if e[3][0][1]+1 < x.sales[e[2][0]].size:
                                e[3][0][1] += 1
                                e[3][1] = 0

                            else:
                                e[3][0][0] += 1 
                                e[3][0][1] = e[3][0][0] +1
                                e[3][1] = 0
                    else:
                    #On modifie l'index de destination dans la tournée de destination, sinon dans l'origine, et sinon on modifie la tournée de destination
                        e[2][1] += 1
                        e[3] = [[0,1],0]
                else:
                    #Si il y a une tournée en plus, on itère dessus, sinon on change tournée d'origine
                    if e[2][1] == e[2][0]:
                        e[2][1] += 1
                    else:
                        e[2] = e[2][0] + 1
                        e[3] = [[0,1],0] 
                        if e[2] == len(x.sales):
                            e = [0,0,0,[[0,1],-1]]
                #fin d'itération pour la collecte sale, nous passons aux plateformes
            else:
                e = [0,0,0,[[0,1],-1]]
                
    #print(next_found)
    #print("______________")
    return [x, e, next_found]

def N34_plat(x:Solution, p:int ,entry:list):
    next_found = False
    e = deepcopy(entry)

    #Exploration des plateformes, INTRA
    while not next_found and e[0] == p:
        #print(e)
        #Dans l'exploration des tournées de produits sales
        if type(e[2])==int:
            if e[1] < 2:
                if e[2] < len(x.plat[e[0]].tournees[e[1]]):
                #Si e[3][0] est dans la range -1, on essaye d'avancer e[3][1], sinon on change de tournée
                    if e[3][0][0] < x.plat[e[0]].tournees[e[1]][e[2]].size-1:
                        #Si on peut avancer e[3][1], on le fait, sinon on avance la seq
                        if e[3][1]+1 in range(x.plat[e[0]].tournees[e[1]][e[2]].size):
                            if e[3][1] + 1 not in range(e[3][0][0],e[3][0][1]):
                                e[3][1] += 1
                                next_found = True
                            else:
                                e[3][1] = e[3][0][1]
                        else:
                            if e[3][0][1]+1 < x.plat[e[0]].tournees[e[1]][e[2]].size:
                                e[3][0][1] += 1
                            else:
                                e[3][0][0] += 1 
                                e[3][0][1] = e[3][0][0] +1
                    else:
                        e[2] += 1
                        e[3] = [[0,1],-1]
                else:
                    e[1] += 1
                    e[2] = 0
                    e[3] = [[0,1],0]
                    if(e[2] == len(x.plat)):
                        e[2] = [0,1]
                        e[3] = [[0,1],0]
            else:
                e[1] = 0
                if len(x.plat[e[0]].tournees[e[1]]) > 1:
                    e[2] = [0,1]
                    e[3] = [[0,1],-1]
                else:
                    e[0] += 1
                    e[2] = [0,1]
                    e[3] = [[0,1],-1]


        #INTER EXPLORATION     
        elif type(e[2])== list:
            
            #Il a déjà été vérifié qu'il existe deux tournées, on ne vérifie plus la longueur de chaque tournée
            #Aussi contrairement à INTRA, on doit essayer chaque sommet d'une tournée vers les autres tournées.
            # print(x.sales[e[2][0]].size)
            # print(x.sales[e[2][1]].size)
            if e[2][0]< len(x.plat):
                if e[2][1] < len(x.plat[e[0]].tournees[e[1]]) and e[2][1] != e[2][0]:
                    if e[3][0][0] < x.plat[e[0]].tournees[e[1]][e[2][0]].size-1:
                        #Si on peut avancer e[3][1], on le fait, sinon on avance la seq
                        if e[3][1]+1 in range(x.plat[e[0]].tournees[e[1]][e[2][1]].size):
                            e[3][1] += 1
                            next_found = True
                        else:
                            if e[3][0][1]+1 < x.plat[e[0]].tournees[e[1]][e[2][0]].size:
                                e[3][0][1] += 1
                                e[3][1] = 0

                            else:
                                e[3][0][0] += 1 
                                e[3][0][1] = e[3][0][0] +1
                                e[3][1] = 0
                    else:
                    #On modifie l'index de destination dans la tournée de destination, sinon dans l'origine, et sinon on modifie la tournée de destination
                        e[2][1] += 1
                        e[3] = [[0,1],0]
                else:
                    #Si il y a une tournée en plus, on itère dessus, sinon on change tournée d'origine
                    if e[2][1] == e[2][0]:
                        e[2][1] += 1
                    else:
                        e[2][0] = e[2][0] + 1
                        e[2][1] = 0
                        e[3] = [[0,-1],0] 
            else:
                e[0] = -2
    #print(next_found)
    #print("______________")
    return [x, e, next_found]