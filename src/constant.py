APIKEY_OPENROUTE = '5b3ce3597851110001cf62483df00dfb4ccb4e8c91dc5e03a8263482'
PRIX_ESSENCE = 1.64
TARIF_HORAIRE_HT = 11.65
CONSOMMATION_VEHICULE = 9.5
ZOOM = 10
LOC_BRIERE = [47.37412011769598, -2.234728966487376]

#Path
PATH_IN = "in"
PATH_OUT = "out"
PATH_DATA = "data"
PATH_INSTANCE = "instance"
PATH_FILE_F = "Fournisseurs"
PATH_FILE_E = "Établissements"
PATH_FILE_N = "Entrepots"
PATH_FILE_T = "Transformateurs"
NAME_DATA = "data.txt"

NAME_CSV_E = "e"
NAME_CSV_F = "f"
NAME_CSV_N = "n"
NAME_CSV_T = "t"
A_NAME_CSV = [NAME_CSV_E,NAME_CSV_F,NAME_CSV_N,NAME_CSV_T]
NAME_CSV_E_GEN = NAME_CSV_E+"_demand"
NAME_CSV_F_GEN = NAME_CSV_F+"_prod"
NAME_CSV_D = "d"
#Dataframe
FIELDS_F_NG= ["Nom","Commune"]
FIELDS_F_GEN = ["Non","Adresse","Commune"]
FIELDS_F= ["Nom","x","y","Commune"]
FIELDS_F_FULL = ["Non","Adresse","Commune","x","y"]
A_FIELDS_F = [FIELDS_F_FULL, FIELDS_F, FIELDS_F_GEN, FIELDS_F_NG]

FIELDS_E_NG = ["Nom de la structure","Nombre de repas par jour","Commune","Domaine","Type de restauration"]
FIELDS_E_GEN = ["Nom de la structure","Adresse", "Nombre de repas par jour","Commune","Domaine","Type de restauration"]
FIELDS_E = ["Nom de la structure","x","y","Nombre de repas par jour","Commune","Domaine","Type de restauration"]
FIELDS_E_FULL = ["Nom de la structure","Adresse","x","y","Nombre de repas par jour","Commune","Domaine","Type de restauration"]
A_FIELDS_E = [FIELDS_E_FULL, FIELDS_E, FIELDS_E_GEN, FIELDS_E_NG]

SUB_FIELDS_E = ["Nom de la structure","Nombre de repas par jour","Commune"]

FIELDS_N_NG = ["Nom de la structure","Commune"]
FIELDS_N_GEN = ["Nom de la structure","Adresse","Commune"]
FIELDS_N = ["Nom de la structure","x","y","Commune"]
FIELDS_N_FULL = ["Nom de la structure","Adresse","x","y","Commune"]
A_FIELDS_N = [FIELDS_N_FULL, FIELDS_N, FIELDS_N_GEN, FIELDS_N_NG]


FIELDS_T_NG = ["Nom de la structure","Commune"]
FIELDS_T_GEN = ["Nom de la structure","Adresse","Commune"]
FIELDS_T = ["Nom de la structure","x","y","Commune"]
FIELDS_T_FULL = ["Nom de la structure","Adresse","x","y","Commune"]
A_FIELDS_T = [FIELDS_T_FULL, FIELDS_T, FIELDS_T_GEN, FIELDS_T_NG]


FIELDS_D = ["E","P","F","d"]

#Affichage
COLOR_PIN_F = "red"
COLOR_PIN_E = "blue"
COLOR_PIN_N = "black"
COLOR_PIN_T = "green"

#Generation
MULT_DEMAND = 1/36
MULTI_FILIERES = 0.4
RATIO_FILIERE_PROD = [0.4,0.4,0.1,0.1]
RATIO_PROD_DEMAND = [2,1,1,1]

DOMAINES = ["Education"]
DEMAND = {
    "Legumes" : [
        "Aubergine","Betterave","Carotte","Champignon","Chou","Concombre","Courgette","Navet","Oignon","Poireau","Pomme de terre","Botte de Radis","Salade","Tomate"
        ],  
    "Laitages" : [
        "Laits","Fromage","Yaourt","Fromage blanc","Crème","Flan Caramel"
        ], 
    "Fruits" : [
        "Pomme","Poire","Fraise","Melon","Pêche","Abricot","Raisin","Kiwi"
    ],
    "Viandes" : [
        "Bovine","Poulet","Canard","Porc","Lapin","Cordon bleu","Dinde","Jambon","Saucisse","Chipolata","Autres charcuteries","Poisson"
        ], 
    "Legumineuses" : [
        "Lentilles"
        ]
}
SUB_DEMAND = {
    "Legumes" : ["Aubergine","Betterave","Carotte","Chou","Concombre","Courgette","Navet","Oignon","Poireau","Pomme de terre","Botte de Radis","Salade","Tomate"], 
    "Laitages" : ["Lait"], 
    "Viandes" : ["Bovine"], 
    "Legumineuses" : ["Lentilles"]
}
COMMUNES = ["Assérac","Batz-sur-Mer","Besné","Camoël","Crossac","Donges","Drefféac","Férel","Guenrouët","Guérande","Herbignac","La Baule-Escoublac","La Chapelle-des-Marais","La Turballe","Le Croisic", "Le Pouliguen", "Mesquer", "Missillac","Montoir-de-Bretagne","Pénestin","Piriac-sur-Mer","Pontchâteau", "Pornichet" , "Prinquiau", "Saint-André-des-Eaux","Sainte-Anne-sur-Brivet","Saint-Gildas-des-Bois","Saint-Joachim","Saint-Lyphard","Saint-Malo-de-Guersac","Saint-Molf","Saint-Nazaire","Sainte-Reine-de-Bretagne","Sévérac","Trignac"]

COUT_METRE_CARRE = 1000.0
NB_METRE_CARRE = 200
ECART_PRIX_PLAT = 0.3
RATIO_AMORTISSEMENT = 1/365