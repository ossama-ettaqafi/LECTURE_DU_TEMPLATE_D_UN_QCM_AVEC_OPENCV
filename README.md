# 📄 Cahier des Charges – Application de Lecture de QCM avec OpenCV

## 📚 Table des Matières

- [🔍 Introduction](#-introduction)
- [🎯 Objectifs du Projet](#-objectifs-du-projet)
- [🛠️ Outils Utilisés](#-outils-utilisés)
- [⚙️ Fonctionnalités](#-fonctionnalités)
- [📐 Spécifications Techniques](#-spécifications-techniques)
- [🚀 Améliorations Futures](#-améliorations-futures)

## 🔍 Introduction

Ce projet a pour but de développer une application capable d’extraire automatiquement les réponses des étudiants à partir de QCM (Questionnaires à Choix Multiples) scannés ou en format PDF. Grâce à Python et à la bibliothèque OpenCV, cette application vise à automatiser la correction et faciliter le travail des enseignants.

## 🎯 Objectifs du Projet

- Automatiser l'extraction des réponses depuis des fichiers PDF de QCM.
- Utiliser le traitement d’image et l’OCR pour détecter et lire les réponses.
- Proposer une interface simple (ligne de commande).
- Obtenir une reconnaissance fiable et rapide des informations.

## 🛠️ Outils Utilisés

### Langage de Programmation

- **Python 3.x**

### Bibliothèques Principales

- [OpenCV](https://opencv.org/) – Traitement d'image
- [NumPy](https://numpy.org/) – Manipulation de matrices
- [PyTesseract](https://github.com/madmaze/pytesseract) – OCR (Reconnaissance Optique de Caractères)
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) – Lecture des fichiers PDF
- [PyPDF2](https://pythonhosted.org/PyPDF2/) – Manipulation des fichiers PDF

## ⚙️ Fonctionnalités

### Interface Utilisateur (CLI)

#### Menu Principal
- `1` – Traiter tous les QCMs d’un dossier prédéfini
- `2` – Accéder aux fonctions avancées
- `3` – Quitter

#### Menu Secondaire
- `1` – Sélectionner un QCM individuel
- `9` – Retour au menu principal

#### Menu Tertiaire
- `1` – Extraire les informations de l’étudiant
- `2` – Extraire les réponses de l’étudiant
- `9` – Retour au menu principal

### Fonctionnalités Techniques

- **Extraction de pages PDF**
- **Amélioration d’image** (ex. redressement, contraste)
- **Reconnaissance OCR** avec PyTesseract
- **Stockage des résultats** pour une analyse ultérieure

### Fonctions Clés

- `haute_qualite()` – Améliore la lisibilité des images
- `afficher_infos()` – Extrait les informations de l’étudiant
- `afficher_reponses()` – Extrait les réponses choisies

## 📐 Spécifications Techniques

### Configuration Requise

- **Matériel :** PC classique avec Python installé
- **Logiciel :** Python 3.x, bibliothèques listées ci-dessus

### Exigences de Performance

- **Précision OCR :** ≥ 95 %
- **Temps de traitement :** ≤ 2 minutes par QCM

## 🚀 Améliorations Futures

- 🔎 **Amélioration de la précision OCR**
- 🧠 **Correction automatique des réponses**
- 🖥️ **Ajout d’une interface graphique (GUI)**
- 📊 **Gestion et stockage des résultats**
- ⚡ **Optimisation des performances**

💡 *Ce projet est en cours de développement. Toute contribution est la bienvenue !*
