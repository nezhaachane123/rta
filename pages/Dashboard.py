



# ########################################################################code final

# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime, timedelta
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials


# # Configuration de la page
# st.set_page_config(
#     page_title="Dashboard",
#     page_icon="📈",
#     layout="wide",
# )

# # Vérifier si l'utilisateur est connecté
# if 'logged_in' not in st.session_state or not st.session_state.logged_in:
#     st.warning("⚠️ Vous devez vous connecter pour accéder à cette page.")
#     st.info("Retournez à la page d'accueil pour vous connecter.")
#     st.stop()

# # Titre et informations utilisateur
# st.title(f"📈 Dashboard - Bienvenue {st.session_state.username}!")


    
# # Bouton Admin uniquement pour les administrateurs
# if st.session_state.role == "admin":
#     if st.button("Page d'Administration"):
#         st.switch_page("pages/Admin.py")

# # Bouton de déconnexion
# if st.button("Déconnexion"):
#     st.session_state.logged_in = False
#     st.session_state.username = ""
#     st.session_state.role = ""
#     st.switch_page("Home.py") 

# # Fonction pour charger les données
# @st.cache_data(ttl=600)  # Mise en cache des données pendant 10 minutes
# def load_data():
#     try:
#         # Connexion à Google Sheets
#         scope = [
#             "https://spreadsheets.google.com/feeds",
#             "https://www.googleapis.com/auth/drive"
#         ]

#         creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
#         client = gspread.authorize(creds)
        
#         # Ouvrir le classeur Google Sheets
#         spreadsheet = client.open("mydata")
        
#         # Récupérer la première feuille
#         sheet1 = spreadsheet.sheet1
#         all_data1 = sheet1.get_all_records()
#         df1 = pd.DataFrame(all_data1)
        
#         # Récupérer la deuxième feuille
#         sheet2 = spreadsheet.get_worksheet(1)
#         all_data2 = sheet2.get_all_records()
#         df2 = pd.DataFrame(all_data2)
        
#         # S'assurer que la colonne Date est au format datetime
#         if 'Date' in df1.columns:
#             df1['Date'] = pd.to_datetime(df1['Date'], format='%d/%m/%Y')
        
#         if 'Date' in df2.columns:
#             df2['Date'] = pd.to_datetime(df2['Date'], format='%d/%m/%Y')
        
#         # Conversion des durées
#         time_cols = ['Prod', 'Pause_planning', 'Lunch', 'Pause_realise', 'prod_realise']
#         for col in time_cols:
#             if col in df1.columns:
#                 df1[col] = pd.to_timedelta(df1[col]).dt.total_seconds()
#             if col in df2.columns:
#                 df2[col] = pd.to_timedelta(df2[col]).dt.total_seconds()
                
#         # Combinaison des dataframes
#         df_combined = pd.concat([df1, df2])
#         return df_combined
#     except Exception as e:
#         st.error(f"Erreur lors du chargement des données : {e}")
#         return pd.DataFrame()

# # Charger les données
# data = load_data()


# # Vérifier si les données sont chargées correctement
# if data.empty:
#     st.warning("Aucune donnée n'a été chargée. Vérifiez la connexion à Google Sheets.")
# else:
#     # Sélecteur de plage de dates
#     st.sidebar.header("Filtres")
    
#     # Obtenir les dates uniques des données
#     unique_dates = sorted(data['Date'].dt.date.unique())
    
#     # Sélecteur de date de début parmi les dates uniques
#     start_date_index = st.sidebar.selectbox(
#         "Date de début",
#         options=range(len(unique_dates)),
#         format_func=lambda x: unique_dates[x].strftime('%d/%m/%Y'),
#         index=0
#     )
#     start_date = unique_dates[start_date_index]
    
#     # Sélecteur de date de fin parmi les dates uniques (à partir de la date de début)
#     end_date_index = st.sidebar.selectbox(
#         "Date de fin",
#         options=range(start_date_index, len(unique_dates)),
#         format_func=lambda x: unique_dates[x].strftime('%d/%m/%Y'),
#         index=len(unique_dates) - 1 - start_date_index
#     )
#     end_date = unique_dates[end_date_index]
    
#     # Filtrer les données selon la plage de dates sélectionnée
#     mask = (data['Date'].dt.date >= start_date) & (data['Date'].dt.date <= end_date)
#     filtered_data = data.loc[mask]
    
#     # Extraction des tranches horaires uniques
#     tranche_values = []
#     for tranche in filtered_data['Tranche'].dropna().unique():
#         if ':' in str(tranche):
#             # Extraire l'heure si la tranche est au format HH:MM
#             heure = tranche.split(' ')[-1] if ' ' in str(tranche) else tranche
#             tranche_values.append(heure)
    
#     # Trier et obtenir les tranches uniques
#     unique_tranches = sorted(set(tranche_values))
    
#     if unique_tranches:
#         # Sélecteur de tranches horaires
#         selected_tranches = st.sidebar.multiselect(
#             "Filtrer par Tranche horaire",
#             options=unique_tranches,
#             default=None,
#             placeholder="Sélectionnez une ou plusieurs tranches horaires"
#         )
        
#         # Filtrer par tranche si des tranches sont sélectionnées
#         if selected_tranches:
#             tranche_filter = filtered_data['Tranche'].astype(str).apply(
#                 lambda x: any(tranche in x for tranche in selected_tranches)
#             )
#             filtered_data = filtered_data[tranche_filter]
    
#     # Filtres additionnels
#     files = st.sidebar.multiselect("Files", options=sorted(filtered_data['File'].unique()))
#     tls = st.sidebar.multiselect("TLS", options=sorted(filtered_data['Tls'].unique()))
#     ops = st.sidebar.multiselect("OPS", options=sorted(filtered_data['OPS'].unique()))
    
