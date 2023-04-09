# Application de lecuture d'un template des pages d'un QCM avec Python et OpenCV
J'ai travaillé avec passion sur ce projet pour créer une application qui permet d'extraire les réponses d'un étudiant dans un QCM en utilisant Python et la bibliothèque OpenCV. Le projet m'a permis de développer mes compétences en programmation et en traitement d'images tout en répondant à un besoin concret dans l'éducation. La détection optique de caractères (OCR) a été l'un des outils essentiels pour identifier les réponses correctes. Je suis fier(e) d'avoir accompli ce projet avec succès et j'ai hâte de continuer à développer mes compétences techniques dans d'autres projets similaires.

## Outils utilisés
Nous avons utilisé dans la réalisation de cette application plusieurs outils les parmi, on trouve :

-   **OpenCV :** c'est une bibliothèque open-source de vision par ordinateur qui offre des fonctionnalités de traitement d'image, de reconnaissance d'objet et de suivi de mouvement. Vous pouvez utiliser OpenCV pour effectuer des opérations de prétraitement sur l'image, telles que le redimensionnement, le flou, la binarisation, la détection de contours et la reconnaissance de formes.
-   **Python :** c'est un langage de programmation populaire et facile à apprendre qui est souvent utilisé pour la vision par ordinateur et l'apprentissage automatique. Vous pouvez utiliser Python pour écrire le code de votre application et pour interagir avec les fonctions OpenCV.
-   **NumPy :** c'est une bibliothèque Python pour la manipulation de tableaux multidimensionnels. Vous pouvez utiliser NumPy pour traiter des tableaux d'images et pour effectuer des opérations mathématiques sur les pixels de l'image.
-   **PyTesseract :** c'est une bibliothèque Python pour la reconnaissance optique de caractères (OCR). Vous pouvez utiliser PyTesseract pour extraire le texte des réponses aux questions de votre QCM.
-   **fitz :** c'est une bibliothèque Python pour la manipulation de fichiers PDF. Vous pouvez utiliser fitz pour calculer les pages du QCM et transformer le QCM en images.
-   **PyPDF2 :** c'est une bibliothèque Python pour la manipulation de fichiers PDF. Vous pouvez utiliser PyPDF2 pour découper le QCM en plusieurs fichiers PDF.

Ces bibliothèques peuvent être utiles pour une variété de tâches liées aux fichiers PDF, telles que la manipulation de pages, la modification de métadonnées, l'extraction de texte et d'images, la conversion en d'autres formats, etc.

En utilisant différentes bibliothèques comme OpenCV, PyTesseract, fitz et PyPDF2, il est possible de réaliser plusieurs tâches liées aux fichiers PDF. Ces outils permettent de prétraiter les images pour faciliter la détection des questions et des réponses, extraire le texte des réponses, transformer les pages du QCM en images pour la reconnaissance de caractères (OCR), découper les fichiers PDF en plusieurs parties pour faciliter leur gestion et distribution.

En combinant ces bibliothèques, il est possible de créer une application qui prend en entrée une image de QCM, détecte les informations et les réponses, extrait le texte et les marqueurs de réponse, et produit une sortie sous forme de texte ou de tableau. Ainsi, il est possible d'automatiser la correction de QCM et de faciliter leur traitement. Voici une image du QCM sur lequel nous devons passer notre test :

<img src="https://user-images.githubusercontent.com/119759894/227744395-ccd879ed-4ac4-47f5-8963-6618f35b27c0.jpg" alt="image du qcm" width="500" align="center">

> Figure 1 : Image du notre QCM

## Réalisation de l’application

### Interface d'utilisateur
<img src="https://user-images.githubusercontent.com/119759894/227742507-8320711c-3c46-4f59-b8b4-ae47b05e020d.png" alt="image du menu 1" width="500" align="center">

>   Figure 2 : Menu principale

