'''

        ----------------- Concept du programme --------------------
        
        est d'extraire les reponses faites par un etudiant
        dans un qcm precis (ce projet a ete fait seulement pour
        traiter ce qcm, donc tous les tailles et les positions
        dependent a ce dernier)

        la lecture de l'image peut prend le temps seulent le
        pytesseract {il faut l'installer dans votre PC et preciser
        le chemin "D:\Program Files\Tesseract-OCR\tesseract.exe")
        
        -----------------------------------------------------------

        Ce programme est devloppe par OSSAMA ETTAQAFI , en 2023
        Contact : ossamaett2002@gmail.com
        Version : 1.0.0
        
'''

# L'importation des modules
import cv2
import time
import os
import os.path
import pytesseract
import numpy as np
import shutil
import fnmatch
import tkinter as tk
import fitz         # pip install PyMuPDF==1.16.14

from tkinter import filedialog
from imutils import contours

pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files\Tesseract-OCR\tesseract.exe"

# Declaration des tableaux
nom_prenom = np.full(31, '')
cours_sec = np.full(31, '')
date_eva = np.full(10, '')

dossier = ['nom_prenom', 'cours_sec', 'date_eva']

chiffre = np.full(10, '')
matricule = np.full(6, '')

qcm_path = ['.temp/page1.jpg', '.temp/page2.jpg']
pdf_path = ''

# Fonction 1 : permet d'ameliorer la qualite d'une image
def haute_qualite(image):
    # Convertir l'image au mode grayscale et faire le blur a l'image
    gray_sele = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray_sele,(7,7),0)
                    
    # Appliquer l'inverse thresh_binary 
    binary = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Appliquer la dilatation
    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)

    return thre_mor

# Fonction 2 : tester si la valeur existe
# Retourner : faux si la valeur n'existe pas
#             vrai si la valeur existe
def setrouve(val, tab):
    existe = False
    
    for i in range(len(tab)):
        if val == tab[i]:
            existe = True
            break

    return existe

# Fonction 3 : calculer le nombre des fichiers qui ce trouvent dans un dossier
def nbr_fichier(path_dossier):
    # Lister les fichiers qui se trouvent dans un dossier du path 'path_dossier'
    lst = os.listdir(path_dossier)

    # Calculer la taille de la liste
    nbr_fichiers = len(lst)
    
    return nbr_fichiers

# Fonction 4 : permet de transformer un tableau en chaine de caracteres et l'inverser
def tab2str(tableau):
    string = ''
    for i in range(len(tableau)):
        if tableau[i] == '':
            string = string + ' '
        else:
            string = string + tableau[i]

    return string[::-1]

# Fonction 5 : calculer le nombre des questions dans un qcm du path donne
def calculer_qsts(img_path):
    #Lire l'image, Changer la taille et les couleurs
    image = inverser_image(img_path)
    image = cv2.resize(image, (2481, 3508))
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]

    # Trouvver les contours, les trier depuis le gauche au droit
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts, _ = contours.sort_contours(cnts, "left-to-right")

    num = 0
    
    # Selectioner seulement les contour des questions
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 10:
            x,y,w,h = cv2.boundingRect(c)

            if (h >= 150 and h <= 160) and (w >= 635 and w <= 645):
                 num = num + 1
                 
    return num

