# Application de lecture d'un modèle de pages de QCM avec Python et OpenCV

**1. Introduction**

J'ai travaillé avec passion sur ce projet pour créer une application permettant d'extraire les réponses d'un étudiant dans un QCM en utilisant Python et la bibliothèque OpenCV. Le projet m'a permis de développer mes compétences en programmation et en traitement d'images tout en répondant à un besoin concret dans le domaine de l'éducation. La détection optique de caractères (OCR) a été l'un des outils essentiels pour identifier les réponses correctes. Je suis fier(e) d'avoir mené à bien ce projet et j'ai hâte de continuer à développer mes compétences techniques dans d'autres projets similaires.

**2. Outils Utilisés**

Dans la réalisation de cette application, j'ai utilisé plusieurs outils, parmi lesquels :

- **2.1. OpenCV :** Une bibliothèque open-source de vision par ordinateur qui offre des fonctionnalités de traitement d'image, de reconnaissance d'objet et de suivi de mouvement.
- **2.2. Python :** Un langage de programmation populaire et facile à apprendre souvent utilisé pour la vision par ordinateur et l'apprentissage automatique.
- **2.3. NumPy :** Une bibliothèque Python pour la manipulation de tableaux multidimensionnels, utile pour traiter des tableaux d'images et effectuer des opérations mathématiques sur les pixels de l'image.
- **2.4. PyTesseract :** Une bibliothèque Python pour la reconnaissance optique de caractères (OCR), utilisée pour extraire le texte des réponses aux questions du QCM.
- **2.5. fitz :** Une bibliothèque Python pour la manipulation de fichiers PDF, utilisée pour calculer les pages du QCM et transformer le QCM en images.
- **2.6. PyPDF2 :** Une bibliothèque Python pour la manipulation de fichiers PDF, utilisée pour découper le QCM en plusieurs fichiers PDF.

Ces bibliothèques sont utiles pour différentes tâches liées aux fichiers PDF, telles que la manipulation de pages, l'extraction de texte et d'images, la conversion en d'autres formats, etc.

**3. Réalisation de l'Application**

**3.1. Interface Utilisateur**

L'application propose une interface utilisateur conviviale avec plusieurs fonctionnalités :

**3.1.1. Menu Principal**
- *Option 1 :* Traitement des QCMs de tous les étudiants stockés dans un dossier prédéfini.
- *Option 2 :* Accès à un deuxième menu pour des tâches spécifiques.
- *Option 3 :* Quitter l'application.

**3.1.2. Deuxième Menu**
- *Choix 1 :* Sélection d'un QCM d'un étudiant à partir de l'ordinateur.
- *Choix 9 :* Retour au premier menu.

**3.1.3. Troisième Menu**
- *Choix 1 :* Extraction des informations de l'étudiant à partir du QCM.
- *Choix 2 :* Extraction des réponses de l'étudiant à partir du QCM.
- *Choix 9 :* Retour au premier menu.

**3.2. Tâches en Arrière-plan**

Le programme effectue plusieurs tâches en arrière-plan :
1. Extraction des images à partir du QCM avec OpenCV.
2. Traitement des images pour extraire le texte avec PyTesseract.
3. Stockage des résultats pour affichage et utilisation ultérieure.

**3.3. Fonctions Importantes**
- *'haute_qualite' :* Améliore la qualité d'une image en utilisant des traitements d'images.
- *'afficher_infos' :* Extrait et affiche les informations de l'étudiant à partir du QCM.
- *'afficher_reponses' :* Extrait et affiche les réponses de l'étudiant à partir du QCM.

**4. Améliorations Futures**

Voici quelques améliorations prévues pour les futures versions de l'application :
- Amélioration de la reconnaissance de caractères pour augmenter la précision.
- Ajout d'une fonctionnalité de correction automatique des QCM.
- Création d'une interface utilisateur graphique (GUI) pour une utilisation plus conviviale.
- Ajout d'une fonctionnalité de stockage des données pour une gestion plus efficace des QCM.
- Optimisation de la vitesse de détection des données avec l'OCR.

**Crédits** <br>
Ce projet a été réalisé par *OSSAMA ETTAQAFI* en utilisant Python et la bibliothèque OpenCV pour la détection d'images et l'OCR. Il est libre de droit et peut être utilisé ou modifié à des fins non commerciales.
