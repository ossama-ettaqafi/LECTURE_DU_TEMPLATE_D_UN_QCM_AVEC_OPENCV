'''

                ------------------------- Concept du programme  -------------------------

                Le concept du programme consiste à extraire les réponses fournies
                par un étudiant dans un QCM précis. Veuillez noter que ce projet
                est uniquement conçu pour traiter ce QCM en particulier, donc toutes
                les tailles et positions dépendent de ce dernier.

                La lecture de l'image peut prendre du temps en utilisant uniquement
                pytesseract. Il est nécessaire d'installer cet outil sur votre ordinateur
                et de préciser le chemin "D:\Program Files\Tesseract-OCR\tesseract.exe".

                Ce programme a été développé par OSSAMA ETTAQAFI en 2023.
                Pour toute question ou demande de renseignements, veuillez contacter
                ossamaett2002@gmail.com.
                
                -------------------------------------------------------------------------
                
'''

# Importation des modules nécessaires
import cv2 # pour lire les images
import time # pour mesurer le temps d'exécution
import os # pour gérer les fichiers et les répertoires
import os.path # pour travailler avec les chemins d'accès aux fichiers
import pytesseract # pour effectuer la reconnaissance optique de caractères (OCR)
import numpy as np # pour manipuler les tableaux multidimensionnels
import shutil # pour copier et déplacer des fichiers
import fitz # pour travailler avec les fichiers PDF
import PyPDF2 # pour manipuler les fichiers PDF
from tkinter import filedialog # pour afficher une boîte de dialogue de sélection de fichiers
from imutils import contours # pour traiter les contours des images

# Configuration de pytesseract
pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files\Tesseract-OCR\tesseract.exe"

# Déclaration des tableaux et des variables
dossiers = ['nom_prenom', 'cours_sec', 'date_eva'] # tableau de noms de dossiers
qcm_path = ['.temp/page1.jpg', '.temp/page2.jpg'] # tableau de chemins d'accès aux images QCM
PDF_PATH = '' # chemin d'accès au fichier PDF (à définir ultérieurement)

# Fonction 1 : importer un fichier pdf
def importerpdf():
    global PDF_PATH # utiliser la variable globale PDF_PATH

    # Afficher une boîte de dialogue pour sélectionner un fichier
    PDF_PATH = filedialog.askopenfilename()

    # Vérifier si le fichier sélectionné est un fichier PDF
    if not PDF_PATH.endswith(".pdf"):
        print("S'il vous plaît importer un fichier PDF!")
        return importerpdf()

    # Si le PDF contient plusieurs étudiants, diviser le fichier PDF en plusieurs fichiers PDF
    if sepearer_pdf(PDF_PATH) is not None:
        print("On a divisé le fichier PDF choisi car il contient plusieurs étudiants! Choisissez un PDF parmi les...")
        return importerpdf()

    # Afficher le chemin d'accès au fichier PDF sélectionné
    print(f"\nChemin du fichier : {PDF_PATH}")

# Fonction 2 : transformer le pdf en image
def transformer_en_img(chemin, fich_pdf):
    doc = fitz.open(fich_pdf) # Ouvrir le fichier PDF avec la bibliothèque PyMuPDF
    zoom = 4
    mat = fitz.Matrix(zoom, zoom) # Créer une matrice pour la conversion PDF vers image
    count = 0 # Initialiser un compteur pour le nombre de pages dans le PDF

    for p in doc:
        count += 1  # Compter le nombre de pages dans le PDF

    # Vérifier si le dossier ".temp" existe déjà, sinon le créer
    if(os.path.exists('.temp')==False):
        os.mkdir('.temp')   
        
    for i in range(count):
        val = f"{chemin}/page{i+1}.jpg"  # Créer un chemin de fichier unique pour chaque page
        page = doc.load_page(i)  # Charger la page à partir du PDF
        pix = page.get_pixmap(matrix=mat)  # Convertir la page en image
        pix.save(val)  # Enregistrer l'image dans le dossier ".temp"

    doc.close()  # Fermer le fichier PDF

