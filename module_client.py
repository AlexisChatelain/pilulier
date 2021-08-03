#!/usr/bin/env python
#client
import time
import socket
#importer le module socket pour le bon fonctionnement du programme
import os
#importer le module socket pour le bon fonctionnement du programme
#---------------------------------------------------

#Variables a modifier au cas ou

TCP_IP = '192.168.229.197' #197
# Adresse IP du SERVEUR

dossier_ordonnance="Ordonnances txt"
#Dossier sur Windows ou se trouvent les fichiers txt qui viennent d'etre crees par excel

dossier_ordonnance_erreurs="Erreurs"
#Dossier sur Windows ou les ordonnances sont transferees pour donner l'information a excel que le pharmacien a repondu non a la demande de savoir si l'ordonnace est bien celle du patient

dossier_ordonnance_transferees="Transferees"
#Dossier sur Windows ou les ordonnances sont transferees pour donner l'information a excel de continuer son programme

#---------------------------------------------------
rep=""
#declaration variable rep pour le reponse
print("Veuillez patienter durant l'initialisation de la connexion ...")
liste=os.listdir(dossier_ordonnance)
#faire la liste des fichiers dans le dossier dans lequel excel vient de creer l'ordonnance (il ne peut y avoir qu'un fichier car python est laisse de suite
if liste[0]==dossier_ordonnance_erreurs:
#si le 1er membre de la liste est le dossier des erreurs...
    liste.pop(0)
    #... supprimer ce membre de la iste (le 2e prend alors le place du 1er etc)
if liste[0]==dossier_ordonnance_transferees:
    #si le 1er membre de la liste est le dossier des transferees...
    liste.pop(0)
    #... supprimer ce membre de la iste (le 2e prend alors le place du 1er etc)
mon_fichier = open(os.path.join(dossier_ordonnance, liste[0]), "r")
#ouvrir le fichier cree par excel (on est alors sur que c'est le seul fichier dans le dossier)
contenu = mon_fichier.read()
#mettre l'integralite du fichier dans la variable contenu
mon_fichier.close()
#fermer le fichier texte
TCP_PORT = 5005
#port TCP pour la communication
BUFFER_SIZE = 1024
#Taille en octets des informations transmises
MESSAGE =contenu.encode()
# le MESSAGE est le contenu du fichier texte converti en bytes avec codage utf-8
boucle=0
# declaration variable boucle
erreur=0
# declaration variable erreur
for boucle in range(3):
#boucle pour communiquer 3 fois entre le pc et le Raspberry
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
    #essayer (pour voir s'il y a une erreur)
        s.connect((TCP_IP, TCP_PORT))
        #initialisation de la connexion
    except TimeoutError:
    #s'il y a une erreur
        print("Assurez-vous que le module serveur fonctionne !")
        #message d'erreur
        liste2=os.listdir(os.path.join(dossier_ordonnance))
        # faire la liste des fichiers dans le dossier des ordonnances
        for num in range(len(liste2)):
        #pour chaque fichier dans la liste...
            if liste2[num]==liste[0]:
            #... si ce fichier est le fichier du patient
                os.rename(os.path.join(dossier_ordonnance, liste[0]), os.path.join(dossier_ordonnance+"/"+dossier_ordonnance_erreurs, liste[0] +"1"))
                #et on le deplacer du dossier des ordonnances crees par excel dans le dossier des erreurs pour qu'excel ait l'info qu'il y a une erreur
        exit()
        #arreter le fichier
    s.send(MESSAGE)
    #envoyer la donnee
    data = s.recv(BUFFER_SIZE)
    #recevoir l'accuse de reception (echo)
    s.close()
    #fermer la liaison
    if erreur==1:
    #si le pharmacien a repondu non au 2e tour...
        print("Recommencez l'operation. Voir plus d'informations sur le Raspberry")
        # afficher le message pour information au pharmacien
        liste2=os.listdir(os.path.join(dossier_ordonnance+"/"+dossier_ordonnance_erreurs))
        # faire la liste des fichiers dans le dossier des erreurs
        for num in range(len(liste2)):
        #pour chaque fichier dans la liste...
            if liste2[num]==liste[0]:
            #... si ce fichier est le fichier du patient
                os.remove(os.path.join(dossier_ordonnance+"/"+dossier_ordonnance_erreurs, liste[0]))
                #on le supprime
        os.rename(os.path.join(dossier_ordonnance, liste[0]), os.path.join(dossier_ordonnance+"/"+dossier_ordonnance_erreurs, liste[0]))
        #et on le deplacer du dossier des ordonnances crees par excel dans le dossier des erreurs pour qu'excel ait l'info qu'il y a une erreur
        exit()
        #arreter le fichier
    if boucle==0:
    #au 1er tour
        if data == MESSAGE:
        #verification que l'accuse de reception soit bien le meme que la donnee
            print("Donnee envoyee puis retournee : Succes")
            # afficher le message pour information au pharmacien
    elif boucle==1:
    #au 2e tour
        while rep !="o" and rep !="O" and rep !="n" and rep !="N":
        #boucle pour refuser toutes les reponses non autorisees
            rep=input(data.decode())
            #demander au pharmacien une reponse en demandant si l'ordonnance est bien celle affichee
            if rep =="n" or rep =="N":
            #si la reponse est non
                erreur=1
                #mettre la variable pour que ce soit pris en compte au prochain tour
            MESSAGE=rep.encode()
            #coder le message pour le transfert
    elif boucle==2:
    #au 3e tour
        liste2=os.listdir(os.path.join(dossier_ordonnance+"/"+dossier_ordonnance_transferees))
        # faire la liste des fichiers dans le dossier des ordonnances transferees
        for num in range(len(liste2)):
        #pour chaque fichier dans la liste...
            if liste2[num]==liste[0]:
            #... si ce fichier est le fichier du patient
                os.remove(os.path.join(dossier_ordonnance+"/"+dossier_ordonnance_transferees, liste[0]))
                #on le supprime
        os.rename(os.path.join(dossier_ordonnance, liste[0]), os.path.join(dossier_ordonnance+"/"+dossier_ordonnance_transferees, liste[0]))
        #et on le deplacer du dossier des ordonnances crees par excel dans le dossier des ordonnances pour qu'excel ait l'info qu'il n'y a pas eu d'erreur et qu'il peut terminer son programme