
# 📊 Projet d’Analyse de Ventes ( Python)


🔗 Dépôt GitHub : https://github.com/maymoun-a/pfa.git

Ce projet est un système d’analyse de données de ventes simulées développé en Python.  
Il contient deux versions :

- 🖥️ Mode Terminal (CLI)
- 🌐 Dashboard interactif avec Streamlit

---

## 🚀 Fonctionnalités

- Génération automatique de données de ventes (`vente.csv`)
- Traitement de grandes données avec le chunking (Pandas)
- Calcul des indicateurs clés :
  - Chiffre d’affaires total
  - Chiffre d’affaires par produit
  - Top produits
- Export des résultats en CSV (`resultats.csv`)
- Visualisations graphiques :
  - Bar chart (Top produits)
  - Histogramme
  - Scatter plot
  - Diagramme circulaire (Top vs autres)

---

## 📁 Structure du projet

```

project/
│
├── vente sans dashbord.py      # Version terminal (CLI)
├── dashbord.py      # Dashboard Streamlit
├── vente.csv             # Données générées
├── resultats.csv         # Résultats de l’analyse
└── README.md

````

---

## 🖥️ 1. Mode Terminal

### ▶️ Exécution :

```bash
python vente sans dashbord.py terminal
````

### 📌 Fonctionnement :

* Demande le nombre de ventes et de produits
* Génère automatiquement les données
* Calcule les performances des produits
* Affiche le Top 10
* Crée automatiquement :

  * `vente.csv`
  * `resultats.csv`

---

## 🌐 2. Dashboard Streamlit

### ▶️ Lancer l’application :

```bash
streamlit run dashbord.py
```

### 📌 Fonctionnalités :

* Import d’un fichier CSV ou génération automatique
* Tableau de bord interactif
* KPI dynamiques
* Graphiques :

  * Top 10 produits (bar chart)
  * Distribution des ventes (scatter)
  * Histogramme
  * Camembert (Top 3 vs autres)
* Aperçu des données

---

## 📊 Structure des données

| Colonne  | Description                |
| -------- | -------------------------- |
| ID       | Identifiant produit        |
| Prix     | Prix unitaire              |
| Quantite | Quantité vendue            |
| Remise   | Remise appliquée (%)       |
| CA       | Chiffre d’affaires calculé |

---

## ⚙️ Installation

### Installer les dépendances :

```bash
pip install pandas numpy matplotlib streamlit
```

---

## 🧠 Technologies utilisées

* Python
* Pandas (analyse de données)
* NumPy (génération de données)
* Matplotlib (visualisation)
* Streamlit (dashboard web)
* Traitement de données en mode chunk (Big Data)

---

## 📈 Fichiers générés

À chaque exécution :

* `vente.csv` → données brutes générées
* `resultats.csv` → résultats de l’analyse

---

## 🎯 Objectif du projet

Ce projet simule un **pipeline d’analyse de données réel**, utilisé dans :

* Analyse des ventes
* Business intelligence
* Tableaux de bord de performance
* Traitement de données volumineuses



## 🚀 Améliorations possibles

* Intégration d’une base de données (SQL)
* Prédiction des ventes avec Machine Learning
* Export Excel avec graphiques
* Déploiement du dashboard en ligne






## 🧠 Auteurs

### 👤 mhomed maymoun aouay
![mhomed maymoun aouay](470533734_122106714482680932_3683554923486708182_n.jpg)

  

---

### 👤 amine gdaiem 
![amine gdaiem ] <img width="1391" height="1413" alt="e5658a6a-98b8-4cc3-b1b3-ffca180c982c" src="https://github.com/user-attachments/assets/4ed62c38-c110-412a-a017-affc963bdacf" />


### 👤 fers drira
![fers drira] <img width="959" height="960" alt="8ca34b6d-95a4-4e32-aff4-777099cdebb4" src="https://github.com/user-attachments/assets/5dc58baf-ef96-46e3-804b-a0e58e62d5b4" />


 

---
