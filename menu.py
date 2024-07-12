from src.constant import RATIO_FILIERE_PROD, RATIO_PROD_DEMAND, MULT_DEMAND, MULTI_FILIERES ,NAME_CSV_E_GEN, NAME_CSV_F_GEN,A_NAME_CSV,CONSOMMATION_VEHICULE, TARIF_HORAIRE_HT, PRIX_ESSENCE,COUT_METRE_CARRE, NB_METRE_CARRE, ECART_PRIX_PLAT, RATIO_AMORTISSEMENT, PATH_IN, PATH_INSTANCE, NAME_CSV_D,NAME_CSV_E,NAME_CSV_F,NAME_CSV_N,NAME_CSV_T,NAME_DATA, A_FIELDS_E,A_FIELDS_F,A_FIELDS_N, A_FIELDS_T, FIELDS_D
from src.entity.instance.instance import Instance
from src.scripts.demandFiller import gen_O, gen_c_time, genDemand, genFill, gen_E_Demand
from src.scripts.findLatLong import replaceLatLong
from src.entity.aff import Aff
from src.entity.df import Df
import os
import pandas as pd
from copy import deepcopy



def control_verif_instance():
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print("               Projet Alimentaire Territoriale - Presqu'île, Brière, Estuaires")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")
    print("                   Contrôleur des instances utilisées pour la résolution")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

    stop = False

    while not stop:
        instances = detect_instance(PATH_IN+"/"+PATH_INSTANCE)
        print_str = ""
        if len(instances) > 0 : 
            print_str = str(len(instances)) + " instance(s) détéctée(s) : "+str(instances)+ "\n Voulez-vous vérifier une de ces instances ? \n 0 pour Non, \n 1 pour Oui"
            i = input_int(print_str,1,0)
            while i == 1:
                print_str = "Quelle instance ?"
                for instance in range(len(instances)):
                    print_str += "\n -  "+str(instance)+" pour instance \""+str(instances[instance])+"\","
                print_str += "\n - -1 pour annuler."
                j = input_int(print_str,len(instances),-1)
                
                if j == -1:
                    i = 0
                else:
                    inst = Instance(instances[j])
                    path = PATH_IN+"/"+PATH_INSTANCE+"/"+inst.name+"/"
                    flags_tab, str_error = inst.check_tableurs()
                    print(flags_tab)
                    print_str = str_check_tableurs(flags_tab, str_error)
                    
                    if(print_str ==""):
                        print("Aucun problème de tableur")
                    else:
                        print(print_str)
                    
                    control_gen_tab(path, flags_tab, inst)
                    
                    flags_data = inst.check_data()
                    print("----------------")
                    print(flags_data)
                    if flags_data != 0:
                        if flags_data != []:    
                            print_str = str_check_data(flags_data)
                            print(print_str)
                            control_gen_data(path,flags_data,flags_tab,inst)            
                            
                        else:
                            print("Les données dans "+NAME_DATA+" sont correctes")
                    else:
                        print("Le fichier "+NAME_DATA+" n'est pas présent dans " + path)

                    if(len(flags_tab) == 5):
                        if(sum(flags_tab[2])<=4 and flags_tab[4]):
                            print("Instance prête pour résolution, modifier main.py pour pouvoir l'utiliser")                    
        else:
            print_str = "Aucune instance détéctée, voulez-vous créer un fichier dans lequel vous pourrez insérez les tableurs ?\n 0 pour Non, \n 1 pour Oui"
            i = input_int(print_str,1,0)
            if i == 1:
                print_str = "Veuillez entrez un nom (sans caractère spécial, ni accent), -1 pour annuler"
                name = input_str(print_str, -1)
                if name == -1 :
                    print("Annulation de création d'instances")
                else:
                    os.mkdir(PATH_IN+"/"+PATH_INSTANCE+"/"+str(name))
        i = input_int("Fin de programme ? 1 pour Oui, 0 pour Non",1,0)  
        if i == 1:
            stop = True
        

