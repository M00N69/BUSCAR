import streamlit as st

st.title("Test de Déploiement Simple")

st.write("Si vous voyez ce message, l'application fonctionne correctement.")

# Essayez de charger et d'afficher une simple DataFrame
import pandas as pd

@st.cache_data
def load_data():
    file_path = "https://www.plateforme-sca.fr/media/11/download"
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.dataframe(df.head())
else:
    st.write("Impossible de charger les données.")

