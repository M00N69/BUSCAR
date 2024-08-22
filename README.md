# Statistiques des Risques de Veille Sanitaire : Bulletins BuSCA

Cette application Streamlit permet d'analyser et de visualiser les statistiques des risques sanitaires à partir des bulletins BuSCA. Les utilisateurs peuvent filtrer les données selon différents critères et visualiser les résultats sous forme de tableaux et de graphiques interactifs.

## Fonctionnalités

### 1. Chargement des Données
Les données sont automatiquement chargées depuis un fichier Excel accessible via un lien URL. Elles sont ensuite traitées et prêtes à être filtrées et visualisées.

### 2. Interface Utilisateur

#### 2.1. Bannière et Titre
- **Bannière** : Une image est utilisée en arrière-plan de la bannière en haut de la page.
- **Titre Principal** : Le titre "Statistiques des Risques de Veille Sanitaire : Bulletins BuSCA" est affiché en haut de la page.

#### 2.2. Menu Latéral de Filtres
- **Plage de numéros de BuSCA** : Permet de sélectionner une plage de numéros pour filtrer les données.
- **Pays** : Filtre les données par pays.
- **Matrices** : Filtre les données par catégories de matrices.
- **Danger** : Filtre les données selon les types de dangers identifiés.
- **Section** : Filtre les données selon les sections définies.
- **Mots-clés** : Permet de rechercher des occurrences spécifiques dans les colonnes sélectionnées, en utilisant des mots-clés séparés par des virgules.

#### 2.3. Visualisation des Données
- **Graphiques en Camembert** : Deux graphiques affichent les 10 principales occurrences des dangers et des matrices, permettant une visualisation rapide des risques les plus fréquents.
- **Tableau de Données** : Un tableau interactif affiche les données filtrées, avec possibilité de tri et de filtrage supplémentaires.

#### 2.4. Liens Cliquables
Les colonnes contenant des liens sont formatées pour que ces derniers soient cliquables, facilitant ainsi la navigation vers les ressources externes.

## Utilisation

1. **Lancer l'application** : Exécutez l'application via Streamlit (`streamlit run votre_script.py`).
2. **Sélectionner les filtres** : Utilisez le menu latéral pour affiner votre recherche en sélectionnant les filtres désirés.
3. **Appliquer les filtres** : Cliquez sur le bouton "Appliquer les filtres" pour mettre à jour l'affichage des données selon vos critères.
4. **Explorer les résultats** : Visualisez les résultats sous forme de graphiques et de tableaux interactifs.

## Dépendances

- **Python 3.x**
- **Streamlit**
- **Pandas**
- **Requests**
- **Openpyxl**
- **Plotly**

Pour installer les dépendances, exécutez :

```bash
pip install streamlit pandas requests openpyxl plotly
