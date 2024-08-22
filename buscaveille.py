import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import plotly.express as px
import re

# Configurer le mode wide
st.set_page_config(layout="wide")

# Custom CSS for changing sidebar background color and resizing the banner
st.markdown(
    """
    <style>
    /* Sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #1A1D23; /* Light blue color */
    }

    /* Sidebar header text color (optional) */
    [data-testid="stSidebar"] .css-1lcbmhc {
        color: black;
    }
    
    /* Sidebar widget text color (optional) */
    [data-testid="stSidebar"] .css-17eq0hr {
        color: black;
    }

    /* Banner styling */
    .banner {
        background-image: url('https://github.com/M00N69/BUSCAR/blob/main/logo%2002%20copie.jpg?raw=true');
        background-size: cover;
        padding: 75px;
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
st.title(" Veille Sanitaire SCA, Surveillance de la Chaine Alimentaire: BuSCA")

# Dropdown section to explain the application
with st.expander("À propos de cette application"):
    st.write("""
    ### Fonctionnement de l'Application

    Cette application est conçue pour vous aider à explorer et analyser les données sur les risques sanitaires provenant des bulletins BuSCA.
    Vous disposez d'une interface simple pour filtrer et visualiser ces données de manière interactive.

    #### Source des Données
    L'application va chercher automatiquement la dernière version de la base de données BuSCA à chaque utilisation.
    Les données proviennent directement de la plateforme BuSCA, accessible via le lien suivant : [Le Dernier BuSCA](https://www.plateforme-sca.fr/le-dernier-busca).
    Cela garantit que vous travaillez toujours avec les informations les plus récentes disponibles.

    #### Fonctionnalités de Filtrage
    Vous pouvez filtrer les données selon plusieurs critères :
    
    - **Plage de numéros de BuSCA :** Filtrez les bulletins par leur numéro pour restreindre les résultats à une plage spécifique.
    - **Matrices :** Filtrez par catégories de matrices, permettant d'affiner l'analyse sur des types spécifiques de données.
    - **Danger :** Filtrez les résultats selon les types de dangers identifiés dans les bulletins.
    - **Section :** Sélectionnez les sections spécifiques pour filtrer les données selon les catégories définies par BuSCA.
    - **Mots-clés :** Recherchez des termes spécifiques à travers plusieurs colonnes clés. Cela vous permet de cibler des informations précises dans le texte des bulletins.

    **Pourquoi les filtres peuvent sembler complexes :** Les filtres sont conçus en fonction de la structure et de la gestion interne de la base de données BuSCA. Certaines catégories sont larges, ce qui reflète la richesse et la complexité des données traitées. Cela permet une grande flexibilité dans l'analyse, même si cela peut paraître complexe au premier abord.

    **Astuce d'Utilisation :** Une fois que vous avez choisi vos filtres et cliqué sur le bouton "Appliquer les filtres", il est préférable de refermer la fenêtre latérale pour profiter d'une meilleure visibilité des résultats.

    #### Visualisation des Données

    - **Tableau des Données (DataFrame) :** Les résultats filtrés sont présentés dans un tableau interactif. Vous pouvez trier et filtrer directement dans ce tableau pour une exploration plus approfondie.
    - **Graphiques en Camembert :** Deux graphiques circulaires vous montrent les 10 principales occurrences des dangers et des matrices. Cela vous donne un aperçu visuel rapide des tendances principales dans les données.
    - **Liens Cliquables :** Les colonnes contenant des liens sont formatées pour que vous puissiez cliquer directement et accéder aux ressources externes pertinentes. Cela inclut des liens vers des documents ou des pages web spécifiques mentionnés dans les bulletins.

    Cette application est conçue pour être intuitive, même si les filtres peuvent parfois paraître détaillés. N'hésitez pas à explorer les différentes options pour mieux comprendre les données de BuSCA.
    """)


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
    columns_to_drop = ["Type"]
    df = df.drop(columns=columns_to_drop, errors='ignore')

    # Initialiser les variables pour éviter les erreurs NameError
    countries, matrices = [], []
    busca_range, dangers, sections = None, [], []
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

        # Filtrage par Danger
        danger_col = 'Danger'
        if danger_col in df.columns:
            dangers = st.multiselect("Sélectionner les dangers", options=df[danger_col].unique())

        # Filtrage par Section
        section_col = 'Section'
        if section_col in df.columns:
            sections = st.multiselect("Sélectionner les sections", options=df[section_col].unique())

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

        # Appliquer les filtres de Danger
        if dangers:
            df = df[df[danger_col].isin(dangers)]

        # Appliquer les filtres de Section
        if sections:
            df = df[df[section_col].isin(sections)]

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
            if danger_col in df.columns:
                danger_counts = df[danger_col].value_counts().nlargest(10)  # Les 10 principales occurrences
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
