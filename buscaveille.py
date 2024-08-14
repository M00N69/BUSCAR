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
st.title(" Veille Sanitaire Bulletin BUSCA , liste des bulletins")

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
    # Initialiser les variables pour éviter les erreurs NameError
    countries, sections, types, matrices = [], [], [], []
    start_date, end_date = None, None

    # Menu latéral pour les filtres
    with st.sidebar:
        st.header("Filtres(utiliser la flèche en haut pour fermer ce volet)")

        # Filtrage par plage de dates
        date_col = 'Date'  # Remplacez par le nom de la colonne des dates
        if date_col in df.columns:
            min_date = df[date_col].min()
            max_date = df[date_col].max()
            start_date, end_date = st.date_input("Sélectionner une plage de dates", [min_date, max_date])

        # Filtrage par pays
        country_col = 'Pays'  # Remplacez par le nom de la colonne des pays
        if country_col in df.columns:
            countries = st.multiselect(
                "Sélectionner les pays",
                options=df[country_col].unique()
            )

        # Filtrage par section, type, matrice
        section_col = 'Section'
        type_col = 'Type'
        matrice_col = 'Matrice (catégories)'

        if section_col in df.columns:
            sections = st.multiselect("Sélectionner les sections", options=df[section_col].unique())

        if type_col in df.columns:
            types = st.multiselect("Sélectionner les types", options=df[type_col].unique())

        if matrice_col in df.columns:
            matrices = st.multiselect("Sélectionner les matrices", options=df[matrice_col].unique())

        # Amélioration de la recherche par mots-clés
        keywords = st.text_area("Recherche par mots-clés (séparés par des virgules)")

        # Bouton pour appliquer les filtres
        apply_filter = st.button("Appliquer les filtres")

    if apply_filter:
        # Appliquer les filtres de dates
        if start_date and end_date and date_col in df.columns:
            df = df[(df[date_col] >= pd.to_datetime(start_date)) & (df[date_col] <= pd.to_datetime(end_date))]

        # Appliquer les filtres de pays
        if countries:
            df = df[df[country_col].isin(countries)]

        # Appliquer les filtres de section, type, matrice
        if sections:
            df = df[df[section_col].isin(sections)]

        if types:
            df = df[df[type_col].isin(types)]

        if matrices:
            df = df[df[matrice_col].isin(matrices)]

        # Appliquer le filtre par mots-clés sur des colonnes spécifiques
        if keywords:
            keyword_list = [kw.strip().lower() for kw in keywords.split(',')]
            cols_to_search = ['Titre', 'Texte', 'Danger', 'Matrice (catégories)']  # Limiter à certaines colonnes
            df = df[df[cols_to_search].apply(lambda row: row.astype(str).str.lower().apply(lambda x: any(kw in x for kw in keyword_list)).any(), axis=1)]

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

        # Affichage du DataFrame avec liens cliquables et ajustement des cellules
        st.subheader("Données Filtrées")
        df_display = df.copy()

        # Rendre les liens cliquables
        def make_clickable(val, text):
            if pd.notna(val):
                return f'<a target="_blank" href="{val}">{text}</a>'
            return val

        df_display['Lien'] = df_display['Lien'].apply(lambda x: make_clickable(x, 'Lien1'))
        df_display['Lien2'] = df_display['Lien2'].apply(lambda x: make_clickable(x, 'Lien2'))

        # Affichage du tableau avec ajustement des tailles
        st.write(df_display.to_html(escape=False, index=False), unsafe_allow_html=True)

