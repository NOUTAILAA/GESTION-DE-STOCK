# Gestion de Stock

Gestion de Stock est une application desktop développée en Python avec Tkinter et MySQL. Elle permet de gérer les produits et les catégories d'un stock, y compris l'ajout, la modification, la suppression et la recherche de produits et de catégories.

## Fonctionnalités

- Gestion des catégories de produits
  - Ajouter, modifier et supprimer des catégories
- Gestion des produits
  - Ajouter, modifier et supprimer des produits
  - Rechercher des produits par nom
- Interface utilisateur intuitive basée sur Tkinter
- Connexion à une base de données MySQL pour stocker les données

## Prérequis

- Python 3.x
- MySQL Server
- Bibliothèques Python nécessaires :
  - Tkinter
  - mysql-connector-python
  - ttkthemes

## Installation

1. **Clonez le dépôt :**
   git clone https://github.com/NOUTAILAA/GESTION-DE-STOCK.git
  
2. **Installez les bibliothèques nécessaires :**
pip install mysql-connector-python ttkthemes

3. **Configurez la base de données :**
Créez une base de données MySQL nommée gestion_stock.
Créez les tables nécessaires :
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL
);

CREATE TABLE produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    quantite INT NOT NULL,
    prix DECIMAL(10, 2) NOT NULL,
    categorie_id INT,
    FOREIGN KEY (categorie_id) REFERENCES categories(id)
);
4. **Configurez la base de données :**
python gestionstockcomplet.py