-   L'option 1 permet de traiter les QCMs de tous les étudiants qui sont stockés dans le dossier 'Etudiants/' situé dans le même emplacement que le programme. En choisissant cette option, le programme recherche automatiquement tous les QCMs des étudiants présents dans ce dossier et les traite selon les instructions programmées.
-   L'option 2 permet de passer à un deuxième menu. Cette option peut être utile si l'utilisateur souhaite effectuer une tâche spécifique qui n'est pas incluse dans le premier menu. En choisissant cette option, le programme affiche un nouveau menu qui présente des options supplémentaires pour l'utilisateur.
-   L'option 3 permet de quitter l'application. Si l'utilisateur choisit cette option, le programme se ferme immédiatement et l'utilisateur revient à l'interface de l'ordinateur ou du système d'exploitation qu'il utilise. Cette option est utile si l'utilisateur a terminé son travail dans le programme ou s'il souhaite quitter rapidement l'application sans effectuer d'autres tâches.

<img src="https://user-images.githubusercontent.com/119759894/227742517-b9691cd2-4ae1-479f-ac82-e18d1dc1f85a.png" alt="image du menu 2" width="500" align="center">

>   Figure 3 : Deuxième menu

-   Le choix [1] permet à l'utilisateur de sélectionner un QCM (au format PDF) d'un étudiant depuis l'ordinateur de l'étudiant, afin que le programme puisse poursuivre son traitement. Cette option offre la possibilité à l'utilisateur de spécifier manuellement le fichier PDF qu'il souhaite traiter, en naviguant dans les dossiers de l'ordinateur de l'étudiant pour trouver le fichier souhaité. Une fois le fichier sélectionné, le programme continuera à traiter le QCM selon les instructions programmées. Cette fonctionnalité est utile si l'utilisateur souhaite traiter des QCMs spécifiques qui ne sont pas stockés dans le dossier prédéfini 'Etudiants/' du programme.

<img src="https://user-images.githubusercontent.com/119759894/227742528-babcd4fe-a915-408c-bc4c-e0170bbb7912.png" alt="importer qcm" width="500" align="center">

>   Figure 4 : Importer un fichier PDF du QCM

-   Le choix [9], pour retourner au premier menu.

<img src="https://user-images.githubusercontent.com/119759894/227742547-17512a11-4c12-4bcf-af02-a88e35f518f8.png" alt="image du menu 3" width="500" align="center">

>   Figure 5 : Troisième menu

Lorsque l'utilisateur choisit l'option [1], le programme extrait automatiquement les informations de l'étudiant et de l'évaluation à partir du QCM PDF sélectionné et les stocke pour une utilisation ultérieure. L'option [3] est automatiquement ajoutée pour permettre à l'utilisateur d'afficher les informations extraites.

De même, lorsque l'utilisateur sélectionne l'option [2], le programme extrait automatiquement les réponses de l'étudiant à partir du QCM PDF sélectionné et les stocke pour une utilisation ultérieure. L'option [4] est automatiquement ajoutée pour permettre à l'utilisateur d'afficher les réponses extraites.

<img src="https://user-images.githubusercontent.com/119759894/227742554-284e416e-eed9-4325-b27c-2442a3ad86ab.png" alt="image du menu 3-2" width="500" align="center">

>   Figure 6 : Troisième menu (après choisir 1 et 2)

Résultat du choix [3], après quelques secondes :

<img src="https://user-images.githubusercontent.com/119759894/227742558-1bc73e66-4ce3-4e42-81cf-9fc796ea411b.png" alt="image du resultat 1" width="500" align="center">

>   Figure 7 : Tableau des informations

*Résultat du choix [4], après quelques minutes :*

<img src="https://user-images.githubusercontent.com/119759894/227742563-42a5f482-0efd-442b-81b0-8f1b154bf0a2.png" alt="image du resultat 2" width="500" align="center">

>   Figure 8 : Tableau des réponses

### Taches en arrière-plan

Le programme effectue plusieurs tâches en arrière-plan, notamment :

