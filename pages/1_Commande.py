import streamlit as st
from database import get_produits, ajouter_commande

st.title("📱 Commandez depuis votre téléphone")
st.write("Scannez, choisissez, et validez !")

produits = get_produits()

for produit in produits:
    id_prod, nom, prix, categorie = produit
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.write(f"**{nom}** ({categorie})")
    with col2:
        st.write(f"{prix:.2f} DT")
    with col3:
        if st.button(f"Ajouter", key=f"btn_{id_prod}"):
            ajouter_commande(id_prod, 1, prix)
            st.success(f"{nom} ajouté !")

st.divider()
st.info("💡 Astuce : Dans une version réelle, vous auriez un panier qui se remplit ici.")