import streamlit as st

st.set_page_config(page_title="Café Data", page_icon="☕", layout="wide")

page_client = st.Page("pages/1_Commande.py", title="Menu Client", icon="📱")
page_dashboard = st.Page("pages/2_Dashboard.py", title="Dashboard Gérant", icon="📊")

pg = st.navigation([page_client, page_dashboard])

st.sidebar.title("☕ Mon Café Tunisien")

pg.run()