#     # Appliquer les filtres supplémentaires
#     if files:
#         filtered_data = filtered_data[filtered_data['File'].isin(files)]
#     if tls:
#         filtered_data = filtered_data[filtered_data['Tls'].isin(tls)]
#     if ops:
#         filtered_data = filtered_data[filtered_data['OPS'].isin(ops)]
    
#     # Vérifier si des données existent après filtrage
#     if filtered_data.empty:
#         st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
#     else:
#         # Affichage des KPIs en haut de la page
#         st.header("Indicateurs clés de performance")
        
#         col1, col2, col3, col4 = st.columns(4)
        
#         # KPI 1: Adhérence moyenne globale (corrigée)
#         # D'abord calculer l'adhérence moyenne par agent
#         agent_adherence = filtered_data.groupby('Nom Agent')['Adherence'].apply(
#             lambda x: x.str.rstrip('%').astype(float).mean()
#         )
#         # Ensuite calculer la moyenne des moyennes des agents
#         avg_adherence = agent_adherence.mean()
        
#         col1.metric(
#             label="Adhérence Moyenne",
#             value=f"{avg_adherence:.2f}%",
#             delta=None
#         )
        
#         # KPI 2: Nombre d'agents
#         num_agents = filtered_data['Nom Agent'].nunique()
#         col2.metric(
#             label="Nombre d'Agents",
#             value=num_agents,
#             delta=None
#         )
        
#         # KPI 3: Nombre de jours
#         num_days = filtered_data['Date'].dt.date.nunique()
#         col3.metric(
#             label="Période Analysée",
#             value=f"{num_days} jours",
#             delta=None
#         )
        
#         # KPI 4: % d'agents avec adhérence moyenne >= 90%
#         # On réutilise agent_adherence calculé précédemment
        
#         # Compter le nombre d'agents avec adhérence moyenne >= 90%
#         agents_above_90 = (agent_adherence >= 90).sum()
#         total_agents = len(agent_adherence)
        
#         # Calculer le pourcentage d'agents avec adhérence >= 90%
#         if total_agents > 0:
#             good_adherence_percent = (agents_above_90 / total_agents) * 100
#         else:
#             good_adherence_percent = 0
            
#         col4.metric(
#             label="Agents avec ≥90% Adhérence",
#             value=f"{good_adherence_percent:.2f}%",
#             delta=None
#         )
        
#         # Affichage des filtres appliqués
#         filter_info = []
#         if start_date == end_date:
#             filter_info.append(f"Date: {start_date.strftime('%d/%m/%Y')}")
#         else:
#             filter_info.append(f"Période: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")
        
#         if selected_tranches:
#             filter_info.append(f"Tranches: {', '.join(selected_tranches)}")
#         if files:
#             filter_info.append(f"Files: {', '.join(files)}")
#         if tls:
#             filter_info.append(f"TLS: {', '.join(tls)}")
#         if ops:
#             filter_info.append(f"OPS: {', '.join(ops)}")
        
#         st.info(f"Filtres appliqués: {' | '.join(filter_info)}")
        
#         # Graphiques du dashboard
#         st.header("Analyse de l'Adhérence")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Graphique 1: Évolution de l'adhérence dans le temps
#             st.subheader("Évolution de l'Adhérence")
            
#             # Regrouper d'abord par date et agent, puis calculer la moyenne d'adhérence par agent
#             adherence_by_date_agent = filtered_data.groupby([filtered_data['Date'].dt.date, 'Nom Agent'])['Adherence'].apply(
#                 lambda x: x.str.rstrip('%').astype(float).mean()
#             ).reset_index()
            
#             # Ensuite regrouper par date et calculer la moyenne des moyennes d'agents
#             adherence_by_date = adherence_by_date_agent.groupby('Date')['Adherence'].mean().reset_index()
#             adherence_by_date.columns = ['Date', 'Adhérence Moyenne']
            
#             # Créer le graphique avec Plotly
#             fig = px.line(
#                 adherence_by_date, 
#                 x='Date', 
#                 y='Adhérence Moyenne',
#                 markers=True,
#                 line_shape='linear'
#             )
#             fig.update_layout(
#                 yaxis_range=[0, 100],
#                 title_text=f"Évolution de l'adhérence moyenne ({start_date.strftime('%d/%m')} - {end_date.strftime('%d/%m')})"
#             )
#             st.plotly_chart(fig, use_container_width=True)
        
#         with col2:
#             # Graphique 2: Distribution de l'adhérence
#             st.subheader("Distribution de l'Adhérence")
            
#             # Calculer l'adhérence moyenne par agent (réutiliser agent_adherence)
            
#             # Créer des tranches d'adhérence
#             bins = [0, 70, 80, 90, 100]
#             labels = ['<70%', '70-80%', '80-90%', '≥90%']
#             adherence_bins = pd.cut(agent_adherence, bins=bins, labels=labels)
            
#             # Compter le nombre d'agents dans chaque tranche
#             adherence_counts = adherence_bins.value_counts().reset_index()
#             adherence_counts.columns = ['Tranche', 'Nombre']
            
#             # Couleurs selon la tranche
#             colors = {
#                 '<70%': 'red',
#                 '70-80%': 'orange',
#                 '80-90%': 'yellow',
#                 '≥90%': 'green'
#             }
            
#             # Créer le graphique avec Plotly
#             fig = px.bar(
#                 adherence_counts,
#                 x='Tranche',
#                 y='Nombre',
#                 color='Tranche',
#                 color_discrete_map=colors,
#                 text='Nombre'
#             )
#             fig.update_layout(
#                 title_text="Répartition des adhérences par niveau"
#             )
#             st.plotly_chart(fig, use_container_width=True)
        