def control_gen_tab(path:str, flags_tab:list, inst : Instance):
    tabs = A_NAME_CSV
    #Génération pour les colonnes x et y
    for tab in range(4):
        if not flags_tab[1][tab]:
            if flags_tab[2][tab] == 2:
                str_ques = "Générer les colonnes [\"x\",\"y\"] pour "+tabs[tab]+" ?\n"
                str_ques += "0 - Non\n"
                str_ques += "1 - Oui\n"
                i = input_int(str_ques, 1,0)
                if i == 1:
                    print(tabs[tab])
                    print(tab)
                    tab_data, code = replaceLatLong(path, tabs[tab])
                    if code != 403:
                        aff = Aff()
                        df = Df()
                        if tab == 0:
                            df.E = tab_data
                        elif tab == 1:
                            df.F = tab_data
                        elif tab == 2:
                            df.N = tab_data
                        elif tab == 3:
                            df.T = tab_data
                        aff.add_point(df)
                        aff.M.save(path+"/"+tabs[tab]+"_verif.html")

    #Génération de commandes (toutes les générations à faire):
    gen_d = False
    if not flags_tab[3]:
        gen_d = True
    elif not flags_tab[4]:
        gen_d = True

    if gen_d:
        files_gen = [NAME_CSV_E_GEN, NAME_CSV_F_GEN]
        flag_files = []
        files = os.listdir(path)
        for file in files_gen:
            if file+".csv" in files:
                flag_files.append(True)
            else:
                flag_files.append(False)
        str_info = str_gen_demand(flag_files)
        print(str_info)
        print(flag_files)
        if not flag_files[0] or flag_files[1]:
            i = 0
            while i !=-1 and (not flag_files[0] or not flag_files[1]):
                j = 0
                str_ques = "Tableur suivant à générer :\n"
                if not flag_files[0]:
                    str_ques += "  - "+str(j)+" Estimation de la demande des cantines\n"
                    j += 1
                if not flag_files[1]:
                    str_ques += "  - "+str(j)+" Affectation des fillières aux producteurs\n"
                str_ques += "  - -1 Retour en arrière"
                i = input_int(str_ques, 1,-1)

                if i == 0:
                    if not flag_files[0]:
                        mult = MULT_DEMAND
                        j = 0
                        while j != -1:
                            str_ques = "Demande d'une cantine définie par :\n"
                            str_ques += "Multiplicateur = "+str(mult)+"\n"
                            str_ques += "Le modifier ? 0 pour Oui, -1 pour non"
                            j = input_int(str_ques,0,-1)
                            if j == 0:
                                diviseur = 0
                                while diviseur != -1:
                                    diviseurs = [10,36]
                                    diviseur = input_int("multiplicateur défini par mois ouvrables (0) ou par semaine ouvrables (1), -1 pour annuler ?",1,-1)
                                    if diviseur != -1:
                                        temp = input_float("Inserez pourcentage (ex : 0,75 pour 75\% d'une unité), pour une unité : "+str(diviseurs[diviseur])+" unités maximum, -1 pour annuler: ", diviseurs[diviseur], -1)
                                        if temp != -1:
                                            mult = temp/diviseurs[diviseur]
                                            diviseur = -1
                                        else:
                                            print("Multiplicateur non modifié")
                                    else:
                                        print("Multiplicateur non modifié")
                        print("Génération selon multiplicateur fourni ")
                        gen_E_Demand(path, NAME_CSV_E,mult=mult, nameFile= NAME_CSV_E_GEN)
                        flag_files[0] = True
                    else:
                        j = 0
                        param = [MULTI_FILIERES,RATIO_FILIERE_PROD]
                        while j != -1:
                            str_info = "Affectation des filières aux producteurs selon :\n"
                            str_info += "  - 0 Chance d'affectation à une autre filière = " + str(param[0]) + "\n"
                            str_info += "  - 1 Répartition des affectations aux filières = " + str(param[1]) + "\n"
                            str_info += "Modifier un paramètre ? De 0 à 1, -1 pour annuler : "
                            j = input_int(str_info,1,-1)
                            if j == 0:
                                temp = input_float("Inserez chance d'affectation, de 0 à 1, -1 pour annuler: ", 1, -1)
                                if temp != -1:
                                    param[0] = temp
                                else:
                                    print("Chance d'affectation non modifiée")
                            elif j == 1:
                                k = 0
                                temp = 0
                                temp_array = []
                                while temp != -1 and k < len(list(inst.prod.keys())):
                                    temp = input_float("Inserez pourcentage pour produit n"+str(i)+" sur "+str(len(list(inst.prod.keys())))+", -1 pour annuler: ", 1, -1)
                                    if temp != -1:
                                        temp_array.append(temp)
                                        k += 1
                                    
                                if temp == -1:
                                    print("Répartition des affectations aux filières non modifiée")
                                else:
                                    if sum(temp_array) != 1:
                                        print("Répartition n'étant pas égale à 1 : "+str(temp_array)+" = "+str(sum(temp_array))+" ,abandon de modifications")
                                    else:
                                        param[1] = deepcopy(temp_array)

                        print("Génération des Affectation des filières aux producteurs")
                        genFill(path, NAME_CSV_F, NAME_CSV_F_GEN, param[0], param[1], inst.prod)                
                        flag_files[1] = True

                elif i == 1:
                    k = 0
                    param = [MULTI_FILIERES,RATIO_FILIERE_PROD]
                    while k != -1:
                        str_info = "Affectation des filières aux producteurs selon :\n"
                        str_info += "  - 0 Chance d'affectation à une autre filière = " + str(param[0]) + "\n"
                        str_info += "  - 1 Répartition des affectations aux filières = " + str(param[1]) + "\n"
                        str_info += "Modifier un paramètre ? De 0 à 1, -1 pour annuler : "
                        k = input_int(str_info,1,-1)
                        if k == 0:
                            temp = input_float("Inserez chance d'affectation, de 0 à 1, -1 pour annuler: ", 1, -1)
                            if temp != -1:
                                param[j] = temp
                            else:
                                print("Chance d'affectation non modifiée")
                        elif k == 1:
                            l = 0
                            temp = 0
                            temp_array = []
                            while temp != -1 and l< len(list(inst.prod.keys())):
                                temp = input_float("Inserez pourcentage pour produit n"+str(l)+" sur "+str(len(list(inst.prod.keys())))+", -1 pour annuler: ", 1, -1)
                                if temp != -1:
                                    temp_array.append(temp)
                                    l += 1
                                
                            if temp == -1:
                                print("Répartition des affectations aux filières non modifiée")
                            else:
                                if sum(temp_array) != 1:
                                    print("Répartition n'étant pas égale à 1 : "+str(temp_array)+" = "+str(sum(temp_array))+" ,abandon de modifications")
                                else:
                                    param[1] = deepcopy(temp_array)
                    
                    print("Génération des Affectation des filières aux producteurs")
                    genFill(path, NAME_CSV_F, NAME_CSV_F_GEN, param[0], param[1], inst.prod)
                    flag_files[1] = True

        if flag_files[0] and flag_files[1]:
            print("Possibilité de générer les demandes :")

            j = 0
            param = RATIO_PROD_DEMAND
            if len(param) != len(list(inst.prod.keys())):
                print("Paramètre enregistré non adaptés à l'instance, génération d'un paramètre basique")
                param = []
                for i in range(len(list(inst.prod.keys()))):
                    param.append(1)

            while j != -1:
                str_info = "Generation des demandes selon :\n"
                str_info += "Nombre de producteurs contactés par filières = " + str(param) + "\n"
                str_info += "Modifier un nombre de producteurs ? 0 pour oui, -1 pour annuler : "
                j = input_int(str_info,0,-1)
                if j == 0:
                    temp_array = []
                    temp = 1
                    i = 0
                    while temp != -1 and i< len(list(inst.prod.keys())):
                        temp = input_int("Inserez nb de producteur pour filière n"+str(i)+" sur "+str(len(list(inst.prod.keys())))+", 0 pour annuler: ", 10, 0)
                        if temp != 0:
                            temp_array.append(temp)
                            i += 1
                        
                        if temp == 0:
                            print("nb de producteur pour filière non modifiée")
                        else:
                            param = deepcopy(temp_array)

            print("Génération des commandes selon les paramètres fournies")
            genDemand(path,NAME_CSV_D,NAME_CSV_E_GEN,NAME_CSV_F_GEN,param, inst.prod)
        else:
            print("Fichies manquants pour génération des commandes, abandon")






