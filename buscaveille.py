import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import plotly.express as px

# Configurer le mode wide
st.set_page_config(layout="wide")

# Bannière avec le logo
st.markdown(
    """
    <style>
    .banner {
        background-image: url('https://github.com/M00N69/BUSCAR/blob/main/logo%2002%20copie.jpg?raw=true');
        background-size: cover;
        padding: 50px;
        text-align: center;
    }
    </style>
    <div class="banner"></div>
    """,
    unsafe_allow_html=True
)

# Titre principal
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
    # Menu latéral pour les filtres
    st.sidebar.header("Filtres")

    # Filtrage par plage de dates
    date_col = 'Date'  # Remplacez par le nom de la colonne des dates
    if date_col in df.columns:
        min_date = df[date_col].min()
        max_date = df[date_col].max()
        start_date, end_date = st.sidebar.date_input("Sélectionner une plage de dates", [min_date, max_date])

        df = df[(df[date_col] >= start_date) & (df[date_col] <= end_date)]

    # Filtrage par pays
    country_col = 'Pays'  # Remplacez par le nom de la colonne des pays
    if country_col in df.columns:
        countries = st.sidebar.multiselect(
            "Sélectionner les pays",
            options=df[country_col].unique(),
            default=df[country_col].unique()
        )
        df = df[df[country_col].isin(countries)]

    # Filtrage par section, type, matrice
    section_col = 'Section'
    type_col = 'Type'
    matrice_col = 'Matrice (catégories)'

    if section_col in df.columns:
        sections = st.sidebar.multiselect("Sélectionner les sections", options=df[section_col].unique())
        if sections:
            df = df[df[section_col].isin(sections)]

    if type_col in df.columns:
        types = st.sidebar.multiselect("Sélectionner les types", options=df[type_col].unique())
        if types:
            df = df[df[type_col].isin(types)]

    if matrice_col in df.columns:
        matrices = st.sidebar.multiselect("Sélectionner les matrices", options=df[matrice_col].unique())
        if matrices:
            df = df[df[matrice_col].isin(matrices)]

    # Recherche par mots-clés
    keywords = st.sidebar.text_area("Recherche par mots-clés (séparés par des virgules)")
    if keywords:
        keyword_list = [kw.strip() for kw in keywords.split(',')]
        df = df[df.apply(lambda row: any(kw.lower() in row.astype(str).str.lower().values for kw in keyword_list), axis=1)]

    # Graphiques en camembert
    st.subheader("Répartition des Dangers")
    if 'Danger' in df.columns:
        danger_counts = df['Danger'].value_counts()
        fig1 = px.pie(danger_counts, names=danger_counts.index, values=danger_counts.values, title="Répartition des Dangers")
        st.plotly_chart(fig1)

    st.subheader("Répartition des Matrices")
    if matrice_col in df.columns:
        matrice_counts = df[matrice_col].value_counts()
        fig2 = px.pie(matrice_counts, names=matrice_counts.index, values=matrice_counts.values, title="Répartition des Matrices")
        st.plotly_chart(fig2)

    # Affichage du DataFrame avec liens cliquables
    st.subheader("Données Filtrées")
    df_display = df.copy()

    # Rendre les liens cliquables
    def make_clickable(val):
        if pd.notna(val):
            return f'<a target="_blank" href="{val}">{val}</a>'
        return val

    df_display['Lien'] = df_display['Lien'].apply(make_clickable)
    df_display['Lien2'] = df_display['Lien2'].apply(make_clickable)

    st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)

