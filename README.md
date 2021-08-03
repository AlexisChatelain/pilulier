## Pilulier (Projet SI BAC)
> Création d'un prototype de préparateur automatique de piluliers

## Informations
Nous étions 5 sur ce projet pluridisciplinaire des Sciences de l'Ingénieur présenté au BAC. <br>
Nous avons créé un prototype de préparateur automatique de piluliers. <br>
Chacun a travaillé sur sa partie (réservoirs, déplacement du plateau, etc).<br>
Je me suis occupé de créer un fichier Excel qui sert d'ordonnance remplie par le médecin ou le pharmacien. 
Une fois l'ordonnance correctement remplie, j'ai fait deux programmes python pour établir une connexion TCP/IP entre le PC et le Raspberry (petit ordinateur embarqué sur le prototype). <br>
Un programme (module client) fonctionne sur Windows pour envoyer l'ordonnance, le second (module serveur) sur la Raspberry pour recevoir l'ordonnance et l'exploiter.<br> 
Nous avons passé chacun un peu moins d'une centaine d'heures sur ce projet. <br>

## Fichiers disponibles :
* Commentaire.pdf : Ce que j'ai évoqué lors de la soutenance du projet.
* Presentation.pdf : Présentation globale du projet
* Ordonnance_type et transfert txt ok 28052019.xls : fichier excel avec macros pour la gestion des ordonnances et l'envoi de celle-ci vers le serveur
* Organigramme 2.0 Alexis.xls : L'organigramme sur excel de ma partie du projet
* module_client.py : script python lancé automatiquement par Excel 
* module_server.py : le code que nous exécutions sur raspberry qui doit fonctionner en permanence
* Vous devez bien-sûr adapter ces 3 derniers fichiers si vous souhaitez utiliser mon code, ils n'étaient fonctionnels que dans la situation exacte de notre projet.