#         # Deuxième ligne de graphiques
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Graphique 3: Top 10 meilleurs agents en adhérence
#             st.subheader("Top 10 Agents - Meilleure Adhérence")
            
#             # Convertir agent_adherence en dataframe pour le graphique
#             agent_adherence_df = agent_adherence.reset_index()
#             agent_adherence_df.columns = ['Nom Agent', 'Adhérence Moyenne']
            
#             # Trier et prendre les 10 meilleurs
#             top_agents = agent_adherence_df.sort_values('Adhérence Moyenne', ascending=False).head(10)
            
#             # Créer le graphique avec Plotly
#             fig = px.bar(
#                 top_agents,
#                 x='Adhérence Moyenne',
#                 y='Nom Agent',
#                 orientation='h',
#                 color='Adhérence Moyenne',
#                 color_continuous_scale='greens',
#                 text='Adhérence Moyenne'
#             )
#             fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
#             fig.update_layout(
#                 xaxis_range=[0, 100],
#                 title_text="Meilleurs agents par adhérence moyenne"
#             )
#             st.plotly_chart(fig, use_container_width=True)
        
#         with col2:
#             # Graphique 4: Adhérence moyenne par File
#             st.subheader("Adhérence par File")
            
#             # Calculer d'abord l'adhérence moyenne par agent et par file
#             file_agent_adherence = filtered_data.groupby(['File', 'Nom Agent'])['Adherence'].apply(
#                 lambda x: x.str.rstrip('%').astype(float).mean()
#             ).reset_index()
            
#             # Ensuite calculer la moyenne des moyennes d'agents par file
#             file_adherence = file_agent_adherence.groupby('File')['Adherence'].mean().reset_index()
#             file_adherence.columns = ['File', 'Adhérence Moyenne']
            
#             # Trier par adhérence décroissante
#             file_adherence = file_adherence.sort_values('Adhérence Moyenne', ascending=False)
            
#             # Créer le graphique avec Plotly
#             fig = px.bar(
#                 file_adherence,
#                 x='File',
#                 y='Adhérence Moyenne',
#                 color='Adhérence Moyenne',
#                 color_continuous_scale='blues',
#                 text='Adhérence Moyenne'
#             )
#             fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
#             fig.update_layout(
#                 yaxis_range=[0, 100],
#                 title_text="Adhérence par file"
#             )
#             st.plotly_chart(fig, use_container_width=True)
#         with col1:
#             # Graphique 5: Adhérence moyenne et Temps de production par agent
#             st.subheader("Adhérence et Production par Agent")
            
#             # Calculer pour chaque agent : l'adhérence moyenne et le temps total de production
#             agent_metrics = filtered_data.groupby('Nom Agent').agg({
#                 'Adherence': lambda x: x.str.rstrip('%').astype(float).mean(),
#                 'Prod': 'sum'  # Temps total de production par agent
#             }).reset_index()
            
#             # Convertir le temps de production en heures pour une meilleure lisibilité
#             agent_metrics['Prod (heures)'] = agent_metrics['Prod'] / 3600
            
#             # Trier par adhérence (ou par production si vous préférez)
#             agent_metrics = agent_metrics.sort_values('Adherence', ascending=False)
            
#             # Limiter à un nombre raisonnable d'agents pour la lisibilité (top 15 par exemple)
#             if len(agent_metrics) > 15:
#                 agent_metrics = agent_metrics.head(15)
            
#             # Créer une figure avec deux axes Y
#             fig = go.Figure()
            
#             # Ajouter la ligne d'adhérence sur l'axe Y primaire
#             fig.add_trace(go.Scatter(
#                 x=agent_metrics['Nom Agent'],
#                 y=agent_metrics['Adherence'],
#                 name='Adhérence Moyenne (%)',
#                 mode='lines+markers',
#                 line=dict(color='green', width=3),
#                 marker=dict(size=10)
#             ))
            
#             # Ajouter la ligne de production sur l'axe Y secondaire
#             fig.add_trace(go.Scatter(
#                 x=agent_metrics['Nom Agent'],
#                 y=agent_metrics['Prod (heures)'],
#                 name='Temps de Production (heures)',
#                 mode='lines+markers',
#                 line=dict(color='blue', width=3, dash='dash'),
#                 marker=dict(size=10),
#                 yaxis='y2'
#             ))
            
#             # Ajouter une ligne horizontale à 90% pour l'objectif d'adhérence
#             fig.add_hline(y=90, line_dash="dot", line_color="red", 
#                         annotation_text="Objectif 90%", annotation_position="top right")
            
#             # Mettre en forme le graphique avec deux axes Y
#             fig.update_layout(
#                 title="Adhérence Moyenne et Temps de Production par Agent",
#                 xaxis=dict(
#                     title="Agent",
#                     tickangle=45
#                 ),
#                 yaxis=dict(
#                     title="Adhérence Moyenne (%)",
#                     range=[0, 105],
#                     side="left",
#                     showgrid=True
#                 ),
#                 yaxis2=dict(
#                     title="Temps de Production (heures)",
#                     side="right",
#                     overlaying="y",
#                     showgrid=False
#                 ),
#                 legend=dict(
#                     orientation="h",
#                     yanchor="bottom",
#                     y=1.02,
#                     xanchor="center",
#                     x=0.5
#                 ),
#                 height=600,
#                 margin=dict(t=100, b=100)
#             )
            
#             st.plotly_chart(fig, use_container_width=True)
#         with col2:
#             # Graphique 6: Répartition des temps par type (prévu vs réalisé)
#             st.subheader("Répartition des Temps")
            
