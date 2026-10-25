import sqlite3

DB_NAME = "menu.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS produits
                 (id INTEGER PRIMARY KEY, nom TEXT, prix REAL, categorie TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS commandes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  produit_id INTEGER, 
                  quantite INTEGER, 
                  total REAL, 
                  date_heure TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute("SELECT COUNT(*) FROM produits")
    if c.fetchone()[0] == 0:
        produits_test = [
            ("Café Express", 1.5, "Boisson"),
            ("Cappuccino", 3.0, "Boisson"),
            ("Thé à la Menthe", 2.0, "Boisson"),
            ("Jus d'Orange", 4.0, "Boisson"),
            ("Croissant", 2.5, "Pâtisserie"),
            ("Sandwich Thon", 5.5, "Sandwich"),
            ("Eau Minérale", 1.0, "Boisson")
        ]
        c.executemany("INSERT INTO produits (nom, prix, categorie) VALUES (?, ?, ?)", produits_test)
    
    conn.commit()
    conn.close()

def get_produits():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM produits")
    produits = c.fetchall()
    conn.close()
    return produits

def ajouter_commande(produit_id, quantite, total):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO commandes (produit_id, quantite, total) VALUES (?, ?, ?)", 
              (produit_id, quantite, total))
    conn.commit()
    conn.close()

init_db()