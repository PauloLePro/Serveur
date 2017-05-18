import socket, os

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

nomFich = "test.log"

##################################################################
# PARTIE ENVOIE DU FICHIER
##################################################################
if nomFich != "":
    try:
        fich = open(nomFich, "rb")  # test si le fichier existe
        fich.close()
    except:
        exit()

    octets = os.path.getsize(nomFich) / 1024

    socket.bind(("",2000))
    socket.listen(1)
    conn, adresse = socket.accept()

    conn.send("NAME " + nomFich + "OCTETS " + str(octets))  # Envoi du nom et de la taille du fichier

    # Boucle temps que l'ont est connecte
    ############################################
    while (conn.connect):
            num = 0
            pourcent = 0
            octets = octets * 1024  # Reconverti en octets
            fich = open(nomFich, "rb")

            if octets > 1024:
                for i in range(octets / 1024): # tu vas perdre des données a cause de la virgule poto
                    fich.seek(num, 0)
                    donnees = fich.read(1024)
                    conn.send(donnees)
                    num = num + 1024
            else:
                donnees = fich.read()
                conn.send(donnees)
            fich.close()
            conn.send(-1)
            conn.close()

