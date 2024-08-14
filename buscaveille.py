import streamlit as st
import pandas as pd
import requests
from io import BytesIO

@st.cache_data
def load_data():
    file_url = "https://www.plateforme-sca.fr/media/11/download"
    try:
        # Télécharger le fichier
        response = requests.get(file_url)
        response.raise_for_status()  # Vérifie que la requête a réussi

        # Charger le fichier Excel depuis le contenu téléchargé
        df = pd.read_excel(BytesIO(response.content), engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.dataframe(df.head())
else:
    st.write("Impossible de charger les données.")