# Fonction 3 : tester si l'image est inversée
#   - Retourner True : si l'image est inversée
#   - Retourner False : si l'image n'est pas inversée
def est_inversee(img_path):
    # Déclarer un tableau
    tableau = np.full(24, '')
    
    # Lire l'image
    image = cv2.imread(img_path)
    image = cv2.resize(image, (2481, 3508))

    # Changer les couleurs de l'image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
    cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts, _ = contours.sort_contours(cnts, "left-to-right")

    for cnt in cnts:
        x1, y1 = cnt[0][0]
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx):
            x, y, w, h = cv2.boundingRect(cnt)

            if (h >= 150 and h <= 160) and (w >= 635 and w <= 645):
                # Sélectionner la case
                image = image[y:y + h, x:x + w]

                x, y, h, w = (105, 55, 38, 376)

                selected = image[y:y + h, x:x + w]
                selected = cv2.resize(selected, (w * 5, h * 5))

                # Rendre l'image plus lisible
                selected = haute_qualite(selected)

                data = pytesseract.image_to_string(selected)
                data = data.replace('\n', ' ').replace('\r', '').replace(' ', '')
                tableau = data

                break

    if tableau == 'unecasemaximumparligne':
        return False
    else:
        return True

# Fonction 4 : Inverser l'image si elle est à l'envers
# - Prend en entrée le chemin de l'image à inverser
# - Utilise la fonction est_inversee pour tester si l'image est inversée
# - Si l'image est inversée, utilise la fonction cv2.flip pour l'inverser
# - Retourne l'image inversée ou non modifiée
def inverser_image(chemin_image):
    img = cv2.imread(chemin_image)
    if est_inversee(chemin_image):
        img = cv2.flip(img, -1)
    return img

# Fonction 5 : permet de supprimer le dossier '.temp'
def supprimer_tempfile():
    shutil.rmtree('.temp', ignore_errors=True)

# Fonction 6 : permet d'ameliorer la qualite d'une image
def haute_qualite(image):
    # Convertir l'image en grayscale et appliquer un flou gaussien
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # Appliquer un seuillage binaire inversé
    binary = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Appliquer la dilatation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel)

    return dilated

# Fonction 7 : calculer le nombre des fichiers et des dossiers qui se trouvent dans un dossier
def count_fd(path_dossier):
    # Lister les fichiers qui se trouvent dans un dossier du path 'path_dossier'
    lst = os.listdir(path_dossier)

    # Calculer la taille de la liste
    count_fds = len(lst)
    
    return count_fds

# Fonction 8 : permet de transformer un tableau en chaîne de caractères
def tab2str(tableau):
    string = ''
    for i in range(len(tableau)):
        if tableau[i] == '': string = string + ' '
        else: string = string + tableau[i]

    return string.rstrip()

# Fonction 9 : Fonction 9 : permet de calculer le nombre des questions dans un QCM du chemin donné
def calculer_qsts(chemin_image):
    # Lire l'image, changer la taille et les couleurs
    image = inverser_image(chemin_image)
    image = cv2.resize(image, (2481, 3508))

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]

    # Trouver les contours, les trier de gauche à droite
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts, _ = contours.sort_contours(cnts, "left-to-right")

    num = 0

    # Sélectionner seulement les contours des questions
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 10:
            x, y, w, h = cv2.boundingRect(c)

            if (h >= 150 and h <= 160) and (w >= 635 and w <= 645):
                num = num + 1
                 
    return num