def control_gen_data(path:str, flags_data:list, flags_tab:list, inst : Instance):
    print(flags_tab)
    print(flags_data)
    inst.data.load_data_txt(inst.name,PATH_IN+"/"+PATH_INSTANCE)
    not_gen = ["C", "P", "N", "T"]
    not_gen_str = ["nombre de plateforme","nombre de cantine","nombre de producteur","nombre de transformateur"]
    not_gen_tab = [NAME_CSV_E,NAME_CSV_F,NAME_CSV_N,NAME_CSV_T]
    not_gen_column = [A_FIELDS_E,A_FIELDS_F,A_FIELDS_N,A_FIELDS_T]

    for flag in flags_data:
        print(flag)

        if flag in not_gen:
            
            j = not_gen.index(flag)
            print(j)
            if flags_tab[0][j] and flags_tab[2][j]:
                str_ques = "Il est possible de générer "+not_gen_str[j]+" via le tableur associé. Récupérer ce nombre ? (recommandé)"
                str_ques += "\n0 - Non"
                str_ques += "\n1 - Oui"
                i = input_int(str_ques,1,0)
                if i == 1:
                    frame = pd.read_csv(path+not_gen_tab[j]+".csv",usecols=not_gen_column[j][flags_tab[2][j]],delimiter=";")
                    if j == 0:
                        inst.data.C = frame.shape[0]
                    elif j == 1:
                        inst.data.P = frame.shape[0]
                    elif j == 2:
                        inst.data.N = frame.shape[0]
                    elif j == 3:
                        inst.data.T = frame.shape[0]
                else:
                    str_ques = "Rentrer "+not_gen_str[j]+" manuellement ?"
                    str_ques += "\n0 - Non"
                    str_ques += "\n1 - Oui"
                    i = input_int(str_ques,1,0)
                    if i == 1:
                        inst.data.F = input_int("Inserez un nombre non négatif",1000000,-1)
                    else:
                        print(not_gen_str[j] + " non rentré.")
        elif flag == "F":
            str_ques = "Il est possible de générer nombre de produits via les informations enregistrées. Récupérer ce nombre ? (recommandé)"
            str_ques += "\n0 - Non"
            str_ques += "\n1 - Oui"
            i = input_int(str_ques,1,0)
            if i == 1:
                inst.data.F = len(list(inst.prod.keys()))
        elif flag == "Fs":
            str_ques = "Pour l'instant, il ne peut y avoir que les légumes en produit sales, affectation à 1"
            print(str_ques)
            inst.data.Fs = 1
        elif flag == "Fp":
            if inst.data.F !=0 and inst.data.Fs != 0:
                str_ques = "Il est possible de générer nombre de produits via F("+str(inst.data.F)+") - Fs ("+str(inst.data.Fs)+") = "+str(inst.data.F-inst.data.Fs)+" . Récupérer ce nombre ? (recommandé)"
                str_ques += "\n0 - Non"
                str_ques += "\n1 - Oui"
                i = input_int(str_ques,1,0)
                if i == 1:
                    inst.data.Fp = inst.data.F-inst.data.Fs
            else:
                str_ques = "Rentrer nombre de produits propres manuellement ?"
                str_ques += "\n0 - Non"
                str_ques += "\n1 - Oui"
                i = input_int(str_ques,1,0)
                if i == 1:
                    inst.data.Fp = input_int("Inserez un nombre non négatif",1000000,-1)
        elif flag == "Q":
            str_ques = "Capacité (en kg) pour tous les véhicules non renseignée, la saisir manuellement ?"
            str_ques += "\n0 - Non"
            str_ques += "\n1 - Oui"
            i = input_int(str_ques,1,0)
            if i == 1:
                temp  = input_int("Inserez un nombre non négatif",1000000,-1)
                if temp != 1 :
                    inst.data.Q = temp
        elif flag == "O":
            if flags_tab[0][3]:
                control_gen_O(inst)
            else:
                print("Rentrée des coûts d'ouverture impossible, le nombre de plateforme n'est pas renseigné.")
        elif flag == "c":
            if sum(flags_tab[0]) == 4 and sum(flags_tab[1]) == 4:
                control_gen_c_T(path,inst)
            else:
                print("Impossible de générer les coûts de transports, tableurs manquants ou incomplets")

    inst.data.save_data(PATH_IN+"/"+PATH_INSTANCE+"/", inst.name)