#             # Calculer d'abord par agent les totaux de temps pour chaque catégorie
#             agent_times = filtered_data.groupby('Nom Agent').agg({
#                 'Prod': 'sum',
#                 'Pause_planning': 'sum',
#                 'Lunch': 'sum',
#                 'prod_realise': 'sum',
#                 'Pause_realise': 'sum'
#             }).reset_index()
            
#             # Calculer les totaux pour tous les agents
#             total_prod_planning = agent_times['Prod'].sum()
#             total_pause_planning = agent_times['Pause_planning'].sum()
#             total_lunch_planning = agent_times['Lunch'].sum()
#             total_prod_realise = agent_times['prod_realise'].sum()
#             total_pause_realise = agent_times['Pause_realise'].sum()
            
#             # Calculer le temps total de lunch réalisé (non directement disponible, le déduire)
#             # Si on suppose que: Total temps réalisé = prod_realise + Pause_realise + lunch_realise
#             # Et que le total réalisé = total prévu, alors:
#             total_time_planning = total_prod_planning + total_pause_planning + total_lunch_planning
#             total_time_realise = total_prod_realise + total_pause_realise
#             total_lunch_realise = total_time_planning - total_time_realise if total_time_realise < total_time_planning else 0
            
#             # Convertir en heures pour une meilleure lisibilité
#             planning_data = pd.DataFrame({
#                 'Catégorie': ['Production', 'Pause', 'Déjeuner'],
#                 'Type': ['Prévu', 'Prévu', 'Prévu'],
#                 'Temps (heures)': [
#                     total_prod_planning / 3600,
#                     total_pause_planning / 3600,
#                     total_lunch_planning / 3600
#                 ]
#             })
            
#             realise_data = pd.DataFrame({
#                 'Catégorie': ['Production', 'Pause', 'Déjeuner'],
#                 'Type': ['Réalisé', 'Réalisé', 'Réalisé'],
#                 'Temps (heures)': [
#                     total_prod_realise / 3600,
#                     total_pause_realise / 3600,
#                     total_lunch_realise / 3600
#                 ]
#             })
            
#             # Combiner les dataframes
#             time_data = pd.concat([planning_data, realise_data])
            
#             # Créer un graphique en barres groupées
#             colors = {
#                 'Production': '#FF6B6B', 
#                 'Pause': '#4ECDC4', 
#                 'Déjeuner': '#FFD166'
#             }
            
#             fig = px.bar(
#                 time_data,
#                 x='Type',
#                 y='Temps (heures)',
#                 color='Catégorie',
#                 barmode='group',
#                 color_discrete_map=colors,
#                 text='Temps (heures)',
#                 title="Répartition des temps de travail : Prévu vs Réalisé",
#                 labels={
#                     'Type': '',
#                     'Temps (heures)': 'Durée (heures)',
#                     'Catégorie': 'Type d\'activité'
#                 }
#             )
            
#             # Formater les valeurs (1 décimale)
#             fig.update_traces(texttemplate='%{text:.1f}h', textposition='outside')
            
#             # Calculer les pourcentages pour ajouter au titre
#             total_planning = total_prod_planning + total_pause_planning + total_lunch_planning
#             total_realise = total_prod_realise + total_pause_realise + total_lunch_realise
            
#             if total_planning > 0:
#                 prod_planning_pct = (total_prod_planning / total_planning) * 100
#                 pause_planning_pct = (total_pause_planning / total_planning) * 100
#                 lunch_planning_pct = (total_lunch_planning / total_planning) * 100
#             else:
#                 prod_planning_pct = pause_planning_pct = lunch_planning_pct = 0
            
#             if total_realise > 0:
#                 prod_realise_pct = (total_prod_realise / total_realise) * 100
#                 pause_realise_pct = (total_pause_realise / total_realise) * 100
#                 lunch_realise_pct = (total_lunch_realise / total_realise) * 100
#             else:
#                 prod_realise_pct = pause_realise_pct = lunch_realise_pct = 0
            
#             # Ajouter une annotation avec les pourcentages
#             fig.add_annotation(
#                 x=0.5, y=1.15,
#                 text=f"Prévu: Production {prod_planning_pct:.1f}%, Pause {pause_planning_pct:.1f}%, Déjeuner {lunch_planning_pct:.1f}%<br>"
#                     f"Réalisé: Production {prod_realise_pct:.1f}%, Pause {pause_realise_pct:.1f}%, Déjeuner {lunch_realise_pct:.1f}%",
#                 showarrow=False,
#                 xref='paper', yref='paper',
#                 font=dict(size=12)
#             )
            
#             st.plotly_chart(fig, use_container_width=True)
#     st.warning("Pour voir la visualisation détaillée par agent, cliquez sur l'option **Real Time Adherence** dans le menu de gauche ")



import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuration de la page
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
)