# Fonction 6 : permet d'extraire toutes les images des questions depuis le path du qcm donne
def images_qsts(img_path):
    #Lire l'image, Changer la taille et les couleurs
    image = inverser_image(img_path)
    image = cv2.resize(image, (2481, 3508))
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]

    # Trouvver les contours et les trier depuis le gauche au droit
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts, _ = contours.sort_contours(cnts, "left-to-right")

    # Selectioner seulement les contours des questions
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 10:
            x,y,w,h = cv2.boundingRect(c)

            if (h >= 150 and h <= 160) and (w >= 635 and w <= 645):
                # Selectioner la question
                selected = image[y:y+h, x:x+w]
                selected = cv2.resize(selected, (w*6,h*6))
                            
                # Selectioner le nombre de la question
                qx=0 
                qy=360
                ques_num = selected[qy:qy+270, qx:qx+398]
                
                # Rendre l'image plus lisable
                ques_num = haute_qualite(ques_num)
       
                number = pytesseract.image_to_string(ques_num, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
                number = number.replace('\n', ' ').replace('\r', '').replace(' ', '')
        
                # Sauvegarder les images dans le dossier 'questions'
                # questions/numero_question.jpg              
                cv2.imwrite('.temp/questions/{}.jpg'.format(number), selected)

# Fonction 7 : permet d'extraire les images des responses depuis l'image d'une question a path donne
            # qst_path : le chemin de l'image
            # nbr_quest : le nombre de la question
def images_rpns(qst_path, nbr_quest):
    # Lire l'image
    img = cv2.imread(qst_path)
    img = cv2.resize(img, (900, 240))

    # Changer les couleurs de l'image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
    contours,hierarchy = cv2.findContours(thresh, 1, 2)

    for cnt in contours:
        x1,y1 = cnt[0][0]
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if len(approx):
            x, y, w, h = cv2.boundingRect(cnt)

            if (h >= 40 and h <= 46) and (w >= 55 and w <= 65):
                # Selectioner seulement le chiffre qui existe dans l'image du choix d'une question
                x, y, h, w = (x + 15, y + 7, h - 13, w - 28)

                selected = img[y:y+h, x:x+w]
                selected = cv2.resize(selected, (440, 550))

                # Ameliorer la qualite de l'image
                #selected = haute_qualite(selected)
                kernel = np.ones((5, 5), np.uint8)
                img_erosion = cv2.erode(img, kernel, iterations=1)

                if 160 <= y and y <= 170: ch = '2'
                else: ch = '1'

                # Tester si les dossiers deja existent, sinon il va les crees
                if(os.path.exists('.temp/reponses/'+str(nbr_quest)+'/{}/'.format(ch))==False):
                    num = 1
                    os.mkdir('.temp/reponses/'+str(nbr_quest)+'/{}/'.format(ch))

                # Enregistrer chaques reponses dans des dossiers specifies
                # num_question/ligne/num_reponse.jpg       
                path = '.temp/reponses/'+str(nbr_quest)+'/{}/'.format(ch)+str(num)+'.jpg'
                cv2.imwrite(path, selected)

                num += 1
            
# Fonction 8 : permet d'extraire les images des responses depuis un nombre precis des questions
               # nbr_qsts : le nombre des questions dans un qcm
def extraire_rpns_qsts(nbr_qsts):
    for q in range(nbr_qsts):
        # Tester si les dossiers deja existent, sinon il va les crees
        if(os.path.exists('.temp/reponses')==False):
            os.mkdir('.temp/reponses')
        
        if(os.path.exists('.temp/reponses/'+str(q+1))==False):
            os.mkdir('.temp/reponses/'+str(q+1))

        # Faire la tache pour chaque question
        images_rpns('.temp/questions/{}.jpg'.format(q+1), q+1)

# Fonction 9 : completer les cases du tableau par ''
def completer_tab(tab):
    ntab = np.full(7, '')
    # Completer le tableau
    for i in range(7):
        if i < len(tab):
            ntab[i] = tab[i]
        else:
            ntab[i] = ''
            
    return ntab

# Fonction 10 : trouver la reponse de l'utilisateur
# Le contenue de l'image : qui n'a pas ete reconnu/reste vide c'est la reponse d'utilisateur
#                          qui a ete reconnu ce choix n'est pas touche par l'utilisateur, ce n'est pas la reponse      
def trouver_reponse(rep1, rep2):
    tab = ["T","A","5","4","3","2","1"]
    rep = np.full((2,7), '')

    if len(rep1) < 7: rep1 = completer_tab(rep1)
    if len(rep2) < 7: rep2 = completer_tab(rep2)

    rep[0] = rep1
    rep[1] = rep2

    fois = 0
    reponse = ''

    j = 1
    while j >= 0:
        i = 0
        while i < 7:
            if fois > 1:
                return -1 #'la reponse est non acceptee'
            
            if setrouve(tab[i], rep[j]) == False : 
                reponse = tab[i]
                return reponse
                fois += 1
            
            i += 1

            if i == 7 and fois == 1:
                return reponse
        j -= 1
        
    if fois == 0:
        return reponse

# Fonction 11 : permet d'afficher les reponses d'etudiant depuis les images des reponses sauvegardes
def afficher_reponses(nbr_ques):
    print("\t> Les reponses :")
    #print("Entrain de traiter, s'il vous plait attender quelques secondes...")
    for q in range(nbr_ques):
        for d in range(2):
            dossier = '.temp/reponses/'+str(q+1)+'/{}/'.format(d+1)
            nf = nbr_fichier(dossier)
            
            # Declaration d'un tableau de (nf) cases
            if d == 0: r1 = np.full(nf, '')
            elif d == 1: r2 = np.full(nf, '')

            for i in range(nf):       
                # Lire l'image
                img = cv2.imread(dossier+'/{}.jpg'.format(i+1))
                
                # Extraire le texte depuis l'image, seulement les caracteres 12345AT
                data = pytesseract.image_to_string(img, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=12345AT')
                data = data.replace('\n', ' ').replace('\r', '').replace(' ', '')
                 
                if d == 0: r1[i] = data
                elif d == 1: r2[i] = data
                
        # Tester la reponse qui se trouve dans le tableau puis l'afficher
        if trouver_reponse(r1, r2) == '':
            print('[ Question '+str(q+1)+' - Aucune reponse ]')
        else:  
            if trouver_reponse(r1, r2) == -1:
                print('[ Question '+str(q+1)+' - La reponses est : la reponse est non acceptee ]')
            else:
                print('[ Question '+str(q+1)+' - La reponses est : ' + trouver_reponse(r1, r2) + ' ]')
            
    # Supprimer les dossiers 'reponses'
    shutil.rmtree('reponses', ignore_errors=True)

# Fonction 12 : permet d'extraire les informations d'etudiant et de l'evaluation (nom, prenom, matricule, date d'evaluation)
def images_infos(img_path):
    # Lire l'image
    image = inverser_image(img_path)
    image = cv2.resize(image, (2481, 3508))

    # Changer les couleurs de l'image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
    cnts,hierarchy = cv2.findContours(thresh, 1, 2)
    cnts, _ = contours.sort_contours(cnts, "top-to-bottom")
    
    num = 1
    i = 0
    for cnt in cnts:
       x1,y1 = cnt[0][0]
       approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
       if len(approx):
            x, y, w, h = cv2.boundingRect(cnt)
            
            if (h >= 500 and h <= 550) and (w >= 800 and w <= 850):
                # Extraire l'image du matricule
                # Selectioner la case
                selected = image[y:y+h, x:x+w]                  
              
                # Tester si les dossiers deja existent, sinon il va les crees
                if(os.path.exists('.temp/informations/matricule')==False):
                    os.mkdir('.temp/informations/matricule')
    
                # Sauvegarder l'image dans le dossier 'matricule'           
                cv2.imwrite('.temp/informations/matricule/matricule.jpg', selected)
                
            if (h>=50 and h<=60) and (w>=30 and w<=40):
                if num > 31:
                    num = 1
                        
                # Selectioner la case
                selected = image[y:y+h, x:x+w]
                selected = cv2.resize(selected, (w*5, h*5))

                # Rendre l'image plus lisable
                selected = haute_qualite(selected)
                
                # Extraire l'image des caracteres : nom/prenom et cours/section
                if (y>=170 and y<=185) or (y>=235 and y<=250):          
                    if y>=170 and y<=185: i = 0
                    else: i = 1
                                            
                # Extraire l'image des caracteres : date d'evaluation
                if y >= 300 and y <= 320:
                    i = 2

                # Tester si les dossier deja existent, sinon il va les crees
                if(os.path.exists('.temp/informations/'+dossier[i])==False):
                    os.mkdir('.temp/informations/'+dossier[i])
    
                # Sauvegarder les images dans des dossiers specifiques           
                cv2.imwrite('.temp/informations/'+dossier[i]+'/{}.jpg'.format(num), selected)

                num = num + 1

# Fonction 13 : permet d'extraire les zones a remplir qui se trouve dans l'image du matricule
def images_mtr(matr_path):
    # Lire l'image
    img = cv2.imread(matr_path)
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

                # Rendre l'image plus lisable
                selected = haute_qualite(selected)
                    
                # Tester si les dossiers deja existent, sinon il va les crees
                if ch != '0':
                    if(os.path.exists('.temp/informations/matricule/{}/'.format(ch))==False):
                        num = 1
                        os.mkdir('.temp/informations/matricule/{}/'.format(ch))
                else:
                    num = 1
                    
                # Enregistrer les chiffres des matricules dans des dossier
                # informations/matricule/nbr_chiffre/matr.jpg
                if ch == '0': path = '.temp/informations/matricule/'+str(num)+'.jpg'
                else: path = '.temp/informations/matricule/{}/'.format(ch)+str(num)+'.jpg'
                cv2.imwrite(path, selected)
                
                num += 1

# Fonction 14 : trouver le nombre masque depuis le tableau
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

# Fonction 15 : completer et trier le matricule
def completer_trier(tab):
    # Completer le tableau
    if len(tab) < 10:
        i = len(tab) - 1
        while i < 10:
            tab[i] = ''
            i += 1

    # Trier le tableau de 9 jusqu'a 0
    base = ['9','8','7','6','5','4','3','2','1','0']

    for i in range(10):
        if setrouve(base[i], tab) == False:
            base[i] = ''
        
    return base

# Fonction 16 : permet d'extraire le matricule depuis la premiere page du qcm
def extraire_matr():
        # Lire le contenu des images puis extraire le nombre masque dans l'image
        for i in range(6):
                im_num = 0

                if i == 0:
                    nf = 1
                else:
                    dossier = '.temp/informations/matricule/'+str(i)+'/'
                    nf = nbr_fichier(dossier)
            
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
                        data = data.replace('\n', ' ').replace('\r', '').replace(' ', '')
                        if i == 0:
                            if data == '':
                                matricule[0] = 'P'
                            break
                        else: chiffre[j] = data
        
                if i != 0 :
                    tab = np.full(len(chiffre),'')
                    tab = completer_trier(chiffre)                 
                    matricule[i] = nombre_masque(tab)

        return tab2str(matricule)[::-1]

# Fonction 17 : permet d'extraire les informations depuis le qcm
def afficher_infos():
    print("\t> Les informations :")
    #print("Entrain de traiter, s'il vous plait attender quelques secondes...")
    for i in range(3):
        if i == 0 or i == 1:
            r = range(31)
        elif i == 2:
            r = range(10)
            
        for j in r:         
            # Lire l'image
            img = cv2.imread('.temp/informations/' + dossier[i] + '/{}.jpg'.format(j+1))
            img = cv2.resize(img, (200, 400))

            w, h, x, y = (148, 350, 23, 30)       
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
                
    # Pour tester
    matricule = extraire_matr()
    print("[ Date de l'evaluation : " + tab2str(date_eva)+ " ]")
    print("[ Nom et prenom : " + tab2str(nom_prenom).rstrip() + " ]")
    print("[ Matricule : " + matricule + " ]")
    print("[ Cours et section : " + tab2str(cours_sec).rstrip() + " ]")

    # Supprimer le dossier 'informations'
    shutil.rmtree('.temp/informations', ignore_errors=True)
    
# Fonction 18 : permet d'extraire les images des donnees depuis un qcm
               # 0 - les informations
               # 1 - les responses
def extraire(type):
    print("Entrain d'extraire depuis le qcm, attendez quelques secondes s'il vous plait...")
    # Extraire les informations qui existe au haut de la premiere page du qcm
    if type == 0:
            # Tester si le dossier deja existe, sinon il va le creer
            if(os.path.exists('.temp/informations')==False):
                os.mkdir('.temp/informations')
                
            images_infos(qcm_path[0])
            images_mtr('.temp/informations/matricule/matricule.jpg')

            # Ouvrir le dossier 'informations'
            #os.startfile(".temp\informations")
            
    # Extraire les questions pour faciliter la facon d'extraire les reponses
    elif type == 1:
            # Tester si le dossier deja existe, sinon il va le creer
            if(os.path.exists('.temp/questions')==False):
                os.mkdir('.temp/questions')
            
            images_qsts(qcm_path[0])
            images_qsts(qcm_path[1])

            extraire_rpns_qsts(calculer_qsts(qcm_path[0]) + calculer_qsts(qcm_path[1]))

            # Supprimer le dossier 'questions'
            shutil.rmtree('.temp/questions', ignore_errors=True)
    
            # Ouvrir le dossier 'reponses'
            #os.startfile(".temp\reponses")
            
    print("L'extraction est termine avec success!")
    
# Fonction 19 : permet d'afficher les donnees depuis un qcm
               # 0 - les informations
               # 1 - les responses
def afficher(type):
    if type == 0:
        afficher_infos()
    elif type == 1:
        afficher_reponses(calculer_qsts(qcm_path[0]) + calculer_qsts(qcm_path[1]))

# Fonction 20 : importer un fichier pdf
def importerpdf():
    global pdf_path
    pdf_path = filedialog.askopenfilename()
    
    while ".pdf" not in pdf_path:
        print("S'il vous plait importer un fichier pdf!")
        pdf_path = filedialog.askopenfilename()

    print(f"Chemin du fichier : {pdf_path}")

# Fonction 21 : transformer le pdf en image
def transforerenimg(pdffile):
    doc = fitz.open(pdffile)
    zoom = 4
    mat = fitz.Matrix(zoom, zoom)
    count = 0

    for p in doc:
        count += 1
        
    # Tester si le dossier deja existe, sinon il va le creer
    if(os.path.exists('.temp')==False):
        os.mkdir('.temp')   
        
    for i in range(count):
        val = f".temp/page{i+1}.jpg"
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=mat)
        pix.save(val)
    doc.close()

# Fonction 22 : extraire les informations depuis tous les qcms des etudiants qui existe
#               dans le dossier 'Etudiants'

def extraire_etudiants():
    lst = os.listdir('Etudiants/')

    for i in range(len(lst)):

        if '.pdf' not in lst[i]:
            continue
        else:
            transforerenimg('Etudiants/'+lst[i])
            
        print(f"\t\t====== Etudiant {i+1} ======")
        extraire(0)
        os.system('cls')
        extraire(1)
        os.system('cls')
        
        afficher(0)
        afficher(1)

# Fonction 23 : tester si l'image est inversee
#           Retourner True : si l'image est inversee
#           Retourner False : si l'image n'est pas inversee
def est_inversee(img_path):
    # Declarer un tableau
    tableau = np.full(24,'')
    
    # Lire l'image
    image = cv2.imread(img_path)
    image = cv2.resize(image, (2481, 3508))

    # Changer les couleurs de l'image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
    cnts,hierarchy = cv2.findContours(thresh, 1, 2)
    cnts, _ = contours.sort_contours(cnts, "left-to-right")

    for cnt in cnts:
       x1,y1 = cnt[0][0]
       approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
       if len(approx):
            x, y, w, h = cv2.boundingRect(cnt)
            
            if (h >= 150 and h <= 160) and (w >= 635 and w <= 645):
                # Selectioner la case
                image = image[y:y+h, x:x+w]
                
                x, y, h, w = (105, 55, 38, 376)
                
                selected = image[y:y+h, x:x+w]
                selected = cv2.resize(selected, (w*5, h*5))

                # Rendre l'image plus lisable
                selected = haute_qualite(selected)
        
                data = pytesseract.image_to_string(selected)
                data = data.replace('\n', ' ').replace('\r', '').replace(' ', '')
                tableau = data

                break

    if tableau == 'unecasemaximumparligne':
        return False
    else:
        return True

# Fonction 24 : Reverser l'image
def inverser_image(img_path):
    img = cv2.imread(img_path)
    
    if est_inversee(img_path) == True:
        img = cv2.flip(img, -1)

    return img
    
# =============================================
# Menu :
# =============================================

def menu1():
    # Supprimer le dossier '.temp' et son contenu
    shutil.rmtree('.temp', ignore_errors=True)
    
    # Nettoyer le console
    os.system('cls')
        
    # Afficher le menu
    print("> Menu : 1/2\nExtraire les infomations et les reponses...")
    
    print("[1] De tous les etudiants")
    print("[2] D'un etudiant precis")

    print("\n[0] Quitter")
    
    print("\n\tChoisir une option : ", end="")
    cle = input()
    choix1(cle)  

def choix1(opt):
    if opt == '1':
        extraire_etudiants()                    
    elif opt == '2':
        # Aller vers le deuxieme menu
        menu2()
    elif opt == '0': quit()                
    else: menu()   
            
def menu2():
    # Nettoyer le console
    os.system('cls')
        
    # Afficher le menu
    print("> Menu : 2/2")
    
    if pdf_path != '':
        print("[1] Extraire les informations")
        print("[2] Extraire les reponses")
        
        if(os.path.exists('.temp/informations')):
            print("[3] Afficher les informations")

        if(os.path.exists('.temp/reponses')):
            print("[4] Afficher les reponses")

        print("\n[5] Faire tous les options")    
    else:
        print("[1] Importer le qcm en pdf")

    print("\n[9] Retourner")
    print("[0] Quitter")
    
    print("\n\tChoisir une option : ", end="")
    cle = input()
    choix2(cle)
        
def choix2(opt):
    if pdf_path != '':
        if opt == '1':      
            # Extraire les questions depuis les deux templates du qcm
            extraire(0)
                    
            # Revenir au menu
            menu()                      
        elif opt == '2':
            # Extraire les questions depuis les deux templates du qcm
            extraire(1)
                    
            # Revenir au menu
            menu()
        elif opt == '3' and os.path.exists('.temp/informations'):
            # Afficher les informations d'etudiant
            afficher(0)
            
            # Revenir au menu
            print("\n\n\tEntrez 'R' ou 'r' pour retourner au menu : ", end="")
            key = input()
            
            if key == 'R' or key == 'r': menu()
            
        elif opt == '4' and os.path.exists('.temp/reponses'):
            # Afficher les reponses d'etudiant
            afficher(1)
                
            # Revenir au menu
            print("\n\n\tEntrez 'R' ou 'r' pour retourner au menu : ", end="")
            key = input()
            
            if key == 'R' or key == 'r': menu()

        elif opt == '5':
            extraire(0)
            os.system('cls')
            extraire(1)
            os.system('cls')
            
            afficher(0)
            afficher(1)

            # Supprimer le dossier '.temp'
            shutil.rmtree('.temp', ignore_errors=True)
            
            print("\n\n\tEntrez 'Q' ou 'q' pour quitter le programme : ", end="")
            key = input()

            if key == 'Q' or key == 'q': quit()
        elif opt == '9': menu1()
        elif opt == '0': quit()                
        else: menu()   
    else:
        if opt == '1':      
            # Importer le pdf du qcm d'etudiant
            importerpdf()
            
            # Transformer le pdf en images
            transforerenimg(pdf_path)
            
            # Revenir au menu
            menu()
        elif opt == '9': menu1()
        elif opt == '0': quit()                
        else: menu()        

# =============================================
# Main Programme :
# =============================================

# Afficher le menu
menu1()

# ============================================
# Fonctions a utilisees
# ============================================

def returner_lesreponses(nbr_ques):
    print("Entrain de traiter, s'il vous plait attender quelques secondes...")
    questions = np.full(nbr_ques, '')
    
    for q in range(nbr_ques):
        for d in range(2):
            dossier = '.Temp/reponses/'+str(q+1)+'/{}/'.format(d+1)
            nf = nbr_fichier(dossier)
            
            # Declaration d'un tableau de (nf) cases
            if d == 0: r1 = np.full(nf, '')
            elif d == 1: r2 = np.full(nf, '')

            for i in range(nf):       
                # Lire l'image
                img = cv2.imread(dossier+'/{}.jpg'.format(i+1))
                
                # Extraire le texte depuis l'image, seulement les caracteres 12345AT
                data = pytesseract.image_to_string(img, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=12345AT')
                data = data.replace('\n', ' ').replace('\r', '').replace(' ', '')
                  
                if d == 0: r1[i] = data
                elif d == 1: r2[i] = data
                
        # Tester la reponse qui se trouve dans le tableau puis l'afficher
        # Tester la reponse qui se trouve dans le tableau puis l'afficher
        if trouver_reponse(r1, r2) == '':
            questions[q] = 'V'
        else:  
            if trouver_reponse(r1, r2) == -1:
                questions[q] = 'E'
            else:
                questions[q] = trouver_reponse(r1, r2)
       
    # Supprimer les dossiers 'reponses'
    shutil.rmtree('reponses', ignore_errors=True)

    return questions

def retourner_lesinfos():
    print("Entrain de traiter, s'il vous plait attender quelques secondes...")
    infos = np.full((4, 31), '')
    
    for i in range(3):
        if i == 0 or i == 1:
            r = range(31)
        elif i == 2:
            r = range(10)
            
        for j in r:         
            # Lire l'image
            img = cv2.imread('.Temp/informations/' + dossier[i] + '/{}.jpg'.format(j+1))
            img = cv2.resize(img, (200, 400))

            w, h, x, y = (148, 350, 23, 30)       
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
                
    # Pour tester
    matricule = extraire_matr()

    infos[0] = tab2str(date_eva)
    infos[1] = tab2str(nom_prenom).rstrip()
    infos[2] = matricule
    infos[3] = tab2str(cours_sec).rstrip()

    # Supprimer le dossier 'informations'
    shutil.rmtree('.Temp/informations', ignore_errors=True)

    return infos

def supprimer_tempfile():
    # Supprimer le dossier '.Temp'
    shutil.rmtree('.Temp', ignore_errors=True)

# Faire tous les taches
def faire_tous(chemin_du_qcmpdf):
    transforerenimg(chemin_du_qcmpdf)
    extraire(0)
    extraire(1)
    
    tableau_infos = retourner_lesinfos()
    tableau_reponses = returner_lesreponses()
	
    print(tableau_infos)
    print(tableau_reponses)

    supprimer_tempfile()

    f = open("depuis qcm.php", "a")
    f.write("<php>\n")
    f.write(f"$tableau_infos = {tableau_infos}\n")
    f.write(f"$tableau_reponses = {tableau_reponses}\n")
    f.write("</php>")
    f.close()

# Fonction qui s'execute
#faire_tous("Etudiants/e1")

    
