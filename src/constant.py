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

#Dataframe
FIELDS_F = ["Nom","x","y","Commune"]
FIELDS_E = ["Nom de la structure","x","y","Nombre de repas par jour","Commune","Domaine","Type de restauration"]
SUB_FIELDS_E = ["Nom de la structure","x","y","Nombre de repas par jour","Commune"]
FIELDS_N = ["Nom de la structure","x","y","Commune"]
FIELDS_T = ["Nom de la structure","x","y","Commune"]
FIELDS_D = ["E","P","F","d"]

#Affichage
COLOR_PIN_F = "red"
COLOR_PIN_E = "blue"
COLOR_PIN_N = "black"
COLOR_PIN_T = "green"

#Generation
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