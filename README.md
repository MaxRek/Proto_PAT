English below

___

# Proto_PAT
Master Informatique Parcours ORO (Optimisation en Recherche Opérationelle)
Stage de recherche 2024 par Maxime REKAR

Le logiciel suivant est un protype d'outil d'aide à la décision pour assister la mise en place de circuits courts de proximité. 
Le problème traité est un problème de Location Routing avec des problématiques de Multi-Product et de Multi-Layer, la résolution utilisée est un GVNS (VNS avec VND en recherche locale).

Les fichiers "Documentation Utilisation.pdf" et "Documentation Instance.pdf" vous indique comment utiliser le logiciel.
Une instance "didactic" est disponible pour démonstration.

___

# Proto_PAT
MSc of Computer Science, Track Optimisation in Operations Research
Research Internship 2024 by Maxime REKAR

The following software is a prototype to assist decision in context of Short Food Supply Chain.

Here's a quick introduction, see beamer and report for more information (translation in progress) :

Legislation "Egalim" in 2018 want to help sustainable and quality food consumption. One aspect of this is through social caterings, schools mainly, asking them to work on severals points. The one we would retain is the [article 24]([https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000037547983]) about the meal composition. Since 2022, 50% of food should be from sustainable sources, 20% of it should be of  "Bioligique" label, creating demand for those products. Schools caterings mainly rely on wholesaler to get their supply, but this law also want to promote food sovereignty and local food suppliers.

We limit our study to local farmers and schools caterings. This is a great opportunity for local farmers to get more buyers, and school gaterings' administrators does want to buy from them, in the limits of being able to give the adequate products. But there's two main emerging problems :

- The first one is organisation-based. Wholesalers have the advantage to simplify supply for administrators, they simply give their order and there's no more work to do until delivery. With local farmers, they would have to take contact, calculate avalaible stock and take actions if providers aren't able to satisfy their orders. For farmers, they would have to stay in contact, prepare/deliver orders, and assure all transactions. This work require time that both actors don't really have, the farmer's side being already overworked.
  
- To second one is the logistics side of orders. Related to the first problem, the logistic is organised by the farmer, from organisation to deliveries. It is source of problem since again it's time-consumming, but it could also be source of non optimal routing, since logisitical problematics aren't their speciality. French studies revealed in severals regions that local farmers often underestimate the time taken for deliveries but also the transport costs. Also, there's might no be any type of "collective distribution" since farmers often don't organise logistics between themselves. Again time is one reason but also distrust between local farmers.

The first problem has already some solutions with severals tools/websites who simplify contact between caterings and farmers. The second ones is more difficult since it requires skills, commun tools and more forward organisation, something that is really hard to organise in a "two parties" system. For this, since 2014, a new type of organisation has been created, call a "Projet Alimentaire Territoriale" (PAT). Their objective is to assist local farmers in those problems, by being a "third party" actor who does severals work to ease the farmers who could be part of these, but it's often local collectivities, citizens and others organisations who want to assist that made them. Their actions are diverse, there's has been more than 400 PAT (453 in 20/12/2024 on public data), and solutions are always specific to the region and their actors, so a solution for one PAT might not work for another one.

With these informations, we could focus on our context. We are working with the "Projet Alimentaire Territoriale Presqu'île Brière Estuaires" who concern the north-west of the "Pays de la Loire" region in France. In this territory, local collectivites and farmers try to find what would be consider the best location to stock collected food products from farmers before distributing them to the school caterings, since there's already cases of local farmers working for school caterings. The intent of this location is to reduce transport costs, reduce time for farmers but also to increase the scope of the project by proving efficiency to others farmers.

Building a specific tool to study the locations is important, since opening costs may not be a real component since local collectivities could give access to warehouses for discounted prices/free. That's why we considered implanting Routing in the Facility Location problem, hence giving the Location Routing Problem. Two other properties that appears was the Multi-Product and Multi-Layers is also implied since we got collect and delivery routes, but also an additional layer where one type of products needed to get through another actor to get processed and usable for school caterings.

The result is a usable prototype, which could be improved upon, in solving capacities but also UI to make it more accessible for a wider range of users.
