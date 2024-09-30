import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk  # Importer ThemedTk
import mysql.connector

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
            mettre_a_jour_combo_categories()
            entry_nom_categorie.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Impossible d'ajouter la catégorie : {err}")
    else:
        messagebox.showwarning("Champ manquant", "Veuillez remplir le champ de la catégorie")

# Fonction pour mettre à jour le combobox des catégories
def mettre_a_jour_combo_categories():
    cursor.execute("SELECT id, nom FROM categories")
    categories = cursor.fetchall()
    combo_categories['values'] = [f"{cat[1]} (ID: {cat[0]})" for cat in categories]

# Ajouter un produit à la base de données
def ajouter_produit():
    nom = entry_nom.get()
    quantite = entry_quantite.get()
    prix = entry_prix.get()
    categorie_id = combo_categories.get()

    if nom and quantite and prix and categorie_id:
        try:
            cat_id = int(categorie_id.split(" (ID: ")[1][:-1])
            cursor.execute("INSERT INTO produits (nom, quantite, prix, categorie_id) VALUES (%s, %s, %s, %s)",
                           (nom, quantite, prix, cat_id))
            conn.commit()
            afficher_produits()
            clear_entries_produit()
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Impossible d'ajouter le produit : {err}")
        except IndexError:
            messagebox.showerror("Erreur", "Sélection de catégorie invalide.")
    else:
        messagebox.showwarning("Champ manquant", "Veuillez remplir tous les champs")

# Afficher tous les produits dans le tableau
def afficher_produits():
    for item in tree_produits.get_children():
        tree_produits.delete(item)

    cursor.execute(
        "SELECT p.id, p.nom, p.quantite, p.prix, c.nom FROM produits p JOIN categories c ON p.categorie_id = c.id")
    for row in cursor.fetchall():
        tree_produits.insert("", "end", values=row)

# Fonction pour supprimer un produit
def supprimer_produit():
    selected_item = tree_produits.selection()
    if not selected_item:
        messagebox.showwarning("Sélection manquante", "Veuillez sélectionner un produit à supprimer.")
        return

    produit_id = tree_produits.item(selected_item)["values"][0]
    try:
        cursor.execute("DELETE FROM produits WHERE id = %s", (produit_id,))
        conn.commit()
        afficher_produits()
    except mysql.connector.Error as err:
        messagebox.showerror("Erreur", f"Impossible de supprimer le produit : {err}")

# Fonction pour modifier un produit
def modifier_produit():
    selected_item = tree_produits.selection()
    if not selected_item:
        messagebox.showwarning("Sélection manquante", "Veuillez sélectionner un produit à modifier.")
        return

    produit_id = tree_produits.item(selected_item)["values"][0]
    nom = entry_nom.get()
    quantite = entry_quantite.get()
    prix = entry_prix.get()
    categorie_id = combo_categories.get()

    if nom and quantite and prix and categorie_id:
        try:
            cat_id = int(categorie_id.split(" (ID: ")[1][:-1])
            cursor.execute("UPDATE produits SET nom = %s, quantite = %s, prix = %s, categorie_id = %s WHERE id = %s",
                           (nom, quantite, prix, cat_id, produit_id))
            conn.commit()
            afficher_produits()
            clear_entries_produit()
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Impossible de modifier le produit : {err}")
        except IndexError:
            messagebox.showerror("Erreur", "Sélection de catégorie invalide.")
    else:
        messagebox.showwarning("Champ manquant", "Veuillez remplir tous les champs")

# Remplir les champs de saisie avec les données du produit sélectionné
def remplir_champs(event):
    selected_item = tree_produits.selection()
    if selected_item:
        produit = tree_produits.item(selected_item)["values"]
        entry_nom.delete(0, tk.END)
        entry_nom.insert(0, produit[1])
        entry_quantite.delete(0, tk.END)
        entry_quantite.insert(0, produit[2])
        entry_prix.delete(0, tk.END)
        entry_prix.insert(0, produit[3])
        combo_categories.set(produit[4])

# Effacer les champs de saisie des produits
def clear_entries_produit():
    entry_nom.delete(0, tk.END)
    entry_quantite.delete(0, tk.END)
    entry_prix.delete(0, tk.END)
    combo_categories.set("")

# Interface principale
root = ThemedTk()  # Utiliser ThemedTk pour le thème
root.title("Gestion de Stock")
root.geometry("800x600")

# Appliquer un thème
root.set_theme("arc")  # Remplace "arc" par le thème de ton choix

# Connexion à la base de données
conn = connexion_bd()
cursor = conn.cursor()

# Section pour ajouter un produit
frame_produit = tk.Frame(root, padx=10, pady=10)
frame_produit.pack(pady=10)

tk.Label(frame_produit, text="Nom du produit").grid(row=0, column=0)
entry_nom = tk.Entry(frame_produit)
entry_nom.grid(row=0, column=1)

tk.Label(frame_produit, text="Quantité").grid(row=1, column=0)
entry_quantite = tk.Entry(frame_produit)
entry_quantite.grid(row=1, column=1)

tk.Label(frame_produit, text="Prix").grid(row=2, column=0)
entry_prix = tk.Entry(frame_produit)
entry_prix.grid(row=2, column=1)

tk.Label(frame_produit, text="Catégorie").grid(row=3, column=0)
combo_categories = ttk.Combobox(frame_produit)
combo_categories.grid(row=3, column=1)

# Remplir le combobox avec les catégories
mettre_a_jour_combo_categories()

button_ajouter_produit = tk.Button(frame_produit, text="Ajouter Produit", command=ajouter_produit)
button_ajouter_produit.grid(row=4, column=0)

button_modifier_produit = tk.Button(frame_produit, text="Modifier Produit", command=modifier_produit)
button_modifier_produit.grid(row=4, column=1)

button_supprimer_produit = tk.Button(frame_produit, text="Supprimer Produit", command=supprimer_produit)
button_supprimer_produit.grid(row=4, column=2)

# Tableau des produits
tree_produits = ttk.Treeview(root, columns=("ID", "Nom", "Quantité", "Prix", "Catégorie"), show="headings")
tree_produits.heading("ID", text="ID")
tree_produits.heading("Nom", text="Nom")
tree_produits.heading("Quantité", text="Quantité")
tree_produits.heading("Prix", text="Prix")
tree_produits.heading("Catégorie", text="Catégorie")
tree_produits.pack(pady=10)

# Événements de sélection
tree_produits.bind("<<TreeviewSelect>>", remplir_champs)

# Afficher les produits au démarrage
afficher_produits()

# Boucle principale
root.mainloop()

# Fermer la connexion à la base de données à la fermeture de l'application
if conn:
    conn.close()
