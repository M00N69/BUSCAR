import streamlit as st
import pandas as pd
import plotly.express as px

# Titre de l'application
st.title("Statistiques des Risques de Veille Sanitaire")

# Charger le fichier Excel
file_path = "https://www.plateforme-sca.fr/media/11/download"
df = pd.read_excel(file_path, engine='openpyxl')

# Afficher une brève description des données
st.subheader("Aperçu des données")
st.dataframe(df.head())

# Interface de recherche par mots-clés
st.subheader("Recherche par mots-clés")
search_term = st.text_input("Entrez un mot-clé pour rechercher dans les données:")

# Filtrer le DataFrame en fonction du terme recherché
if search_term:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    st.write(f"Résultats pour la recherche : {search_term}")
else:
    filtered_df = df

# Afficher les résultats filtrés
st.dataframe(filtered_df)

# Exemple de visualisation
st.subheader("Visualisation des données")
if not filtered_df.empty:
    fig = px.bar(filtered_df, x='Nom_de_la_colonne_X', y='Nom_de_la_colonne_Y', title="Exemple de Graphique")
    st.plotly_chart(fig)
else:
    st.write("Aucun résultat trouvé. Essayez un autre mot-clé.")
