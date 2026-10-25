import streamlit as st
import pandas as pd
import sqlite3
import random
from datetime import datetime, timedelta

st.title("📊 Tableau de Bord - Gérant")

# --- FONCTION POUR GÉNÉRER DES DONNÉES FACTICES ---
def generer_donnees_factices():
    conn = sqlite3.connect("menu.db")
    c = conn.cursor()
    
    # On récupère les produits existants
    c.execute("SELECT id, prix FROM produits")
    produits = c.fetchall()
    
    if not produits:
        st.error("Aucun produit dans la base de données.")
        return

    # On génère 300 commandes aléatoires sur les 30 derniers jours
    for _ in range(300):
        # Choisir un produit au hasard
        prod_id, prix = random.choice(produits)
        quantite = random.randint(1, 3)
        total = prix * quantite
        
        # Générer une date aléatoire dans les 30 derniers jours
        jours_aleatoires = random.randint(0, 30)
        date_commande = datetime.now() - timedelta(days=jours_aleatoires)
        
        # Simuler des heures de pointe (12h-14h et 16h-18h)
        if random.random() < 0.6: # 60% de chance d'être à une heure de pointe
            heure = random.choice([12, 13, 16, 17])
            date_commande = date_commande.replace(hour=heure, minute=random.randint(0, 59))
        else:
            date_commande = date_commande.replace(hour=random.randint(8, 20), minute=random.randint(0, 59))
            
        date_str = date_commande.strftime("%Y-%m-%d %H:%M:%S")
        
        c.execute("INSERT INTO commandes (produit_id, quantite, total, date_heure) VALUES (?, ?, ?, ?)", 
                  (prod_id, quantite, total, date_str))
        
    conn.commit()
    conn.close()
    st.success("300 commandes générées avec succès !")
    st.rerun() # Recharge la page pour afficher les nouvelles données

# --- BOUTON DE GÉNÉRATION (Affiché uniquement si la base est vide ou pour tester) ---
with st.sidebar:
    st.write("---")
    st.write("🛠️ **Mode Démo**")
    if st.button("Générer 300 commandes de test"):
        generer_donnees_factices()

# --- CONNEXION ET LECTURE DE LA BASE ---
conn = sqlite3.connect("menu.db")
query = """
SELECT c.id, p.nom, p.categorie, c.quantite, c.total, c.date_heure
FROM commandes c
JOIN produits p ON c.produit_id = p.id
ORDER BY c.date_heure DESC
"""
df = pd.read_sql_query(query, conn)
conn.close()

if df.empty:
    st.warning("Aucune commande pour le moment. Cliquez sur le bouton 'Générer 300 commandes de test' dans le menu à gauche pour remplir le tableau de bord !")
else:
    # Convertir la colonne date en format datetime pour l'analyse
    df['date_heure'] = pd.to_datetime(df['date_heure'])
    
    # --- LIGNE 1 : LES KPIs PRINCIPAUX ---
    col1, col2, col3 = st.columns(3)
    
    ca_total = df['total'].sum()
    col1.metric("Chiffre d'Affaires Total", f"{ca_total:.2f} DT")
    
    nb_commandes = len(df)
    col2.metric("Nombre de Commandes", nb_commandes)
    
    panier_moyen = ca_total / nb_commandes if nb_commandes > 0 else 0
    col3.metric("Panier Moyen", f"{panier_moyen:.2f} DT")
    
    st.divider()

    # --- LIGNE 2 : ANALYSE DES PRODUITS ---
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        st.subheader("🏆 Top 5 Produits (par Quantité)")
        top_produits_qte = df.groupby('nom')['quantite'].sum().sort_values(ascending=False).head(5)
        st.bar_chart(top_produits_qte, color="#FF4B4B")
        
    with col_graph2:
        st.subheader("💰 Top 5 Produits (par Chiffre d'Affaires)")
        top_produits_ca = df.groupby('nom')['total'].sum().sort_values(ascending=False).head(5)
        st.bar_chart(top_produits_ca, color="#00C853")

    st.divider()

    # --- LIGNE 3 : ANALYSE TEMPORELLE ---
    st.subheader("🕒 Analyse des Heures de Pointe")
    # Extraire l'heure de la date
    df['heure'] = df['date_heure'].dt.hour
    # Compter le nombre de commandes par heure et trier par heure
    commandes_par_heure = df['heure'].value_counts().sort_index()
    st.bar_chart(commandes_par_heure, color="#2962FF")
    st.caption("Ce graphique montre à quelles heures de la journée les clients commandent le plus.")

    st.divider()

    # --- HISTORIQUE ---
    st.subheader("📋 Historique récent (10 dernières commandes)")
    # On affiche seulement les colonnes utiles
    df_affichage = df[['date_heure', 'nom', 'quantite', 'total']].head(10).copy()
    df_affichage['date_heure'] = df_affichage['date_heure'].dt.strftime('%d/%m/%Y %H:%M')
    st.dataframe(df_affichage, use_container_width=True)