# CSS personnalisé pour améliorer l'apparence
st.markdown("""
<style>
    /* Styles globaux */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Fond global et sidebar */
    .stApp {
        background-color: #f8f9fa;
    }
    
    .stSidebar {
        background-color: #ffffff;
        border-right: 1px solid #e6e6e6;
    }
    
    /* Style des cartes */
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
        border-top: 4px solid #1a73e8;
    }
    
    /* Style des en-têtes */
    h1 {
        color: #212121;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 2rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #f0f0f0;
    }
    
    h2, h3 {
        color: #424242;
        font-weight: 500;
    }
    
    /* Style des métriques */
    div[data-testid="stMetric"] {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        color: #1a73e8;
    }
    
    /* Style des boutons */
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #0d47a1;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Style des filtres */
    .stSelectbox, .stMultiSelect {
        background-color: white;
        border-radius: 6px;
        padding: 0.5rem;
        box-shadow: 0 1px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    /* Style des graphiques */
    div[data-testid="stDecoration"] {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* Info banners */
    div[data-testid="stAlert"] {
        border-radius: 8px;
        font-size: 0.9rem;
    }
    
    /* Animation de transition */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .dashboard-container {
        animation: fadeIn 0.5s ease forwards;
    }
    
    /* Palette de couleurs pour les graphiques */
    .custom-plot {
        --color-primary: #1a73e8;
        --color-secondary: #00bcd4;
        --color-success: #4caf50;
        --color-warning: #ff9800;
        --color-error: #f44336;
    }
    
    /* Style des onglets */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f3f4f6;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1a73e8 !important;
        color: white !important;
    }
    
    /* Style pour la boîte des pourcentages */
    .percentage-box {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 15px;
        text-align: center;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Vérifier si l'utilisateur est connecté
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Vous devez vous connecter pour accéder à cette page.")
    st.info("Retournez à la page d'accueil pour vous connecter.")
    st.stop()

# En-tête de la page avec animation
st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
st.markdown(f"""
<div style="display: flex; align-items: center; margin-bottom: 1rem;">
    <h1 style="margin: 0; font-size: 2rem;">
        <span style="color: #1a73e8; margin-right: 10px;">📊</span> 
        Tableau de bord d'adhérence
    </h1>
    <div style="margin-left: auto; padding: 8px 15px; background-color: #e8f0fe; border-radius: 30px; display: flex; align-items: center;">
        <span style="color: #1a73e8; margin-right: 8px;">👤</span>
        <span style="font-weight: 500;">{st.session_state.username}</span>
        <span style="margin: 0 5px; color: #949494;">|</span>
        <span style="color: #666; font-size: 0.9rem;">{st.session_state.role}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Barre de navigation
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.session_state.role == "admin" and st.button("👑 Administration"):
        st.switch_page("pages/Admin.py")
        
with col2:
    if st.button("📈 Real Time Adherence"):
        st.switch_page("pages/Real_Time_Adherence.py")
        
with col3:
    if st.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.switch_page("Home.py")

# Ligne de séparation
st.markdown('<hr style="margin: 1rem 0; border: none; height: 1px; background-color: #e0e0e0;">', unsafe_allow_html=True)

# Fonction pour charger les données
@st.cache_data(ttl=600)
def load_data():
    try:
        # Connexion à Google Sheets
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        
        # Ouvrir le classeur Google Sheets
        spreadsheet = client.open("mydata")
        
        # Récupérer toutes les feuilles du classeur
        all_worksheets = spreadsheet.worksheets()
        
        # Liste pour stocker tous les DataFrames
        all_dfs = []
        
        # Pour chaque feuille, récupérer les données
        for worksheet in all_worksheets:
            sheet_name = worksheet.title
            
            # Récupérer les données
            all_data = worksheet.get_all_records()
            
            # Vérifier si la feuille contient des données
            if all_data:
                # Créer un DataFrame
                df = pd.DataFrame(all_data)
                
                # Ajouter le nom de la feuille comme colonne pour identification
                df['source_sheet'] = sheet_name
                
                # S'assurer que la colonne Date est au format datetime
                if 'Date' in df.columns:
                    try:
                        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
                    except:
                        st.warning(f"Problème de conversion de date dans la feuille {sheet_name}")
                
                # Conversion des durées
                time_cols = ['Prod', 'Pause_planning', 'Lunch', 'Pause_realise', 'prod_realise']
                for col in time_cols:
                    if col in df.columns:
                        try:
                            df[col] = pd.to_timedelta(df[col]).dt.total_seconds()
                        except:
                            # Si erreur, continuer sans bloquer
                            pass
                
                # Ajouter le DataFrame à la liste
                all_dfs.append(df)
        
        # Combiner tous les DataFrames
        if all_dfs:
            df_combined = pd.concat(all_dfs, ignore_index=True)
            return df_combined
        else:
            st.warning("Aucune donnée n'a été trouvée dans les feuilles du classeur.")
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return pd.DataFrame()

# Charger les données
with st.spinner("Chargement des données..."):
    data = load_data()

# Vérifier si les données sont chargées correctement
if data.empty:
    st.warning("Aucune donnée n'a été chargée. Vérifiez la connexion à Google Sheets.")
else:
    # Section des filtres dans la sidebar
    st.sidebar.markdown("""
    <div style="background-color: #1a73e8; padding: 10px; border-radius: 8px; color: white; text-align: center; margin-bottom: 20px; font-weight: 600;">
        FILTRES
    </div>
    """, unsafe_allow_html=True)
    
    # Obtenir les dates uniques des données
    unique_dates = sorted(data['Date'].dt.date.unique())
    
    # Sélecteur de date de début parmi les dates uniques
    st.sidebar.markdown("### Période d'analyse")
    start_date_index = st.sidebar.selectbox(
        "Date de début",
        options=range(len(unique_dates)),
        format_func=lambda x: unique_dates[x].strftime('%d/%m/%Y'),
        index=0
    )
    start_date = unique_dates[start_date_index]
    
    # Sélecteur de date de fin
    end_date_index = st.sidebar.selectbox(
        "Date de fin",
        options=range(start_date_index, len(unique_dates)),
        format_func=lambda x: unique_dates[x].strftime('%d/%m/%Y'),
        index=len(unique_dates) - 1 - start_date_index
    )
    end_date = unique_dates[end_date_index]
    
    # Filtrer les données selon la plage de dates sélectionnée
    mask = (data['Date'].dt.date >= start_date) & (data['Date'].dt.date <= end_date)
    filtered_data = data.loc[mask]
    
    # Filtres additionnels avec séparateurs visuels
    st.sidebar.markdown('<div style="margin: 15px 0; height: 1px; background: #e0e0e0;"></div>', unsafe_allow_html=True)
    st.sidebar.markdown("### Filtres additionnels")
    
    # Extraction et sélection des tranches horaires
    tranche_values = []
    for tranche in filtered_data['Tranche'].dropna().unique():
        if ':' in str(tranche):
            heure = tranche.split(' ')[-1] if ' ' in str(tranche) else tranche
            tranche_values.append(heure)
    
    unique_tranches = sorted(set(tranche_values))
    if unique_tranches:
        selected_tranches = st.sidebar.multiselect(
            "Tranches horaires",
            options=unique_tranches,
            default=None,
            placeholder="Sélectionnez une ou plusieurs tranches horaires"
        )
        
        if selected_tranches:
            tranche_filter = filtered_data['Tranche'].astype(str).apply(
                lambda x: any(tranche in x for tranche in selected_tranches)
            )
            filtered_data = filtered_data[tranche_filter]
    
    # Autres filtres
    files = st.sidebar.multiselect("Files", options=sorted(filtered_data['File'].unique()))
    tls = st.sidebar.multiselect("TLS", options=sorted(filtered_data['Tls'].unique()))
    ops = st.sidebar.multiselect("OPS", options=sorted(filtered_data['OPS'].unique()))
    
    # Appliquer les filtres supplémentaires
    if files:
        filtered_data = filtered_data[filtered_data['File'].isin(files)]
    if tls:
        filtered_data = filtered_data[filtered_data['Tls'].isin(tls)]
    if ops:
        filtered_data = filtered_data[filtered_data['OPS'].isin(ops)]
    
    # Bouton de rafraîchissement des données
    st.sidebar.markdown('<div style="margin: 15px 0; height: 1px; background: #e0e0e0;"></div>', unsafe_allow_html=True)
    if st.sidebar.button("🔄 Rafraîchir les données"):
        st.cache_data.clear()
        st.rerun()
    
    # Afficher un résumé des filtres appliqués
    filter_info = []
    if start_date == end_date:
        filter_info.append(f"Date: {start_date.strftime('%d/%m/%Y')}")
    else:
        filter_info.append(f"Période: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")
    
    if selected_tranches:
        filter_info.append(f"Tranches: {', '.join(selected_tranches)}")
    if files:
        filter_info.append(f"Files: {', '.join(files)}")
    if tls:
        filter_info.append(f"TLS: {', '.join(tls)}")
    if ops:
        filter_info.append(f"OPS: {', '.join(ops)}")
    
    # Vérifier si des données existent après filtrage
    if filtered_data.empty:
        st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
    else:
        # Afficher les filtres appliqués
        st.info(f"📌 Filtres appliqués: {' | '.join(filter_info)}")
        
        # Affichage des KPIs en haut de la page
        st.markdown("## Indicateurs clés de performance")
        
        # Calculer les KPIs
        agent_adherence = filtered_data.groupby('Nom Agent')['Adherence'].apply(
            lambda x: x.str.rstrip('%').astype(float).mean()
        )
        avg_adherence = agent_adherence.mean()
        num_agents = filtered_data['Nom Agent'].nunique()
        num_days = filtered_data['Date'].dt.date.nunique()
        agents_above_90 = (agent_adherence >= 90).sum()
        total_agents = len(agent_adherence)
        good_adherence_percent = (agents_above_90 / total_agents) * 100 if total_agents > 0 else 0
        
        # Afficher les KPIs dans des cartes modernes
        kpi_cols = st.columns(4)
        with kpi_cols[0]:
            st.metric(
                label="Adhérence Moyenne",
                value=f"{avg_adherence:.2f}%",
                delta=None
            )
        
        with kpi_cols[1]:
            st.metric(
                label="Nombre d'Agents",
                value=num_agents,
                delta=None
            )
        
        with kpi_cols[2]:
            st.metric(
                label="Période Analysée",
                value=f"{num_days} jours",
                delta=None
            )
        
        with kpi_cols[3]:
            st.metric(
                label="Agents avec ≥90% Adhérence",
                value=f"{good_adherence_percent:.2f}%",
                delta=None
            )
        
        # Graphiques du dashboard dans des sections distinctes
        st.markdown("## Analyse de l'Adhérence")
        
        # Première ligne de graphiques
        graph_cols1 = st.columns(2)
        
        with graph_cols1[0]:
            # Graphique 1: Évolution de l'adhérence dans le temps
            st.markdown("---")
            st.subheader("Évolution de l'Adhérence")
            
            # Préparation des données
            adherence_by_date_agent = filtered_data.groupby([filtered_data['Date'].dt.date, 'Nom Agent'])['Adherence'].apply(
                lambda x: x.str.rstrip('%').astype(float).mean()
            ).reset_index()
            
            adherence_by_date = adherence_by_date_agent.groupby('Date')['Adherence'].mean().reset_index()
            adherence_by_date.columns = ['Date', 'Adhérence Moyenne']
            
            # Graphique avec style amélioré
            fig = px.line(
                adherence_by_date, 
                x='Date', 
                y='Adhérence Moyenne',
                markers=True,
                line_shape='linear'
            )
            fig.update_layout(
                yaxis_range=[0, 100],
                title=None,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins, sans-serif"),
                margin=dict(l=10, r=10, t=10, b=10),
                hovermode="x unified",
                xaxis=dict(
                    title="Date",
                    gridcolor='rgba(211,211,211,0.3)',
                    tickformat='%d/%m/%Y'
                ),
                yaxis=dict(
                    title="Adhérence Moyenne (%)",
                    gridcolor='rgba(211,211,211,0.3)'
                )
            )
            fig.update_traces(
                line_color='#1a73e8',
                marker=dict(size=8, color='#0d47a1')
            )
            # Ajouter ligne de référence à 90%
            fig.add_hline(
                y=90, 
                line_dash="dash", 
                line_color="#4caf50",
                annotation_text="Objectif 90%",
                annotation_position="top right"
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with graph_cols1[1]:
            # Graphique 2: Distribution de l'adhérence
            st.markdown("---")
            st.subheader("Distribution de l'Adhérence")
            
            # Créer des tranches d'adhérence
            bins = [0, 70, 80, 90, 100]
            labels = ['<70%', '70-80%', '80-90%', '≥90%']
            adherence_bins = pd.cut(agent_adherence, bins=bins, labels=labels)
            
            # Compter le nombre d'agents dans chaque tranche
            adherence_counts = adherence_bins.value_counts().reset_index()
            adherence_counts.columns = ['Tranche', 'Nombre']
            
            # Couleurs selon la tranche avec une palette moderne
            colors = {
                '<70%': '#f44336',  # Rouge
                '70-80%': '#ff9800',  # Orange
                '80-90%': '#ffc107',  # Jaune
                '≥90%': '#4caf50'   # Vert
            }
            
            # Créer le graphique avec style amélioré
            fig = px.bar(
                adherence_counts,
                x='Tranche',
                y='Nombre',
                color='Tranche',
                color_discrete_map=colors,
                text='Nombre'
            )
            fig.update_layout(
                title=None,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins, sans-serif"),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(
                    title="Niveau d'adhérence",
                    gridcolor='rgba(211,211,211,0.3)'
                ),
                yaxis=dict(
                    title="Nombre d'agents",
                    gridcolor='rgba(211,211,211,0.3)'
                ),
                legend_title_text=None
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Deuxième ligne de graphiques
        graph_cols2 = st.columns(2)
        
        with graph_cols2[0]:
            # Graphique 3: Top 10 meilleurs agents en adhérence
            st.markdown("---")
            st.subheader("Top 10 - Meilleure Adhérence")
            
            # Préparation des données
            agent_adherence_df = agent_adherence.reset_index()
            agent_adherence_df.columns = ['Nom Agent', 'Adhérence Moyenne']
            
            # Trier et prendre les 10 meilleurs
            top_agents = agent_adherence_df.sort_values('Adhérence Moyenne', ascending=False).head(10)
            
            # Graphique avec style amélioré
            fig = px.bar(
                top_agents,
                x='Adhérence Moyenne',
                y='Nom Agent',
                orientation='h',
                text='Adhérence Moyenne',
                color='Adhérence Moyenne',
                color_continuous_scale=[(0, '#ff9800'), (0.5, '#8bc34a'), (1, '#4caf50')]
            )
            fig.update_layout(
                title=None,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins, sans-serif"),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(
                    title="Adhérence Moyenne (%)",
                    range=[0, 100],
                    gridcolor='rgba(211,211,211,0.3)'
                ),
                yaxis=dict(
                    title=None,
                    autorange="reversed"
                ),
                coloraxis_showscale=False
            )
            fig.update_traces(
                texttemplate='%{text:.2f}%', 
                textposition='outside',
                marker_line_width=0
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with graph_cols2[1]:
            # Graphique 4: Adhérence moyenne par File
            st.markdown("---")
            st.subheader("Adhérence par File")
            
            # Préparation des données
            file_agent_adherence = filtered_data.groupby(['File', 'Nom Agent'])['Adherence'].apply(
                lambda x: x.str.rstrip('%').astype(float).mean()
            ).reset_index()
            
            file_adherence = file_agent_adherence.groupby('File')['Adherence'].mean().reset_index()
            file_adherence.columns = ['File', 'Adhérence Moyenne']
            file_adherence = file_adherence.sort_values('Adhérence Moyenne', ascending=False)
            
            # Graphique avec style amélioré
            fig = px.bar(
                file_adherence,
                x='File',
                y='Adhérence Moyenne',
                text='Adhérence Moyenne',
                color='Adhérence Moyenne',
                color_continuous_scale=[(0, '#ff9800'), (0.5, '#8bc34a'), (1, '#4caf50')]
            )
            fig.update_layout(
                title=None,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins, sans-serif"),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(
                    title="File",
                    tickangle=45,
                    gridcolor='rgba(211,211,211,0.3)'
                ),
                yaxis=dict(
                    title="Adhérence Moyenne (%)",
                    range=[0, 100],
                    gridcolor='rgba(211,211,211,0.3)'
                ),
                coloraxis_showscale=False
            )
            fig.update_traces(
                texttemplate='%{text:.2f}%', 
                textposition='outside',
                marker_line_width=0
            )
            fig.add_hline(
                y=90, 
                line_dash="dash", 
                line_color="#4caf50",
                annotation_text="Objectif 90%",
                annotation_position="top right"
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Troisième ligne de graphiques
        graph_cols3 = st.columns(2)
        
        with graph_cols3[0]:
            # Graphique 3: Top 10 agents avec adhérence la plus faible
            st.markdown("---")
            st.subheader("10 Agents - Adhérence la Plus Faible")
            
            # Préparation des données
            agent_adherence_df = agent_adherence.reset_index()
            agent_adherence_df.columns = ['Nom Agent', 'Adhérence Moyenne']
            
            # Trier et prendre les 10 plus faibles (au lieu des 10 meilleurs)
            bottom_agents = agent_adherence_df.sort_values('Adhérence Moyenne', ascending=True).head(10)
            
            # Graphique avec style amélioré et couleurs adaptées pour indiquer des scores faibles
            fig = px.bar(
                bottom_agents,
                x='Adhérence Moyenne',
                y='Nom Agent',
                orientation='h',
                text='Adhérence Moyenne',
                color='Adhérence Moyenne',
                # Palette de couleurs inversée pour indiquer les performances faibles
                color_continuous_scale=[(0, '#f44336'), (0.5, '#ff9800'), (1, '#ffc107')]
            )
            fig.update_layout(
                title=None,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins, sans-serif"),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(
                    title="Adhérence Moyenne (%)",
                    range=[0, 100],
                    gridcolor='rgba(211,211,211,0.3)'
                ),
                yaxis=dict(
                    title=None,
                    autorange="reversed"
                ),
                coloraxis_showscale=False
            )
            fig.update_traces(
                texttemplate='%{text:.2f}%', 
                textposition='outside',
                marker_line_width=0
            )
            
            # Ajout d'une ligne de seuil pour indiquer l'objectif de 90%
            fig.add_vline(
                x=90,
                line_dash="dash", 
                line_color="#4caf50",
                annotation_text="Objectif 90%",
                annotation_position="top"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with graph_cols3[1]:
            # Graphique 6: Répartition des temps par type
            st.markdown("---")
            st.subheader("Répartition des Temps de Travail")
            
            # Préparation des données
            agent_times = filtered_data.groupby('Nom Agent').agg({
                'Prod': 'sum',
                'Pause_planning': 'sum',
                'Lunch': 'sum',
                'prod_realise': 'sum',
                'Pause_realise': 'sum'
            }).reset_index()
            
            # Calculer les totaux
            total_prod_planning = agent_times['Prod'].sum()
            total_pause_planning = agent_times['Pause_planning'].sum()
            total_lunch_planning = agent_times['Lunch'].sum()
            total_prod_realise = agent_times['prod_realise'].sum()
            total_pause_realise = agent_times['Pause_realise'].sum()
            
            # Calculer le temps de lunch réalisé
            total_time_planning = total_prod_planning + total_pause_planning + total_lunch_planning
            total_time_realise = total_prod_realise + total_pause_realise
            total_lunch_realise = total_time_planning - total_time_realise if total_time_realise < total_time_planning else 0
            
            # Préparer les données pour le graphique
            planning_data = pd.DataFrame({
                'Catégorie': ['Production', 'Pause', 'Déjeuner'],
                'Type': ['Prévu', 'Prévu', 'Prévu'],
                'Temps (heures)': [
                    total_prod_planning / 3600,
                    total_pause_planning / 3600,
                    total_lunch_planning / 3600
                ]
            })
            
            realise_data = pd.DataFrame({
                'Catégorie': ['Production', 'Pause', 'Déjeuner'],
                'Type': ['Réalisé', 'Réalisé', 'Réalisé'],
                'Temps (heures)': [
                    total_prod_realise / 3600,
                    total_pause_realise / 3600,
                    total_lunch_realise / 3600
                ]
            })
            
            time_data = pd.concat([planning_data, realise_data])
            
            # Calculer les pourcentages
            total_planning = total_prod_planning + total_pause_planning + total_lunch_planning
            total_realise = total_prod_realise + total_pause_realise + total_lunch_realise
            
            if total_planning > 0:
                prod_planning_pct = (total_prod_planning / total_planning) * 100
                pause_planning_pct = (total_pause_planning / total_planning) * 100
                lunch_planning_pct = (total_lunch_planning / total_planning) * 100
            else:
                prod_planning_pct = pause_planning_pct = lunch_planning_pct = 0
            
            if total_realise > 0:
                prod_realise_pct = (total_prod_realise / total_realise) * 100
                pause_realise_pct = (total_pause_realise / total_realise) * 100
                lunch_realise_pct = (total_lunch_realise / total_realise) * 100
            else:
                prod_realise_pct = pause_realise_pct = lunch_realise_pct = 0
            
            # Afficher les pourcentages en HTML avant le graphique
            st.markdown(f"""
            <div class="percentage-box">
                <p style="margin: 0;">
                    <b>Prévu:</b> Production {prod_planning_pct:.1f}%, Pause {pause_planning_pct:.1f}%, Déjeuner {lunch_planning_pct:.1f}%<br>
                    <b>Réalisé:</b> Production {prod_realise_pct:.1f}%, Pause {pause_realise_pct:.1f}%, Déjeuner {lunch_realise_pct:.1f}%
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Couleurs modernes pour les catégories
            colors = {
                'Production': '#1a73e8',  # Bleu
                'Pause': '#00bcd4',       # Turquoise
                'Déjeuner': '#ff9800'     # Orange
            }
            
            # Graphique avec style amélioré
            fig = px.bar(
                time_data,
                x='Type',
                y='Temps (heures)',
                color='Catégorie',
                barmode='group',
                color_discrete_map=colors,
                text='Temps (heures)'
            )
            fig.update_layout(
                title=None,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins, sans-serif"),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(
                    title=None,
                    gridcolor='rgba(211,211,211,0.3)'
                ),
                yaxis=dict(
                    title="Durée (heures)",
                    gridcolor='rgba(211,211,211,0.3)'
                ),
                legend_title=None
            )
            fig.update_traces(texttemplate='%{text:.1f}h', textposition='outside')
            
            # Pas d'annotation dans le graphique, car nous avons déjà affiché les pourcentages en HTML
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        
        
st.markdown('</div>', unsafe_allow_html=True)  # Fermeture du container principal
