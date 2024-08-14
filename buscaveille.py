import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import plotly.express as px

# Titre de l'application
st.title("Statistiques des Risques de Veille Sanitaire")

# Fonction pour charger les données depuis l'URL
@st.cache_data
def load_data():
    file_url = "https://www.plateforme-sca.fr/media/11/download"
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        df = pd.read_excel(BytesIO(response.content), engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return pd.DataFrame()

# Charger les données
df = load_data()

if df.empty:
    st.write("Impossible de charger les données.")
else:
    # Afficher un aperçu des données
    st.subheader("Aperçu des données")
    st.dataframe(df.head())

    # Interface de recherche par mots-clés
    st.subheader("Recherche par mots-clés")
    search_term = st.text_input("Entrez un mot-clé pour rechercher dans les données :")

    # Filtrer le DataFrame en fonction du terme recherché
    if search_term:
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
        st.write(f"Résultats pour la recherche : {search_term}")
    else:
        filtered_df = df

    # Afficher les résultats filtrés
    st.dataframe(filtered_df)

    # Exemple de visualisation avec Plotly si les colonnes spécifiques existent
    st.subheader("Visualisation des données")
    if not filtered_df.empty:
        # Ici, vous devez spécifier les colonnes que vous souhaitez visualiser
        if 'Danger' in filtered_df.columns and 'Matrice (catégories)' in filtered_df.columns:
            fig = px.bar(filtered_df, x='Matrice (catégories)', y='Danger', title="Danger par Matrice (catégories)")
            st.plotly_chart(fig)
        else:
            st.write("Les colonnes spécifiées pour le graphique ne sont pas présentes dans les données.")
    else:
        st.write("Aucun résultat trouvé. Essayez un autre mot-clé.")