1.  Extraction des images à partir du QCM à traiter à l'aide de la bibliothèque OpenCV, en les renommant et en les enregistrant dans des dossiers distincts pour faciliter leur manipulation ultérieure. Ces images peuvent inclure des images de questions, des réponses et des images de caractères tels que le nom, le prénom, le cours, la section et la date d'évaluation.
2.  Parcours des dossiers contenant les images et traitement de ces dernières à l'aide de la bibliothèque Pytesseract, afin d'extraire le contenu textuel de chaque image.
3.  Stockage des résultats du traitement dans des variables et affichage des informations extraites dans la console utilisateur pour une utilisation ultérieure.

**Résumé :** Le programme extrait et traite les images à partir du QCM en utilisant OpenCV et Pytesseract pour extraire les informations textuelles telles que les noms, les matricules, les réponses, etc., et stocke les résultats dans des variables pour affichage dans la console utilisateur.

### Partie Code

Il existe plusieurs fonctions et méthodes importantes créées avec Python, parmi les :

-   **‘haute_qualite’ :** utilise des traitements d'images pour améliorer la qualité d'une image. Elle commence par convertir l'image en niveau de gris, puis applique un flou gaussien pour réduire le bruit. Ensuite, elle utilise une méthode de seuillage pour créer une image binaire à partir de l'image floue. Enfin, elle applique la morphologie de dilatation pour renforcer les contours de l'image. Le résultat final est retourné par la fonction.
-   **‘afficher_infos’** : permet d'extraire les informations depuis le QCM. Elle utilise la bibliothèque Pytesseract pour extraire le texte depuis les images des informations. Elle lit les images de la première page du QCM et extrait le nom, le prénom, le cours, la section, la date de l'évaluation et le matricule. La fonction appelle la fonction ‘extraire_matr’ pour extraire le matricule. Les informations sont ensuite affichées à l'écran en utilisant la fonction ‘print’. Enfin, la fonction supprime le dossier informations.
-   **‘afficher_reponses’ :** permet d'afficher les réponses d'un étudiant en se basant sur les images des réponses sauvegardées. Elle parcourt chaque question et chaque réponse de chaque question pour extraire le texte de l'image et trouver la réponse de l'étudiant en utilisant la fonction **‘trouver_reponse’**. Si la réponse n'a pas été trouvée, la fonction affiche "Aucune réponse". Si la réponse n'a pas été acceptée, la fonction affiche "La réponse est non acceptée". Sinon, la fonction affiche la réponse trouvée. Enfin, les dossiers de réponses sont supprimés.
-   **‘inverser_image’ :** prend le chemin d'une image en entrée, teste si elle est inversée à l'aide de la fonction ‘est_inversee’, et renvoie l'image inversée si elle est inversée, sinon renvoie l'image non inversée.

## Améliorations futures
Voici la liste des améliorations que nous avons prévues pour les futures versions de notre application d'extraction de réponses de QCM :

-   Amélioration de la reconnaissance de caractères en utilisant des algorithmes plus sophistiqués pour augmenter la précision.
-   Ajout d'une fonctionnalité de correction automatique pour permettre aux professeurs de corriger les QCM plus rapidement et plus efficacement.
-   Création d'une interface utilisateur graphique (GUI) pour simplifier l'utilisation de l'application.
-   Ajout d'une fonctionnalité de stockage des données extraites pour faciliter la gestion et la correction des QCMs.
-   Ajout d'une fonctionnalité de parallélisation des tâches et optimisation de la mise en cache pour augmenter la vitesse de détection des données avec pytessract (OCR).
-   Ajout d'une version anglaise pour faciliter l'utilisation par les utilisateurs anglophones.

Ces améliorations permettront de traiter rapidement un grand nombre de QCMs pour une gestion plus efficace des examens.

## Crédits
Ce projet a été réalisé par [OSSAMA ETTAQAFI](https://www.linkedin.com/in/afatratinmypocket/) en utilisant Python et la bibliothèque OpenCV pour la détection d'images et l'OCR. Il est libre de droit et peut être utilisé ou modifié à des fins non commerciales.
