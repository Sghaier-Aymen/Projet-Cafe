import streamlit as st
import pandas as pd
import sqlite3
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

st.title("🧠 Analyse des Associations (Machine Learning)")
st.write("Cet algorithme (Apriori) analyse les commandes passées pour trouver quels produits sont souvent achetés ensemble.")

# --- CHARGEMENT DES DONNÉES ---
conn = sqlite3.connect("menu.db")
query = """
SELECT c.id as commande_id, p.nom
FROM commandes c
JOIN produits p ON c.produit_id = p.id
"""
df = pd.read_sql_query(query, conn)
conn.close()

if df.empty:
    st.warning("Aucune donnée. Allez sur le Dashboard Gérant et générez des commandes de test.")
else:
    # 1. Regrouper les produits par commande (transaction)
    # (Dans notre simulation, 1 clic = 1 commande d'un seul produit. 
    # Pour que l'algorithme fonctionne, on va simuler des "paniers" en groupant les commandes par minute)
    
    # On crée des "paniers" artificiels pour la démo
    df['panier_id'] = df.index // 3  # Groupe les commandes par 3 pour simuler un panier moyen
    
    transactions = df.groupby('panier_id')['nom'].apply(list).tolist()

    # 2. Transformer les données pour l'algorithme (One-Hot Encoding)
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

    # 3. Appliquer l'algorithme Apriori
    # min_support = 0.05 signifie qu'on cherche des associations présentes dans au moins 5% des paniers
    frequent_itemsets = apriori(df_encoded, min_support=0.05, use_colnames=True)
    
    if frequent_itemsets.empty:
        st.info("Pas assez de données pour trouver des associations fréquentes. Générez plus de commandes !")
    else:
        # 4. Générer les règles d'association
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.3)
        
        # Trier par confiance décroissante
        rules = rules.sort_values(by='confidence', ascending=False)

        st.subheader("🔍 Résultats de l'analyse")
        st.write("Voici les combinaisons de produits qui apparaissent souvent ensemble :")

        # Afficher les résultats de manière lisible
        for index, row in rules.head(5).iterrows():
            antecedents = ", ".join(list(row['antecedents']))
            consequents = ", ".join(list(row['consequents']))
            confidence = row['confidence'] * 100
            
            st.success(f"💡 **Si un client achète : {antecedents}**")
            st.write(f"👉 **Il a {confidence:.1f}% de chances d'acheter aussi : {consequents}**")
            st.write("---")

        st.subheader("📊 Tableau des règles")
        st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']], use_container_width=True)
        
        st.info("""
        **Comment lire ces résultats pour le gérant ?**
        *   **Support** : La fréquence de la combinaison dans toutes les ventes.
        *   **Confiance** : La probabilité d'acheter le produit B sachant qu'on a acheté le produit A.
        *   **Lift** : Si > 1, cela signifie que l'association est plus forte que le hasard.
        """)