def control_gen_O(inst : Instance):
    O_gen = False
    if inst.data.N > 0:
        str_ques = "Coût d'ouverture pour les plateformes non trouvées, voulez-vous les générer ?"
        str_ques += "\n0 - Non"
        str_ques += "\n1 - Oui"
        i = input_int(str_ques,1,0)
        if i == 1:
            param = [COUT_METRE_CARRE,NB_METRE_CARRE,ECART_PRIX_PLAT,RATIO_AMORTISSEMENT]
            while i ==1:
                str_info = "Cout d'ouverture défini par :\n"
                str_info += "  - 0 Prix au mètre carré = " + str(param[0]) + "\n"
                str_info += "  - 1 Nombre de mètre carré pour les plateformes = " + str(param[1]) + "\n"
                str_info += "  - 2 Ecart de prix entre les plateformes = " + str(param[2]) + "\n"
                str_info += "  - 3 Ratio ammortissement = " + str(param[3]) + "\n"
                str_info += "Modifier un paramètre ? De 0 à 3, -1 pour annuler : "
                j = input_int(str_info,3,-1)
                if j == -1:
                    i = 0
                elif j == 0:
                    temp = input_float("Inserez prix au mètre carré, -1 pour annuler: ", 100000000, -1)
                    if temp != -1:
                        param[j] = temp
                    else:
                        print("Prix au mètre carré non modifié")
                elif j == 1:
                    temp = input_float("Inserez Nombre de mètre carré pour les plateformes, -1 pour annuler: ", 100000000, -1)
                    if temp != -1:
                        param[j] = temp
                    else:
                        print("Nombre de mètre carré pour les plateformes non modifié")
                elif j == 2:
                    temp = input_float("Inserez écart en pourcentage (ex : 75,2), -1 pour annuler: ", 100, -1)
                    if temp != -1:
                        param[j] = temp
                    else:
                        print("Ecart pour les prix des plateformes non modifié")
                elif j == 3:
                    diviseurs = [12,52]
                    diviseur = input_int("Ratio défini par mois (0) ou par semaine (1), -1 pour annuler ?",1,-1)
                    if diviseur != -1:
                        temp = input_float("Inserez nb d'unités choisis, pour une année : "+str(diviseurs[diviseur])+" unités maximum, -1 pour annuler: ", diviseurs[diviseur], -1)
                        if temp != -1:
                            param[j] = temp/diviseurs[diviseur]
                        else:
                            print("Ratio ammortissement non modifié")
                    else:
                        print("Ratio amortissement non modifié")
            
            print("Fin des modifications : Génération de coûts selon les paramètres fournis")
            inst.data.O = gen_O(inst.data.N,param[0],param[1],param[2],param[3])
            O_gen = True
        
        if i == 0:
            str_ques = "Coût d'ouverture pour les plateformes non trouvées, voulez-vous saisir manuellement "+str(inst.data.N)+" coût d'ouverture ?"
            str_ques += "\n0 - Non"
            str_ques += "\n1 - Oui"
            i = input_int(str_ques,1,0)
            if i == 1:
                r = []
                j = 0
                temp = 0
                while len(r) < inst.data.N and temp != 1:
                    temp = input_float("Inserez une valeur positive pour la plateforme "+str(j)+", -1 pour annuler la saisie", 1000000000,-1)
                    if temp != -1:
                        r.append(temp)
                        j += 1
                    else:
                        print("Saisie interrompue")
                
                if len(r) == inst.data.N:
                    print("Affectation réussie")
                    inst.data.O = r
                    O_gen = True

    else:
        print("Nombre de plateformes non précisé, impossible de générer/saisir des données")

    return O_gen

