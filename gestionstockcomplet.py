import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
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
        messagebox.showerror(
            "Erreur", f"Erreur de connexion à la base de données : {err}")
        return None

# Ajouter une catégorie à la base de données


def ajouter_categorie():
    nom = entry_nom_categorie.get()
    if nom:
        try:
            cursor.execute("INSERT INTO categories (nom) VALUES (%s)", (nom,))
            conn.commit()
            afficher_categories()
            mettre_a_jour_combo_categories()
            entry_nom_categorie.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror(
                "Erreur", f"Impossible d'ajouter la catégorie : {err}")
    else:
        messagebox.showwarning(
            "Champ manquant", "Veuillez remplir le champ de la catégorie")

# Fonction pour mettre à jour le combobox des catégories


def mettre_a_jour_combo_categories():
    cursor.execute("SELECT id, nom FROM categories")
    categories = cursor.fetchall()
    combo_categories['values'] = [
        f"{cat[1]} (ID: {cat[0]})" for cat in categories]

# Afficher toutes les catégories dans le tableau


def afficher_categories():
    for item in tree_categories.get_children():
        tree_categories.delete(item)

    cursor.execute("SELECT * FROM categories")
    for row in cursor.fetchall():
        tree_categories.insert("", "end", values=row)

# Fonction pour afficher la gestion des produits
# Fonction pour afficher la gestion des produits


def afficher_gestion_produits():
    frame_categories.pack_forget()
    frame_produits.pack(pady=10)
    afficher_produits()  # Call this to display products when the frame is shown

# Ajouter un produit à la base de données


def ajouter_produit():
    nom = entry_nom.get()
    quantite = entry_quantite.get()
    prix = entry_prix.get()
    categorie_id = combo_categories.get()

    if nom and quantite and prix and categorie_id:
        try:
            # Validation des données
            quantite = int(quantite)
            prix = float(prix)
            cat_id = int(categorie_id.split(" (ID: ")[1][:-1])

            cursor.execute("INSERT INTO produits (nom, quantite, prix, categorie_id) VALUES (%s, %s, %s, %s)",
                           (nom, quantite, prix, cat_id))
            conn.commit()
            afficher_produits()
            clear_entries_produit()
        except ValueError:
            messagebox.showerror(
                "Erreur", "Quantité et prix doivent être des nombres.")
        except mysql.connector.Error as err:
            messagebox.showerror(
                "Erreur", f"Impossible d'ajouter le produit : {err}")
        except IndexError:
            messagebox.showerror("Erreur", "Sélection de catégorie invalide.")
    else:
        messagebox.showwarning(
            "Champ manquant", "Veuillez remplir tous les champs")

# Recherrcher les produits


def rechercher_produit():
    recherche = entry_recherche_produit.get()
    for item in tree_produits.get_children():
        tree_produits.delete(item)

    cursor.execute(
        "SELECT p.id, p.nom, p.quantite, p.prix, c.nom FROM produits p JOIN categories c ON p.categorie_id = c.id WHERE p.nom LIKE %s", (f'%{recherche}%',))
    for row in cursor.fetchall():
        tree_produits.insert("", "end", values=row)

# Afficher tous les produits dans le tableau


def afficher_produits():
    for item in tree_produits.get_children():
        tree_produits.delete(item)

    cursor.execute(
        "SELECT p.id, p.nom, p.quantite, p.prix, c.nom FROM produits p JOIN categories c ON p.categorie_id = c.id")
    for row in cursor.fetchall():
        tree_produits.insert("", "end", values=row)

# Fonction pour afficher la gestion des catégories


def afficher_gestion_categories():
    frame_produits.pack_forget()
    frame_categories.pack(pady=10)

# Fonction pour supprimer un produit


def supprimer_produit():
    selected_item = tree_produits.selection()
    if not selected_item:
        messagebox.showwarning("Sélection manquante",
                               "Veuillez sélectionner un produit à supprimer.")
        return

    produit_id = tree_produits.item(selected_item)["values"][0]
    try:
        cursor.execute("DELETE FROM produits WHERE id = %s", (produit_id,))
        conn.commit()
        afficher_produits()
    except mysql.connector.Error as err:
        messagebox.showerror(
            "Erreur", f"Impossible de supprimer le produit : {err}")

# Fonction pour modifier un produit


def modifier_produit():
    selected_item = tree_produits.selection()
    if not selected_item:
        messagebox.showwarning("Sélection manquante",
                               "Veuillez sélectionner un produit à modifier.")
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
            messagebox.showerror(
                "Erreur", f"Impossible de modifier le produit : {err}")
        except IndexError:
            messagebox.showerror("Erreur", "Sélection de catégorie invalide.")
    else:
        messagebox.showwarning(
            "Champ manquant", "Veuillez remplir tous les champs")

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

# Fonction pour supprimer une catégorie


def supprimer_categorie():
    selected_item = tree_categories.selection()
    if not selected_item:
        messagebox.showwarning(
            "Sélection manquante", "Veuillez sélectionner une catégorie à supprimer.")
        return

    categorie_id = tree_categories.item(selected_item)["values"][0]
    try:
        cursor.execute("DELETE FROM categories WHERE id = %s", (categorie_id,))
        conn.commit()
        afficher_categories()
        mettre_a_jour_combo_categories()
    except mysql.connector.Error as err:
        messagebox.showerror(
            "Erreur", f"Impossible de supprimer la catégorie : {err}")

