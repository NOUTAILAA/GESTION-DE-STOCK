import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import mysql.connector
import subprocess
import sys

# Connexion à la base de données MySQL
def connexion_bd():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="gestion_stock"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Erreur", f"Erreur de connexion à la base de données : {err}")
        return None

# Ajouter une catégorie à la base de données
def ajouter_categorie():
    nom = entry_nom_categorie.get()
    if nom:
        try:
            cursor.execute("INSERT INTO categories (nom) VALUES (%s)", (nom,))
            conn.commit()
            afficher_categories()
            entry_nom_categorie.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Impossible d'ajouter la catégorie : {err}")
    else:
        messagebox.showwarning("Champ manquant", "Veuillez remplir le champ de la catégorie")

# Afficher toutes les catégories dans le tableau
def afficher_categories():
    for item in tree_categories.get_children():
        tree_categories.delete(item)

    cursor.execute("SELECT * FROM categories")
    for row in cursor.fetchall():
        tree_categories.insert("", "end", values=row)

# Fonction pour passer à la page de gestion des produits
def aller_a_gestion_produits():
    # Ferme la fenêtre actuelle
    root.destroy()
    # Exécute gestion_produits.py
    subprocess.Popen([sys.executable, "gestion_produits.py"])

# Interface principale
root = ThemedTk()
root.title("Gestion des Catégories")
root.geometry("400x300")

# Connexion à la base de données
conn = connexion_bd()
cursor = conn.cursor()

# Section pour ajouter une catégorie
frame_categorie = tk.Frame(root, padx=10, pady=10)
frame_categorie.pack(pady=10)

tk.Label(frame_categorie, text="Nom de la catégorie").grid(row=0, column=0)
entry_nom_categorie = tk.Entry(frame_categorie)
entry_nom_categorie.grid(row=0, column=1)

button_ajouter_categorie = tk.Button(frame_categorie, text="Ajouter Catégorie", command=ajouter_categorie)
button_ajouter_categorie.grid(row=0, column=2)

# Bouton pour passer à la gestion des produits
button_gestion_produits = tk.Button(root, text="Gestion des Produits", command=aller_a_gestion_produits)
button_gestion_produits.pack(pady=10)

# Tableau des catégories
tree_categories = ttk.Treeview(root, columns=("ID", "Nom"), show="headings")
tree_categories.heading("ID", text="ID")
tree_categories.heading("Nom", text="Nom")
tree_categories.pack(pady=10)

# Afficher les catégories au démarrage
afficher_categories()

# Boucle principale
root.mainloop()

# Fermer la connexion à la base de données lors de la fermeture de l'application
conn.close()