def control_gen_c_T(path:str,inst:Instance):
    c_gen = False
    if(inst.data.C > 0 and inst.data.N>0 and inst.data.P>0 and inst.data.T>0):
        str_ques = "Coût des transports non trouvées, voulez-vous les générer ?"
        str_ques += "\n0 - Non"
        str_ques += "\n1 - Oui"
        i = input_int(str_ques,1,0)
        if i == 1:
            param = [CONSOMMATION_VEHICULE,TARIF_HORAIRE_HT, PRIX_ESSENCE]
            i = 1
            while i ==1:
                str_info = "Cout de transport d'un point A à B défini par :\n"
                str_info += "  - 0 Consommation d'un véhicule pour 100km en litres = " + str(param[0]) + "\n"
                str_info += "  - 1 Tarif horaire pour le chauffeur en euro/heure = " + str(param[1]) + "\n"
                str_info += "  - 2 Prix du carburant au litre = " + str(param[2]) + "\n"
                str_info += "Modifier un paramètre ? De 0 à 2, -1 pour annuler : "
                j = input_int(str_info,2,-1)
                if j == -1:
                    i = 0
                elif j == 0:
                    temp = input_float("Inserez Consommation d'un véhicule pour 100km en litres, -1 pour annuler: ", 100000000, -1)
                    if temp != -1:
                        param[j] = temp
                    else:
                        print("Consommation d'un véhicule pour 100km en litres non modifié")
                elif j == 1:
                    temp = input_float("Inserez Tarif horaire pour le chauffeur en euro/heure, -1 pour annuler: ", 100000000, -1)
                    if temp != -1:
                        param[j] = temp
                    else:
                        print("Tarif horaire pour le chauffeur en euro/heure non modifié")
                elif j == 2:
                    temp = input_float("Inserez Prix du carburant au litre, -1 pour annuler : ", 100, -1)
                    if temp != -1:
                        param[j] = temp
                    else:
                        print("Prix du carburant au litre non modifié")

            inst.data.df.load_csv(path,e_name=NAME_CSV_E,f_name=NAME_CSV_F,n_name=NAME_CSV_N,t_name=NAME_CSV_T)
            print("Fin des modifications : Génération des coûts de transports selon les paramètres fournis")
            if gen_c_time(inst,consommation=param[0],tarif_horaire=param[1],prix=param[2]):
                c_gen = True
    else:
        print("Les informations relatives aux différents acteurs (clients, plateformes, producteurs et transformateur) ne sont pas définies")
    
    return c_gen