# Fonction pour modifier une catégorie


def modifier_categorie():
    selected_item = tree_categories.selection()
    if not selected_item:
        messagebox.showwarning(
            "Sélection manquante", "Veuillez sélectionner une catégorie à modifier.")
        return

    categorie_id = tree_categories.item(selected_item)["values"][0]
    nouveau_nom = entry_nom_categorie.get()

    if nouveau_nom:
        try:
            cursor.execute(
                "UPDATE categories SET nom = %s WHERE id = %s", (nouveau_nom, categorie_id))
            conn.commit()
            afficher_categories()
            mettre_a_jour_combo_categories()
            entry_nom_categorie.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror(
                "Erreur", f"Impossible de modifier la catégorie : {err}")
    else:
        messagebox.showwarning(
            "Champ manquant", "Veuillez remplir le champ de la catégorie")


# Interface principale
root = ThemedTk()
root.title("Gestion de Stock")
root.geometry("1200x600")

# Appliquer un thème
root.set_theme("arc")

# Connexion à la base de données
conn = connexion_bd()
cursor = conn.cursor()

# Frame pour la gestion des catégories
frame_categories = tk.Frame(root, padx=10, pady=10)
frame_categories.pack(pady=10)

tk.Label(frame_categories, text="Nom de la catégorie").grid(row=0, column=0)
entry_nom_categorie = tk.Entry(frame_categories)
entry_nom_categorie.grid(row=0, column=1)

button_ajouter_categorie = tk.Button(
    frame_categories, text="Ajouter Catégorie", command=ajouter_categorie)
button_ajouter_categorie.grid(row=0, column=2)

# Tableau des catégories
tree_categories = ttk.Treeview(
    frame_categories, columns=("ID", "Nom"), show="headings")
tree_categories.heading("ID", text="ID")
tree_categories.heading("Nom", text="Nom")
tree_categories.grid(row=1, column=0, columnspan=3, pady=10)

# Afficher les catégories au démarrage
afficher_categories()

# Boutons pour modifier et supprimer des catégories
button_modifier_categorie = tk.Button(
    frame_categories, text="Modifier Catégorie", command=modifier_categorie)
button_modifier_categorie.grid(row=2, column=1)

button_supprimer_categorie = tk.Button(
    frame_categories, text="Supprimer Catégorie", command=supprimer_categorie)
button_supprimer_categorie.grid(row=2, column=2)

# Frame pour la gestion des produits
frame_produits = tk.Frame(root, padx=10, pady=10)

entry_recherche_produit = tk.Entry(frame_produits)
entry_recherche_produit.grid(row=7, column=0)
button_recherche = tk.Button(
    frame_produits, text="Rechercher", command=rechercher_produit)
button_recherche.grid(row=7, column=1)


# Ajouter une entrée pour la recherche dans l'interface


tk.Label(frame_produits, text="Nom du produit").grid(row=0, column=0)
entry_nom = tk.Entry(frame_produits)
entry_nom.grid(row=0, column=1)

tk.Label(frame_produits, text="Quantité").grid(row=1, column=0)
entry_quantite = tk.Entry(frame_produits)
entry_quantite.grid(row=1, column=1)

tk.Label(frame_produits, text="Prix").grid(row=2, column=0)
entry_prix = tk.Entry(frame_produits)
entry_prix.grid(row=2, column=1)

tk.Label(frame_produits, text="Catégorie").grid(row=3, column=0)
combo_categories = ttk.Combobox(frame_produits)
combo_categories.grid(row=3, column=1)

button_ajouter_produit = tk.Button(
    frame_produits, text="Ajouter Produit", command=ajouter_produit)
button_ajouter_produit.grid(row=4, column=1)
# Boutons pour modifier et supprimer des produits
button_modifier_produit = tk.Button(
    frame_produits, text="Modifier Produit", command=modifier_produit)
button_modifier_produit.grid(row=4, column=0)
button_supprimer_produit = tk.Button(
    frame_produits, text="Supprimer Produit", command=supprimer_produit)
button_supprimer_produit.grid(row=4, column=2)


# Tableau des produits
tree_produits = ttk.Treeview(frame_produits, columns=(
    "ID", "Nom", "Quantité", "Prix", "Catégorie"), show="headings")
tree_produits.heading("ID", text="ID")
tree_produits.heading("Nom", text="Nom")
tree_produits.heading("Quantité", text="Quantité")
tree_produits.heading("Prix", text="Prix")
tree_produits.heading("Catégorie", text="Catégorie")
tree_produits.grid(row=5, column=0, columnspan=2, pady=10)

# Événement de sélection pour remplir les champs de produit
tree_produits.bind("<<TreeviewSelect>>", remplir_champs)


# Menu
menu_bar = tk.Menu(root)
menu_gestion = tk.Menu(menu_bar, tearoff=0)
menu_gestion.add_command(label="Gérer Catégories",
                         command=afficher_gestion_categories)
menu_gestion.add_command(label="Gérer Produits",
                         command=afficher_gestion_produits)
menu_bar.add_cascade(label="Gestion", menu=menu_gestion)
root.config(menu=menu_bar)

# Afficher les catégories au démarrage
afficher_categories()
mettre_a_jour_combo_categories()

root.mainloop()

# Fermer la connexion à la base de données à la fermeture de l'application
conn.close()