# Fonction 10 : permet d'extraire toutes les images des questions depuis le chemin du QCM donné.
def images_qsts(chemin_image):
    # Lire l'image, Changer la taille et les couleurs
    image = inverser_image(chemin_image)
    image = cv2.resize(image, (2481, 3508))
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]

    # Trouver les contours et les trier depuis le gauche au droit
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts, _ = contours.sort_contours(cnts, "left-to-right")

    # Sélectionner seulement les contours des questions
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 10:
            x, y, w, h = cv2.boundingRect(c)

            if (h >= 150 and h <= 160) and (w >= 635 and w <= 645):
                # Sélectionner la question
                selected = image[y:y+h, x:x+w]
                selected = cv2.resize(selected, (w*6,h*6))
                            
                # Sélectionner le nombre de la question
                (qx, qy) = (0, 360)
                ques_num = selected[qy:qy+270, qx:qx+398]
                
                # Rendre l'image plus lisible
                ques_num = haute_qualite(ques_num)
       
                number = pytesseract.image_to_string(ques_num, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
                number = number.replace('\n', ' ').replace('\r', '').replace(' ', '')
        
                # Sauvegarder les images dans le dossier 'questions'
                # questions/numero_question.jpg              
                cv2.imwrite('.temp/questions/{}.jpg'.format(number), selected)
            
# Fonction 11 : permet d'extraire les images des réponses depuis l'image d'une question à path donné
#   - qst_path : le chemin de l'image
#   - nbr_quest : le nombre de la question
def images_rpns(image_qst, nbr_quest):
    # Lire l'image
    img = cv2.imread(image_qst)
    img = cv2.resize(img, (900, 240))

    # Changer les couleurs de l'image
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    seuil = cv2.threshold(gris, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
    contours, hierarchy = cv2.findContours(seuil, 1, 2)

    for cnt in contours:
        x1, y1 = cnt[0][0]
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if len(approx):
            x, y, w, h = cv2.boundingRect(cnt)

            if (h==35 or h==36) and (w==52 or w==53 or w==54):
                # Sélectionner seulement le chiffre qui existe dans l'image du choix d'une question
                x, y, h, w = (x + 15, y + 1, h - 2, w - 28)
                selected = img[y:y+h, x:x+w]
                selected = cv2.resize(selected, (w*5, h*5))

                # Améliorer la qualité de l'image
                kernel = np.ones((5, 5), np.uint8)
                selected = cv2.erode(selected, kernel, iterations=1)
                #selected = haute_qualite(selected)

                if 150 <= y and y <= 180:
                    ch = '2'
                else:
                    ch = '1'

                # Tester si les dossiers existent déjà, sinon il va les créer
                if os.path.exists('.temp/reponses/'+str(nbr_quest)+'/{}/'.format(ch)) == False:
                    num = 1
                    os.mkdir('.temp/reponses/'+str(nbr_quest)+'/{}/'.format(ch))

                # Enregistrer chaque réponse dans des dossiers spécifiés
                # num_question/ligne/num_reponse.jpg       
                path = '.temp/reponses/'+str(nbr_quest)+'/{}/'.format(ch)+str(num)+'.jpg'
                cv2.imwrite(path, selected)

                num += 1

# Fonction 12 : permet d'extraire les images des réponses depuis un nombre précis de questions
#   - nbr_qsts : le nombre de questions dans un QCM
def extraire_rpns_qsts(nbr_qsts):
    for q in range(nbr_qsts):
        # Créer le dossier de la question si nécessaire
        os.makedirs('.temp/reponses/{}'.format(q+1), exist_ok=True)

        # Extraire les réponses depuis l'image d'une question
        images_rpns('.temp/questions/{}.jpg'.format(q+1), q+1)

# Fonction 13 : compléter les cases du tableau par ''
def completer_tab(tab):
    ntab = np.full(7, '')
    for i in range(7):
        if i < len(tab):
            ntab[i] = tab[i]
        else:
            ntab[i] = ''
    return ntab

# Fonction 14 : trouver la réponse de l'utilisateur
#   - Le contenu de l'image qui n'a pas été reconnu/reste vide est la réponse de l'utilisateur.
#   - Le choix qui a été reconnu et qui n'a pas été touché par l'utilisateur n'est pas la réponse.      
def trouver_reponse(rep1, rep2):
    tab = ["T","A","5","4","3","2","1"]
    rep = np.full((2,7), '')

    if len(rep1) < 7: rep1 = completer_tab(rep1)
    if len(rep2) < 7: rep2 = completer_tab(rep2)

    rep[0] = rep1
    rep[1] = rep2

    fois = 0
    reponse = 0

    j = 1
    while j >= 0:
        i = 0
        while i < 7:
            if fois > 1:
                return -1
            
            if tab[i] not in rep[j] : 
                reponse = tab[i]
                return reponse
                fois += 1
            
            i += 1

            if i == 7 and fois == 1:
                return reponse
        j -= 1
        
    if fois == 0:
        return reponse

# Fonction 15 : permet d'afficher les réponses d'étudiant depuis les images des réponses sauvegardées
def afficher_reponses(nbr_ques):
    resultats = []
    for q in range(nbr_ques):
        for d in range(2):
            dossier = '.temp/reponses/'+str(q+1)+'/{}/'.format(d+1)
            nf = count_fd(dossier)
            
            # Déclaration d'un tableau de (nf) cases
            if d == 0: r1 = np.full(nf, '')
            elif d == 1: r2 = np.full(nf, '')

            for i in range(nf):       
                # Lire l'image
                img = cv2.imread(dossier+'/{}.jpg'.format(i+1))
                
                # Extraire le texte depuis l'image, seulement les caractères 12345AT
                data = pytesseract.image_to_string(img, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=12345AT')
                data = data.replace('\n', '').replace('\r', '').replace(' ', '')
                 
                if d == 0: r1[i] = data
                elif d == 1: r2[i] = data
            
        # Tester la réponse qui se trouve dans le tableau puis l'afficher
        reponse = trouver_reponse(r1, r2)
        if reponse == 0:
            resultats.append([q+1, 'Aucune réponse'])
        elif reponse == -1:
            resultats.append([q+1, 'Réponse non acceptée'])
        else:
            resultats.append([q+1, reponse])

    # Afficher le tableau des résultats
    print('+----------------------+------------------------+')
    print('| Question             | Réponse                |')
    print('+----------------------+------------------------+')
    for row in resultats:
        print(f'| {str(row[0]).ljust(20)} | {str(row[1]).ljust(22)} |')
    print('+----------------------+------------------------+')
     
    # Supprimer les dossiers 'reponses'
    shutil.rmtree('.temp/reponses', ignore_errors=True)

# # Fonction 16 : permet d'extraire les informations d'étudiant et de l'évaluation (nom, prénom, matricule, date d'évaluation)
def images_infos(chemin_image):
    # Lire l'image
    image = inverser_image(chemin_image)
    image = cv2.resize(image, (2481, 3508))

    # Changer les couleurs de l'image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
    cnts,hierarchy = cv2.findContours(thresh, 1, 2)
    cnts, _ = contours.sort_contours(cnts, "left-to-right")

    # Créer les dossiers nécessaires s'ils n'existent pas déjà
    for dossier in dossiers:
        if not os.path.exists(f'.temp/informations/{dossier}'):
            os.makedirs(f'.temp/informations/{dossier}')

    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)

        if (h >= 500 and h <= 550) and (w >= 800 and w <= 850):
            # Extraire l'image du matricule
            selected = image[y:y+h, x:x+w]
            os.makedirs('.temp/informations/matricule')
            cv2.imwrite('.temp/informations/matricule/matricule.jpg', selected)

        elif (h >= 50 and h <= 60) and (w >= 30 and w <= 40):
            selected = image[y:y+h, x:x+w]
            selected = cv2.resize(selected, (w*5, h*5))
            selected = haute_qualite(selected)
            
            # Extraire l'image des caractères : nom/prénom et cours/section
            if y >= 170 and y <= 250:
                dossier = 'nom_prenom' if y <= 185 else 'cours_sec'
                num = count_fd(f'.temp/informations/{dossier}') + 1
                cv2.imwrite(f'.temp/informations/{dossier}/{num}.jpg', selected)

            # Extraire l'image des caractères : date d'évaluation
            elif y >= 300 and y <= 320:
                num = count_fd('.temp/informations/date_eva') + 1
                cv2.imwrite(f'.temp/informations/date_eva/{num}.jpg', selected)

# Fonction 17 : permet d'extraire les zones à remplir qui se trouvent dans l'image du matricule
def images_mtr(chemin_matricule):
    # Lire l'image
    img = cv2.imread(chemin_matricule)
    img = cv2.resize(img, (1200, 800))
    
    # Changer les couleurs de l'image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
    cnts,hierarchy = cv2.findContours(thresh, 1, 2)
    cnts, _ = contours.sort_contours(cnts, "top-to-bottom")

    num = 1
    for cnt in cnts:
       x1,y1 = cnt[0][0]
       approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
       if len(approx):
            x, y, w, h = cv2.boundingRect(cnt)
            
            if (h >= 30 and h <= 40) and (w >= 50 and w <= 60):
                # Pour nommer les dossiers
                if 100 <= y and y <= 120: ch = '0'
                elif 230 <= y and y <= 240: ch = '1'
                elif 350 <= y and y <= 360: ch = '2'
                elif 470 <= y and y <= 480: ch = '3'            
                elif 590 <= y and y <= 600: ch = '4'              
                elif 710 <= y and y <= 730: ch = '5'

                # Selectioner seulement le caractere encadre
                x, y, h, w = (x + 15, y + 4, h - 5, w - 28)

                selected = img[y:y+h, x:x+w]
                selected = cv2.resize(selected, (w*5, h*5))

                # Rendre l'image plus lisible
                selected = haute_qualite(selected)
                    
                # Tester si les dossiers existent déjà, sinon les créer
                if ch != '0':
                    if(os.path.exists('.temp/informations/matricule/{}/'.format(ch))==False):
                        num = 1
                        os.mkdir('.temp/informations/matricule/{}/'.format(ch))
                else:
                    num = 1
                    
                # Enregistrer les chiffres des matricules dans des dossiers
                # informations/matricule/nbr_chiffre/matr.jpg
                if ch == '0': chemin_fichier = '.temp/informations/matricule/'+str(num)+'.jpg'
                else: chemin_fichier = '.temp/informations/matricule/{}/'.format(ch)+str(num)+'.jpg'
                cv2.imwrite(chemin_fichier, selected)
                
                num += 1
        
# Fonction 18 : trouver le nombre masqué depuis le tableau
def nombre_masque(tab):
        num = 9
        c = False
        for i in range(10):
           if tab[i] == '':
                num = num - i
                c = True
                break
        if c : 
          return num
        else:
          return ''

# Fonction 19 : compléter et trier le matricule
def completer_trier(tab):
    # Compléter le tableau
    if len(tab) < 10:
        i = len(tab) - 1   
        while i < 10:
            tab[i] = ''
            i += 1

    # Trier le tableau de 9 jusqu'à 0
    base = ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0']

    for i in range(10):
        if base[i] not in tab:
            base[i] = ''

    return base

# Fonction 20 : permet d'extraire le matricule depuis la première page du QCM
def extraire_matr():
        chiffre = np.full(10, '')
        matricule = np.full(6, '')
    
        # Lire le contenu des images puis extraire le nombre masque dans l'image
        for i in range(6):
                im_num = 0

                if i == 0:
                    nf = 1
                else:
                    dossier = '.temp/informations/matricule/'+str(i)+'/'
                    nf = count_fd(dossier)
            
                for j in range(nf):
                        im_num = im_num + 1
                    
                        # Lire l'image
                        if i == 0:
                            path = '.temp/informations/matricule/1.jpg'.format(im_num)
                            if os.path.exists(path) == True:
                                img = cv2.imread(path)
                            else:
                                matricule[i] = 'P'
                                break
                        else: img = cv2.imread(dossier+'{}.jpg'.format(im_num))

                        # Extraire le texte depuis l'image, seulement les caracteres P0123456789
                        data = pytesseract.image_to_string(img, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=P0123456789')
                        data = data.replace('\n', '').replace('\r', '').replace(' ', '')
                        if i == 0:
                            if data == '':
                                matricule[0] = 'P'
                            break
                        else: chiffre[j] = data
        
                if i != 0 :
                    tab = np.full(len(chiffre),'')
                    tab = completer_trier(chiffre)                 
                    matricule[i] = nombre_masque(tab)

        return matricule

# Fonction 21 : permet d'extraire les informations depuis le QCM
def afficher_infos():
    nom_prenom = np.full(31, '')
    cours_sec = np.full(31, '')
    date_eva = np.full(10, '')
    
    matricule = np.full(6, '')
    
    for i in range(3):
        if i == 0 or i == 1:
            r = range(31)
        elif i == 2:
            r = range(10)
            
        for j in r:         
            # Lire l'image
            img = cv2.imread('.temp/informations/' + dossiers[i] + '/{}.jpg'.format(j+1))
            img = cv2.resize(img, (200, 400))

            w, h, x, y = (175, 350, 16, 16)       
            img = img[y:y+h, x:x+w]
            
            # Extraire le texte depuis l'image
            if i == 0 or i == 1:
                data = pytesseract.image_to_string(img, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                data = data.replace('\n', ' ').replace('\r', '').replace(' ', '')
                
                if i == 0: nom_prenom[j] = data
                elif i == 1: cours_sec[j] = data
            elif i == 2:
                data = pytesseract.image_to_string(img, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=/0123456789')
                data = data.replace('\n', ' ').replace('\r', '').replace(' ', '')
                date_eva[j] = data
                
    # Pour afficher
    matricule = extraire_matr()
    
    # Créer une liste des informations à afficher
    informations = [
        ['Date de l\'évaluation', tab2str(date_eva).rstrip()],
        ['Nom et prénom', tab2str(nom_prenom).rstrip()],
        ['Matricule', tab2str(matricule).rstrip()],
        ['Cours et section', tab2str(cours_sec).rstrip()]
    ]

    # Afficher le tableau des résultats
    print('+----------------------+------------------------+')
    print('| Information          | Donnée                 |')
    print('+----------------------+------------------------+')
    for row in informations:
        print(f'| {str(row[0]).ljust(20)} | {str(row[1]).ljust(22)} |')
    print('+----------------------+------------------------+')

    # Supprimer le dossier 'informations'
    shutil.rmtree('.temp/informations', ignore_errors=True)
    
# Fonction 22 : permet d'extraire les images des données depuis un QCM
    # type: 0 - les informations
    # type: 1 - les réponses
def extraire(type):
    t0 = time.time()
    
    # Créer le dossier correspondant si nécessaire
    dossier = ".temp/informations" if type == 0 else ".temp/questions"
    if not os.path.exists(dossier):
        os.mkdir(dossier)

    if type == 0:
        # Extraire les informations
        images_infos(qcm_path[0])

        # Extraire le matricule
        images_mtr('.temp/informations/matricule/matricule.jpg')

    elif type == 1:     
        nb_pages = nbr_pages(PDF_PATH)

        for i in range(nb_pages):
            # Extraire les questions
            images_qsts(qcm_path[i])

        # Extraire les réponses
        extraire_rpns_qsts(sum([calculer_qsts(qcm_path[i]) for i in range(nb_pages)]))

        # Supprimer le dossier 'questions'
        shutil.rmtree(dossier, ignore_errors=True)
        
    t1 = time.time()
    
    # Calculer et retourner le temps d'exécution en secondes
    return round(t1 - t0, 2)
  
# Fonction 23 : permet d'afficher les données d'un QCM
    # type: 0 - les informations
    # type: 1 - les réponses
def afficher(type):
    t0 = time.time()
    
    # Afficher les informations personnelles
    if type == 0:
        afficher_infos()
    # Afficher les réponses aux questions
    elif type == 1:
        # Calculer la liste des questions
        qsts = 0
        nb_pages = nbr_pages(PDF_PATH)
        
        for i in range(nb_pages):
            qsts += calculer_qsts(qcm_path[i])

        # Afficher les réponses correspondantes
        afficher_reponses(qsts)

    t1 = time.time()
    
    #Calculer et retourner le temps d'exécution en secondes
    return round(t1 - t0, 2)

# Fonction 24 : extraire les informations de tous les QCMs des étudiants qui existent dans le dossier 'Etudiants'
def extraire_etudiants():
    # Parcourir tous les fichiers dans le dossier 'Etudiants'
    for filename in os.listdir('Etudiants/'):
        # Vérifier si c'est un fichier PDF
        if not filename.endswith('.pdf'):
            continue

        # Extraire les informations depuis le fichier PDF
        global PDF_PATH  # Utiliser la variable globale PDF_PATH
        PDF_PATH = f"Etudiants/{filename}"

        # Extraire d'autres PDF si le PDF contient plusieurs étudiants
        PDF_PATH = sepearer_pdf(PDF_PATH)

    for filename in os.listdir('Etudiants/'):
        # Supprimer le dossier '.temp' et son contenu
        supprimer_tempfile()
        
        # Vérifier si c'est un fichier PDF
        if not filename.endswith('.pdf'):
            continue
        
        # Extraire les informations depuis le fichier PDF
        PDF_PATH = f"Etudiants/{filename}"

        # Transformer le PDF en image
        transformer_en_img('.temp', PDF_PATH)
        
        # Afficher le nom de l'étudiant
        print(f"\t--------------- QCM : {filename} ---------------")

        # Calculer le temps d'exécution
        temps = 0
        
        # Extraire les informations pour chaque étudiant      
        temps += extraire(0) + extraire(1)
        print(f"> Le temps d'extraction est : {sec_en_min(temps)}\n")

        # Afficher les informations extraites
        temps = afficher(0)    
        print(f"> Le temps d'affichage est : {sec_en_min(temps)}\n")
        temps = afficher(1)    
        print(f"> Le temps d'affichage est : {sec_en_min(temps)}\n")

        
# Fonction 25 : calculer le nombre des pages dans un PDF
def nbr_pages(fich_pdf):
    # Ouvrir le PDF avec fitz
    doc = fitz.open(fich_pdf)
    count = 0
    
    # Parcourir toutes les pages du PDF et incrémenter le compteur
    for p in doc:
        count += 1

    # Retourner le nombre de pages
    return count

# Fonction 26 : tester si le PDF contient plusieurs étudiants ou non
def sepearer_pdf(fich_pdf):
    if nbr_pages(fich_pdf) == 1:
        return None
    
    # Créer le dossier de la question si nécessaire
    os.makedirs('.temp/images', exist_ok=True)

    # Transformer le PDF en images pour les traiter
    transformer_en_img('.temp/images', fichier_pdf)

    # Lister les fichiers qui se trouvent dans un dossier du chemin '.temp/images'
    liste = os.listdir('.temp/images')

    pages_num = []

    for chemin_img in liste:
        # Lire l'image, changer la taille et les couleurs
        image = inverser_image('.temp/images/'+chemin_img) 
        image = cv2.resize(image, (2481, 3508))
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]

        # Trouver les contours et les trier de gauche à droite
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts, _ = contours.sort_contours(cnts, "left-to-right")

        # Sélectionner uniquement les contours des questions
        detection_num = 0
        for c in cnts:
            if detection_num > 2:
                break
            
            area = cv2.contourArea(c)
            if area > 10:
                x,y,w,h = cv2.boundingRect(c)
                if (w >= 1370 and w <= 1375) and (h >= 385 and h <= 390):
                    # Si les dimensions w = 1371 et h = 389 existent dans une image alors c'est la première page d'un PDF
                    # on sauvegarde sa position (le nombre de la page)
                    pages_num.append(int(chemin_img.replace('page', '').replace('.jpg', '')))              
                    detection_num += 1

    if nbr_pages(fichier_pdf) == 2 and detection_num == 1:
        return None

    for page in pages_num:
        if valeur_suivante(pages_num, page) != None:
            diviser_pdf(fichier_pdf, page, valeur_suivante(pages_num, page) - 1)
        else:
            diviser_pdf(fichier_pdf, page, page)
            
    # Supprimer le dossier 'images'
    shutil.rmtree('.temp/images', ignore_errors=True)

    # Supprimer le fichier '.pdf'
    os.remove(fichier_pdf)

    return "Séparation terminée !"

"""
Fonction 27 :
    Divise un fichier PDF en un nouveau fichier contenant la plage de pages spécifiée.
    
    chemin_entree: Le chemin vers le fichier PDF d'entrée.
    page_debut: Le numéro de la page de début de la division.
    page_fin: Le numéro de la page de fin de la division.
    chemin_sortie: Le chemin vers le fichier PDF de sortie.
"""
def diviser_pdf(nom_fichier, page_debut, page_fin):
    # Ouverture du fichier PDF en mode lecture binaire
    with open(nom_fichier, 'rb') as fichier:
        # Lecture du contenu du fichier PDF
        pdf = PyPDF2.PdfReader(fichier)
        
        # Création d'un nouveau PDF contenant seulement les pages spécifiées
        nouveau_pdf = PyPDF2.PdfWriter()
        for i in range(page_debut-1, page_fin):
            # Ajout de chaque page du PDF original au nouveau PDF
            page = pdf.pages[i]
            nouveau_pdf.add_page(page)
            
        # Enregistrement du nouveau PDF dans un fichier
        nom_nouveau_fichier = f"{nom_fichier.replace('.pdf', '')}_{page_debut}-{page_fin}.pdf"
        with open(nom_nouveau_fichier, 'wb') as nouveau_fichier:
            nouveau_pdf.write(nouveau_fichier)

# Fonction 27 : trouver la valeur suivante
def valeur_suivante(tableau, valeur_actuelle):
    # Obtenir l'index de la valeur actuelle dans le tableau
    try:
        index_valeur_actuelle = tableau.index(valeur_actuelle)
    except ValueError:
        # Si la valeur actuelle n'est pas dans le tableau, retourner None
        return None
    
    # Vérifier s'il y a une valeur suivante dans le tableau
    if index_valeur_actuelle + 1 < len(tableau):
        # Si oui, retourner la valeur suivante
        return tableau[index_valeur_actuelle + 1]
    else:
        # Sinon, retourner None
        return None

# Fonction 28 : transformer les secondes en minutes
def sec_en_min(secondes):
    minutes = secondes // 60  # division entière pour obtenir le nombre de minutes
    secondes_restantes = secondes % 60  # modulo pour obtenir les secondes restantes
    return f"{int(round(minutes))}:{int(round(secondes_restantes))}min"

# =============================================
# Menus :
# =============================================

def premier_menu():
    # Supprimer le dossier '.temp' et son contenu
    supprimer_tempfile()

    # Nettoyer la console
    os.system('cls')

    # Afficher le menu
    print(">> Menu : 1/3\nExtraire les informations et les réponses\n")

    print("1. De tous les étudiants")
    print("2. D'un étudiant précis\n")

    print("0. Quitter\n")

    choix = input("\tChoisir une option : ")
    choix1(int(choix))

def choix1(opt):
    if opt == 1:
        t0 = time.time()
        extraire_etudiants()
        t1 = time.time()

        # Calculer le temps d'exécution en secondes
        temps = t1 - t0

        print(f"> Le temps d'exécution est : {sec_en_min(temps)}\n")
    elif opt == 2:
        # Aller vers le deuxième menu
        deuxieme_menu()
    elif opt == 0:
        quit()
    else:
        print("Option invalide.")
        premier_menu()

def deuxieme_menu():
    # Nettoyer le console
    os.system('cls')
        
    # Afficher le menu    
    if PDF_PATH != '':
        print(">> Menu : 3/3\n")
        print("1. Extraire les informations")
        print("2. Extraire les réponses")
        print("")

        if(os.path.exists('.temp/informations')):
            print("3. Afficher les informations")

        if(os.path.exists('.temp/reponses')):
            print("4. Afficher les réponses\n")

        print("5. Faire toutes les options\n")
    else:
        print(">> Menu : 2/3\n")
        print("1. Importer le QCM en PDF\n")

    print("9. Retourner")
    print("0. Quitter\n")

    choix = input("\tChoisir une option : ")
    choix2(int(choix))
        
def choix2(opt):
    if PDF_PATH != '':
        if opt == 1:      
            # Extraire les questions depuis le premier template du 1er page du qcm
            extraire(0)
                    
            # Revenir au menu
            deuxieme_menu()                      
        elif opt == 2:
            # Extraire les questions depuis la deuxieme template du 1er page du qcm
            extraire(1)
                    
            # Revenir au menu
            deuxieme_menu()
        elif opt == 3 and os.path.exists('.temp/informations'):
            # Temps d'affichage
            temps = (afficher(0))
            print(f"> Le temps de traitement et d'affichage est : {sec_en_min(temps)}\n")
            
            # Revenir au menu
            print("\n\n\tEntrez 'R' ou 'r' pour retourner au menu : ", end="")
            key = input()
            
            if key == 'R' or key == 'r': deuxieme_menu()
        
        elif opt == 4 and os.path.exists('.temp/reponses'):
            # Temps d'affichage
            temps = afficher(1)
            print(f"> Le temps de traitement et d'affichage est : {sec_en_min(temps)}\n")
              
            # Revenir au menu
            print("\n\n\tEntrez 'R' ou 'r' pour retourner au menu : ", end="")
            key = input()
            
            if key == 'R' or key == 'r': deuxieme_menu()

        elif opt == 5:
            # Supprimer le dossier '.temp'
            supprimer_tempfile()
            
            transformer_en_img('.temp', PDF_PATH)

            # Calculer le temps d'execution
            temps = 0
            temps += extraire(0) + extraire(1)
            temps += afficher(0) + afficher(1)
            print(f"> Le temps d'exécution est : {sec_en_min(temps)}\n")

            # Supprimer le dossier '.temp'
            supprimer_tempfile()
            
            print("\n\n\tEntrez 'Q' ou 'q' pour quitter le programme : ", end="")
            key = input()

            if key == 'Q' or key == 'q': quit()
        elif opt == 9: premier_menu()
        elif opt == 0: quit()                
        else: deuxieme_menu()   
    else:
        if opt == 1:      
            # Importer le pdf du qcm d'etudiant
            importerpdf()
            
            # Transformer le pdf en images
            transformer_en_img('.temp', PDF_PATH)
            
            # Revenir au menu
            deuxieme_menu()
        elif opt == 9: premier_menu()
        elif opt == 0: quit()                
        else: deuxieme_menu()

        
# =============================================
# Main Programme :
# =============================================

premier_menu()

