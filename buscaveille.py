import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import plotly.express as px
import re

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
    .dataframe td {
        white-space: normal !important;
        word-wrap: break-word !important;
    }
    </style>
    <div class="banner"></div>
    """,
    unsafe_allow_html=True
)

# Titre principal
st.title("Statistiques des Risques de Veille Sanitaire : Bulletins BuSCA")

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
    # Supprimer les colonnes "Section" et "Type" pour gagner de l'espace
    columns_to_drop = ["Section", "Type"]
    df = df.drop(columns=columns_to_drop, errors='ignore')

    # Initialiser les variables pour éviter les erreurs NameError
    countries, matrices = [], []
    busca_range = None
    keywords = ""

    # Menu latéral pour les filtres
    with st.sidebar:
        st.header("Filtres")

        # Filtrage par numéro de BuSCA
        busca_col = 'BuSCA'  # Nom exact de la colonne
        if busca_col in df.columns:
            busca_min = int(df[busca_col].min())
            busca_max = int(df[busca_col].max())
            busca_range = st.slider(
                "Sélectionner une plage de numéros de BuSCA",
                min_value=busca_min,
                max_value=busca_max,
                value=(busca_min, busca_max)
            )

        # Filtrage par pays
        country_col = 'Pays'  # Remplacez par le nom de la colonne des pays
        if country_col in df.columns:
            countries = st.multiselect(
                "Sélectionner les pays",
                options=df[country_col].unique()
            )

        # Filtrage par matrice
        matrice_col = 'Matrice (catégories)'
        if matrice_col in df.columns:
            matrices = st.multiselect("Sélectionner les matrices", options=df[matrice_col].unique())

        # Recherche par mots-clés
        keywords = st.text_area("Recherche par mots-clés (séparés par des virgules)")

        # Bouton pour appliquer les filtres
        apply_filter = st.button("Appliquer les filtres")

    if apply_filter:
        # Appliquer les filtres de numéro de BuSCA
        if busca_range and busca_col in df.columns:
            df = df[(df[busca_col] >= busca_range[0]) & (df[busca_col] <= busca_range[1])]

        # Appliquer les filtres de pays
        if countries:
            df = df[df[country_col].isin(countries)]

        # Appliquer les filtres de matrice
        if matrices:
            df = df[df[matrice_col].isin(matrices)]

        # Appliquer le filtre par mots-clés sur des colonnes spécifiques
        if keywords:
            keyword_list = [kw.strip().lower() for kw in keywords.split(',')]
            keyword_patterns = [r'\b' + re.escape(kw) + r's?\b' for kw in keyword_list]  # Ajouter \b pour les bordures de mots et gérer le pluriel

            def match_keywords(text, patterns):
                return any(re.search(pattern, text) for pattern in patterns)

            cols_to_search = ['Titre', 'Texte', 'Danger', 'Matrice (catégories)']  # Limiter à certaines colonnes
            df = df[df[cols_to_search].apply(lambda row: row.astype(str).str.lower().apply(lambda x: match_keywords(x, keyword_patterns)).any(), axis=1)]

        # Remplacer les NaN par des chaînes vides pour un affichage plus propre
        df.fillna('', inplace=True)

        # Graphiques en camembert côte à côte
        st.subheader("Répartition des Dangers et Matrices")
        col1, col2 = st.columns(2)

        with col1:
            if 'Danger' in df.columns:
                danger_counts = df['Danger'].value_counts().nlargest(10)  # Les 10 principales occurrences
                fig1 = px.pie(danger_counts, names=danger_counts.index, values=danger_counts.values, title="Top 10 des Dangers")
                fig1.update_layout(margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig1, use_container_width=True)

        with col2:
            if matrice_col in df.columns:
                matrice_counts = df[matrice_col].value_counts().nlargest(10)  # Les 10 principales occurrences
                fig2 = px.pie(matrice_counts, names=matrice_counts.index, values=matrice_counts.values, title="Top 10 des Matrices")
                fig2.update_layout(margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig2, use_container_width=True)

        # Rendre les liens cliquables
        def make_clickable(val, text):
            if pd.notna(val) and val != '':
                return f'<a target="_blank" href="{val}">{text}</a>'
            return ''

        df['Lien'] = df['Lien'].apply(lambda x: make_clickable(x, 'Lien1'))
        df['Lien2'] = df['Lien2'].apply(lambda x: make_clickable(x, 'Lien2'))

        # Affichage du DataFrame avec possibilité de tri et filtrage
        st.dataframe(df)

        # Affichage du tableau formaté avec liens
        st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