def input_float(prompt,lim,exit):
    r = ''
    valid = False
    while not valid and r != exit:
        temp_r = input(prompt+"\n")
        if temp_r != "":
            try:
                r = float(temp_r)
                if r > lim:
                    print("Merci de donner un nombre ne dépassant pas "+str(lim)+ " ("+str(exit)+" pour quitter)")
                else:
                    valid = True
            except ValueError as ve:
                print("L'entrée " + str(temp_r) + " ne peut pas être converti, merci de donner un nombre ne dépassant pas "+str(lim)+ " ("+str(exit)+" pour quitter)")
        else:
            print("Merci de donner un nombre ne dépassant pas "+str(lim)+ " ("+str(exit)+" pour quitter)")
    return r

def input_int(prompt,lim,exit):
    r = ''
    valid = False
    while not valid and r != exit:
        temp_r = input(str(prompt)+"\n")
        if temp_r != "":
            try:
                r = int(temp_r)
                if r > lim:
                    print("Merci de donner un nombre ne dépassant pas "+str(lim)+ " ("+str(exit)+" pour quitter)")
                else:
                    valid = True
            except ValueError as ve:
                print("L'entrée " + str(temp_r) + " ne peut pas être converti, merci de donner un nombre ne dépassant pas "+str(lim)+ " ("+str(exit)+" pour quitter)")
        else:
            print("Merci de donner un nombre ne dépassant pas "+str(lim)+ " ("+str(exit)+" pour quitter)")
    return r

def input_str(prompt,exit):
    r = ''
    valid = False
    while not valid and r != exit:
        temp_r = input(prompt+"\n")
        if temp_r != "":
            r = str(temp_r)
            valid = True
        else:
            print("Merci de donner un nom sans caractères spéciaux, sans accent.")
    return r

def detect_instance(path:str):
    instances = []
    for item in os.listdir(path):
        print()
        if os.path.isdir(path+"/"+item):
            instances.append(item)
    return instances

