#Ceci est le module serveur 
#prg_Thomas est un bout de programme réalisé par un de mes camarades pour le contrôle des moteurs connectés au Raspberry.

import socket
#importer le module socket pour le bon fonctionnement du programme
import os
#importer le module socket pour le bon fonctionnement du programme
import re
#importer le module pour enlever les retours à la ligne
from adafruit_motorkit import MotorKit
#module pour le contôle des moteurs
import time
#module de gestion du temps
#-------------------------------------------------------

# Variables modifiables au cas où

TCP_IP = '192.168.229.197' #13
# Adresse IP du serveur à la salle du lycée

Dossier_ordonnances ="Ordonnances"
#Dossier sur le Raspberry où sont créés les fichiers txt contenants les données

Dossier_ordonnances_ok= "Ordonnances traitees"
#Dossier sur le Raspberry où sont déplacés créés les fichiers txt ordonnances après remplissage du pillulier

separateur=";"
#Séparateur utilisé par excel pour la créarion du fichier txt

extension_txt =".txt"
#extension du fichier texte

codage='utf-8'
#codage pour la transmission

#-------------------------------------------------------


def prg_Thomas():

    kit=MotorKit()
    pas = 0.6283185305
    micro_pas = 0.6283185305 / 4
    n=100 #int(input())#valeur de distance 100mm
    m=10.5 #int(input())#valeur de distance 10.5mm
    o=21 #int(input())#valeur de distance 21mm
    deplacement=0
    print("type médicament",type_médicament)
    print("x :" ,x)
    for i in range(int(n/pas)): #mesure d'écart ici ou chercher à mieux     programmer
        kit.stepper1.onestep() #angle équivalent à une distance parcourue de 100mm
    time.sleep(0.01)
    print (deplacement + 100)
    deplacement = deplacement + 100
    time.sleep(3)
    position = 0
    print(position+1)
    #while str(date_rasp)!=str(grille[ligne+1][9]):
    #!!!!!!!!!!!! ATTENTINON NE FONCTIONNE PAS : TEST DE LA DATE
    for i in range(int(m/pas)): #mesure d'écart ici ou chercher à mieux programmer
        print(str(date_rasp))
        print(str(grille[ligne+1][9]))
        print("date différente")
        kit.stepper1.onestep() #angle équivalent à une distance parcourue de 10.5mm
        time.sleep(0.01)
    time.sleep(3)
    print(deplacement + 10.5)
    deplacement = deplacement + 10.5
    for position in range (1,7):
        print(position +1)
        if x == 0 :
            for i in range(int(o/pas)): #mesure d'écart ici ou mieux programmer
                kit.stepper1.onestep() #angle <=> à une distance parcourue de 21mm

                time.sleep(0.01)
            time.sleep(3)
        else :  
            time.sleep(x/5) # x*3 normalement
        print(deplacement+21)
        deplacement =deplacement+21  

    kit.stepper1.release()
    #TRES IMPORTANT
date_rasp = ""
ok=0
suite=0
rep=""
while ok  != 1:
    if ok == 0:
        date_rasp = ""
        date_rasp = input("Veuillez indiquer la date d'aujourd'hui (au format jj/mm/aaaa)")
    try:
        if len(date_rasp) ==  10 and date_rasp[2:3] == "/" and date_rasp[5:6] == "/" and int(date_rasp[:2])>=0 and int(date_rasp[:2])<=32 and int(date_rasp[3:5])>=0 and int(date_rasp[3:5])<=13 and int(date_rasp[-4:])>=2018 and int(date_rasp[-4:])<=2050:
            suite = 1
    except:
        ok=0
    if suite == 1:
        while rep != "o" and rep != "n" and rep != "O" and rep != "N":
            rep=input("La date renseignée est-elle "+ str(date_rasp)+" ? (o/n)")
        if rep == "o" or  rep == "O":
            ok = 1
        else:
            rep=""
            suite = 0
