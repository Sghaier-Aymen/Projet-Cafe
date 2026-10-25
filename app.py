import streamlit as st

st.set_page_config(page_title="Café Data", page_icon="☕", layout="wide")

page_client = st.Page("pages/1_Commande.py", title="Menu Client", icon="📱")
page_dashboard = st.Page("pages/2_Dashboard.py", title="Dashboard Gérant", icon="📊")

pg = st.navigation([page_client, page_dashboard])

st.sidebar.title("☕ Mon Café Tunisien")

pg.run()
import streamlit as st

st.set_page_config(page_title="Café Data", page_icon="☕", layout="wide")

page_client = st.Page("pages/1_Commande.py", title="Menu Client", icon="📱")
page_dashboard = st.Page("pages/2_Dashboard.py", title="Dashboard Gérant", icon="📊")
# NOUVELLE LIGNE ICI
page_ml = st.Page("pages/3_Machine_Learning.py", title="Machine Learning", icon="🧠")

pg = st.navigation([page_client, page_dashboard, page_ml])

st.sidebar.title("☕ Mon Café Tunisien")

pg.run()