def str_check_tableurs(flags:list, str_error : str):
    print_str = ""
    if flags[0][0] :
        if not flags[1][0]:
            if flags[2][0] == 2:
                print_str += "  - Tableur pour Etablissement manque des colonnes [\"x\", \"y\"], possibilité de les générer.\n"       
            elif flags[2][0]==3: #Donc égal à 3
                print_str += "  - Tableur pour Etablissement manque des colonnes [\"x\", \"y\"], nécéssite colonne [\"Adresse\"] pour générer.\n"       
            else:
                print_str += "  - Tableur pour Etablissement dont les colonnes ne sont pas reconnues\n"
    else:
        print_str += "  - Tableur pour Etablissement non trouvé, veuillez le nommer \""+NAME_CSV_E+".csv\"\n"
    if flags[0][1] :
        if not flags[1][1]:
            if flags[2][1] == 2:
                print_str += "  - Tableur pour Fournisseur manque des colonnes [\"x\", \"y\"], possibilité de les générer.\n"       
            elif flags[2][1] == 3: #Donc égal à 3
                print_str += "  - Tableur pour Fournisseur manque des colonnes [\"x\", \"y\"], nécéssite colonne [\"Adresse\"] pour générer.\n"
            else:
                print_str += "  - Tableur pour Fournisseur dont les colonnes ne sont pas reconnues\n"       
    else:
        print_str += "  - Tableur pour Fournisseur non trouvé, veuillez le nommer \""+NAME_CSV_F+".csv\"\n"

    if flags[0][2] :
        if not flags[1][2]:
            if flags[2][2] == 2:
                print_str += "  - Tableur pour Plateforme manque des colonnes [\"x\", \"y\"], possibilité de les générer.\n"       
            elif flags[2][2] == 3: #Donc égal à 3
                print_str += "  - Tableur pour Plateforme manque des colonnes [\"x\", \"y\"], nécéssite colonne [\"Adresse\"] pour générer.\"\n"       
            else:
                print_str += "  - Tableur pour Plateforme dont les colonnes ne sont pas reconnues\n"       
    else:
        print_str += "  - Tableur pour Plateforme non trouvé, veuillez le nommer \""+NAME_CSV_N+".csv\"\n"

    if flags[0][3] :
        if not flags[1][3]:
            if flags[2][3] == 2:
                print_str += "  - Tableur pour Transformateur manque des colonnes [\"x\", \"y\"], possibilité de les générer.\n"       
            elif flags[2][3] == 3: #Donc égal à 3
                print_str += "  - Tableur pour Transformateur manque des colonnes [\"x\", \"y\"], nécéssite colonne [\"Adresse\"] pour générer.\"\n"       
            else:
                print_str += "  - Tableur pour Transformateur dont les colonnes ne sont pas reconnues\n"       
    else:
        print_str += "  - Tableur pour Transformateur non trouvé, veuillez le nommer \""+NAME_CSV_T+".csv\"\n"

    if flags[3]:
        if not(flags[0][0] and flags[0][1] and flags[2][0]):
            print_str += "Tableur pour Commandes présent, mais ne peut être vérifié.\n"
        elif flags[4]:
            print_str += str_error
    else:
        print_str += "Tableur pour Commandes non présent, veuillez le nommer \""+NAME_CSV_D+".csv\"\n"

    return print_str

def str_check_data(missing_data:list):
    print_str = "Données manquantes : \n"
    if "N" in missing_data:
        print_str += "  - nombre de plateforme(s)\n"
    if "C" in missing_data:
        print_str += "  - nombre de cantine(s)\n"
    if "P" in missing_data:
        print_str += "  - nombre de producteur(s)\n"
    if "T" in missing_data:
        print_str += "  - nombre de transformateur(s)\n"
    if "F" in missing_data:
        print_str += "  - nombre de produits total\n"
    if "Fs" in missing_data:
        print_str += "  - nombre de produits sales au total\n"
    if "Fp" in missing_data:
        print_str += "  - nombre de produits propres au total\n"
    if "Q" in missing_data:
        print_str += "  - capacité des véhicules\n"
    if "O" in missing_data:
        print_str += "  - coût d'ouverture des plateformes\n"
    if "c" in missing_data:
        print_str += "  - coût des transports\n"
    if "time" in missing_data:
        print_str += "  - temps des transports\n"
    return print_str
   
def str_gen_demand(flags:list):
    str_info = ""
    if not flags[0]:
        if str_info == "":
            str_info = "Problème au niveau de la génération du tableur des demandes :\n"
        str_info += "  - Le tableur "+NAME_CSV_E_GEN+" n'est pas dans le dossier\n"
    if not flags[1]:
        if str_info == "":
            str_info = "Problème au niveau de la génération du tableur des demandes :\n"
        str_info += "  - Le tableur "+NAME_CSV_F_GEN+" n'est pas dans le dossier\n"
    if flags[1] and flags[0]:
        str_info ="Génération possible de demande pour le tableur"

control_verif_instance()