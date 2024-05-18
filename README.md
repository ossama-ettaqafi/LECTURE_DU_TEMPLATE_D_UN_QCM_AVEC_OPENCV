# Cahier des Charges pour l'Application de Lecture d'un Modèle de Pages de QCM avec Python et OpenCV

## Table des Matières

- [Introduction](#introduction)
- [Objectifs du Projet](#objectifs-du-projet)
- [Outils Utilisés](#outils-utilisés)
- [Fonctionnalités](#fonctionnalités)
- [Spécifications Techniques](#spécifications-techniques)
- [Améliorations Futures](#améliorations-futures)

## Introduction

Ce cahier des charges détaille le développement d'une application permettant d'extraire les réponses des étudiants à partir de QCM (Questionnaire à Choix Multiples) en utilisant Python et OpenCV. Cette application vise à automatiser la correction des QCM et à fournir une solution efficace pour les enseignants et les institutions éducatives.

## Objectifs du Projet

- Automatiser l'extraction des réponses des étudiants à partir de QCM scannés ou en format PDF.
- Utiliser des techniques de traitement d'image et de reconnaissance optique de caractères (OCR) pour extraire les informations pertinentes.
- Fournir une interface utilisateur intuitive pour faciliter l'utilisation de l'application.
- Assurer la précision et la fiabilité de l'extraction des données.

## Outils Utilisés

### Bibliothèques et Langages
- **Python :** Langage principal pour le développement de l'application.
- **OpenCV :** Bibliothèque pour le traitement d'images et la reconnaissance d'objets.
- **NumPy :** Pour la manipulation de tableaux multidimensionnels.
- **PyTesseract :** Pour la reconnaissance optique de caractères (OCR).
- **fitz (PyMuPDF) :** Pour la manipulation de fichiers PDF.
- **PyPDF2 :** Pour découper et manipuler les fichiers PDF.

## Fonctionnalités

### Interface Utilisateur
L'application disposera d'une interface en ligne de commande (CLI) avec les menus suivants :

#### Menu Principal
- **Option 1 :** Traiter les QCMs de tous les étudiants stockés dans un dossier prédéfini.
- **Option 2 :** Accéder à un menu pour des tâches spécifiques.
- **Option 3 :** Quitter l'application.

#### Deuxième Menu
- **Choix 1 :** Sélectionner un QCM d'un étudiant à partir de l'ordinateur.
- **Choix 9 :** Retourner au menu principal.

#### Troisième Menu
- **Choix 1 :** Extraire les informations de l'étudiant à partir du QCM.
- **Choix 2 :** Extraire les réponses de l'étudiant à partir du QCM.
- **Choix 9 :** Retourner au menu principal.

### Fonctionnalités Techniques
- **Extraction des images :** Extraire les pages du QCM à partir de fichiers PDF.
- **Traitement des images :** Améliorer la qualité des images pour une meilleure reconnaissance.
- **OCR :** Utiliser PyTesseract pour extraire le texte des réponses.
- **Stockage des résultats :** Enregistrer les données extraites pour une utilisation ultérieure.

### Fonctions Importantes
- **'haute_qualite':** Améliorer la qualité des images.
- **'afficher_infos':** Extraire et afficher les informations de l'étudiant.
- **'afficher_reponses':** Extraire et afficher les réponses de l'étudiant.

## Spécifications Techniques

### Exigences Matérielles et Logiciels
- **Matériel :** Ordinateur avec une configuration de base suffisante pour exécuter Python et OpenCV.
- **Logiciel :** Python 3.x, OpenCV, NumPy, PyTesseract, fitz (PyMuPDF), PyPDF2.

### Exigences de Performance
- **Précision :** L'application doit atteindre un taux de précision d'au moins 95% pour la reconnaissance des caractères.
- **Vitesse :** L'application doit traiter un QCM en moins de 2 minutes.

## Améliorations Futures

- **Amélioration de l'OCR :** Améliorer la précision de la reconnaissance de caractères.
- **Correction Automatique :** Ajouter une fonctionnalité pour corriger automatiquement les QCM.
- **Interface Graphique (GUI) :** Développer une interface utilisateur graphique pour une utilisation plus conviviale.
- **Gestion des Données :** Ajouter une fonctionnalité pour le stockage et la gestion des données des QCM.
- **Optimisation des Performances :** Optimiser la vitesse de détection et de traitement des données.