print("Date enregistrée")
print("La connexion est en cours de fonctionnement")
TCP_PORT = 5005
#port TCP pour la communication
BUFFER_SIZE = 1024
#Taille en octets des informations transmises
boucle=0
#initialisation de la variable boucle pour la boucle
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
#initialisation de la connexion
while 1:
#boucle infinie pour attendre la donnée
    for boucle in range(3):
    #2e boucle pour communiquer 3 fois entre le pc et le Raspberry
        s.listen(1)
        conn, addr = s.accept()
        while 1:
            data = conn.recv(BUFFER_SIZE)
            #réception de la donnée
            if not data: break
            #s'il n'y a pas de donnée, on sort de la boucle infinie
            if boucle==0:
            #au 1er tour...
                msg=data.decode()
                #... on passe la donnée de byte en string (chaîne de caractères)
                fin_nom=msg.find(separateur)
                #on cherche le 1er séparateur dans la donnée...
                mon_fichier= open(os.path.join(Dossier_ordonnances,msg[:fin_nom]+extension_txt),"w")
                #... pour pouvoir trouver le nom et prénom du patient et ouvrir (ou créer) un fichier à ce nom
                mon_fichier.write(msg)
                #on écrit l'intégralité de la donnée (de l'ordonnance) dans le fichier qui qui s'être ouvert
                mon_fichier.close()
                #on ferme le fichier (ça l'enregistre en même temps)
                conn.send(data)  # echo
                #renvoyer la donnée au client comme accusé de réception (echo)
            elif boucle == 1:
            #au 2e tour...
                liste=os.listdir(Dossier_ordonnances)
                #on regarde la liste des fichiers dans le dossier où est crée le fichier
                conn.send(bytes("\n\n\n-------------------------------------------------------------\nLe patient est-il "+ str(liste[0][:len(liste[0])-4])+" ?\nRépondre par o ou n puis appuyez sur Entrée.\n-------------------------------------------------------------\nVotre réponse : ",codage))
                #on demande confirmation au pharmacien que c'est le bon fichier
            elif boucle == 2:
            #au 3e tour
                rep=data.decode()
                #on passe la réponse de byte en string (chaîne de caractères)
                conn.send(data)
                #accusé de réception de la réponse (echo)
        conn.close()
        #fermer la connexion à chaque fois que donnée est reçue
        print("Donnée reçue puis retournée : Succès.")
        # afficher le message pour information au pharmacien

    if rep =="n" or rep=="N":
    # si le pharmacien répond non
        print("Recommencez l'opération. Il doit n'y avoir aucun fichier dans le dossier",Dossier_ordonnances,"!")
        # afficher le message pour information au pharmacien
    else:
    # sinon la réponse est forcément positive car le contrôle de la réponse a été fait sur le module client
        fich = open(os.path.join(Dossier_ordonnances, liste[0]), "r")
        # ouvrir l'ordonnance du patient
        contenu = fich.read()
        # lire tout le fichier et le placer dans une variable
        sep=contenu.count(separateur)
        #compter le nombre de séparateurs
        new_contenu = re.compile(r'[\n]')
        #repérer les retours à la ligne
        contenu = new_contenu .sub("", contenu)
        #et les remplacer par rien
        nblignes = len(open(os.path.join(Dossier_ordonnances, liste[0])).readlines())
        #compter le nombre de ligne de le fichier
        grille=[[""for j in range(10)]for i in range(nblignes)]
        #créer une grille de 10 en largeur par le nombre de ligne du fichier texte
        for i in range(nblignes):
        #pour chaque ligne
            for j in range(10):
            #pour chaque colonne
                sep=contenu.find(separateur)
                #chercher le 1er séparateur
                grille[i][j]=contenu[:sep]
                #remplir la grille avec la partie de gauche du contenu jusqu'au 1er séparateur
                contenu=contenu[sep+1:]
                #supprimer du contenu la partie mise dans la grille
                print ("[",i,"][",j,"] ",grille[i][j])
                #afficher le contenu du fichier à partir de la grille
        fich.close()
        # table des données (pour Thomas)
        '''
grille[0][0] # NOM Prénom
grille[0][1] # (Sexe(H ou F),Date de naissance)
grille[0][2] # Vide
grille[0][3] # Vide
grille[0][4] # Vide
grille[0][5] # Vide
grille[0][6] # Vide
grille[0][7] # Vide
grille[0][8] # Vide
grille[0][9] # Vide
grille[1][0] # code du médicament
grille[1][1] # Nombre de comprimés au petit déjeuner ligne 1 (ligne 2 du fichier texte)
grille[1][2] # Nombre de comprimés au déjeuner ligne 1 (ligne 2 du fichier texte)
grille[1][3] # Nombre de comprimés au dîner ligne 1 (ligne 2 du fichier texte)
grille[1][4] # Nombre de comprimés au coucher ligne 1 (ligne 2 du fichier texte)
grille[1][5] # Type de fréquence ligne 1 (ligne 2 du fichier texte)
grille[1][6] # Variable de la fréquence ligne 1 (ligne 2 du fichier texte)
grille[1][7] # Date du début du traitement ligne 1 (ligne 2 du fichier texte)
grille[1][8] # Date de fin du traitement ligne 1 (ligne 2 du fichier texte)
grille[n][0] # code du médicament ligne n (ligne n+1 du fichier texte)
grille[n][1] # Nombre de comprimés au petit déjeuner ligne n (ligne n+1 du fichier texte)
grille[n][2] # Nombre de comprimés au déjeuner ligne n (ligne n+1 du fichier texte)
grille[n][3] # Nombre de comprimés au dîner ligne n (ligne n+1 du fichier texte)
grille[n][4] # Nombre de comprimés au coucher ligne n (ligne n+1 du fichier texte)
grille[n][5] # Type de fréquence ligne n (ligne n+1 du fichier texte)
grille[n][6] # Variable de la fréquence ligne n (ligne n+1 du fichier texte)
grille[n][7] # Date du début du traitement ligne n (ligne n+1 du fichier texte)
grille[n][8] # Date de fin du traitement ligne n (ligne n+1 du fichier texte)
grille[n][9] # Indication: jour de prise ligne n (ligne n+1 du fichier texte)
        '''

        print("prg moteurs")
        type_médicament=1
        tout_fait = 1
        while tout_fait != nblignes :
            for ligne in range(nblignes-1) :
                if int(grille[ligne+1][0])==type_médicament:
                    x=int(grille[ligne+1][1])+int(grille[ligne+1][2])+int(grille[ligne+1][3])+int(grille[ligne+1][4])
                    prg_Thomas()
                    #lancer la fonction de Thomas (déplacement moteur selon x)
                    tout_fait=tout_fait + 1
            type_médicament=type_médicament+1
        #pour chaque ligne du fichier texte
        print("Session terminée")      

        os.rename(os.path.join(Dossier_ordonnances, liste[0]), os.path.join(Dossier_ordonnances_ok, liste[0]))

        #Après distribution des médicaments, déplacer l'ordonnance du patient dans le dossier des ordonnances traitées
