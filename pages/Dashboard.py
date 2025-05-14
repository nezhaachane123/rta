



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



# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime, timedelta
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # Configuration de la page
# st.set_page_config(
#     page_title="Dashboard",
#     page_icon="📊",
#     layout="wide",
# )

# # CSS personnalisé pour améliorer l'apparence
# st.markdown("""
# <style>
#     /* Styles globaux */
#     @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
#     html, body, [class*="css"] {
#         font-family: 'Poppins', sans-serif;
#     }
    
#     /* Fond global et sidebar */
#     .stApp {
#         background-color: #f8f9fa;
#     }
    
#     .stSidebar {
#         background-color: #ffffff;
#         border-right: 1px solid #e6e6e6;
#     }
    
#     /* Style des cartes */
#     .card {
#         background-color: white;
#         border-radius: 10px;
#         padding: 1.5rem;
#         box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
#         margin-bottom: 1rem;
#         border-top: 4px solid #1a73e8;
#     }
    
#     /* Style des en-têtes */
#     h1 {
#         color: #212121;
#         font-weight: 600;
#         margin-bottom: 1rem;
#         font-size: 2rem;
#         padding-bottom: 0.5rem;
#         border-bottom: 1px solid #f0f0f0;
#     }
    
#     h2, h3 {
#         color: #424242;
#         font-weight: 500;
#     }
    
#     /* Style des métriques */
#     div[data-testid="stMetric"] {
#         background-color: white;
#         border-radius: 10px;
#         padding: 1rem;
#         box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
#         transition: transform 0.2s ease;
#     }
    
#     div[data-testid="stMetric"]:hover {
#         transform: translateY(-3px);
#     }
    
#     div[data-testid="stMetricLabel"] {
#         font-size: 0.9rem !important;
#         font-weight: 500 !important;
#     }
    
#     div[data-testid="stMetricValue"] {
#         font-size: 1.8rem !important;
#         font-weight: 600 !important;
#         color: #1a73e8;
#     }
    
#     /* Style des boutons */
#     .stButton>button {
#         background-color: #1a73e8;
#         color: white;
#         border-radius: 6px;
#         padding: 0.5rem 1rem;
#         font-weight: 500;
#         border: none;
#         transition: all 0.3s ease;
#     }
    
#     .stButton>button:hover {
#         background-color: #0d47a1;
#         box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#     }
    
#     /* Style des filtres */
#     .stSelectbox, .stMultiSelect {
#         background-color: white;
#         border-radius: 6px;
#         padding: 0.5rem;
#         box-shadow: 0 1px 6px rgba(0, 0, 0, 0.05);
#         margin-bottom: 1rem;
#     }
    
#     /* Style des graphiques */
#     div[data-testid="stDecoration"] {
#         background-color: white;
#         border-radius: 10px;
#         padding: 1rem;
#         box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
#     }
    
#     /* Info banners */
#     div[data-testid="stAlert"] {
#         border-radius: 8px;
#         font-size: 0.9rem;
#     }
    
#     /* Animation de transition */
#     @keyframes fadeIn {
#         0% { opacity: 0; transform: translateY(10px); }
#         100% { opacity: 1; transform: translateY(0); }
#     }
    
#     .dashboard-container {
#         animation: fadeIn 0.5s ease forwards;
#     }
    
#     /* Palette de couleurs pour les graphiques */
#     .custom-plot {
#         --color-primary: #1a73e8;
#         --color-secondary: #00bcd4;
#         --color-success: #4caf50;
#         --color-warning: #ff9800;
#         --color-error: #f44336;
#     }
    
#     /* Style des onglets */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 2px;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         background-color: #f3f4f6;
#         border-radius: 4px 4px 0px 0px;
#         padding: 10px 16px;
#         transition: all 0.2s ease;
#     }
    
#     .stTabs [aria-selected="true"] {
#         background-color: #1a73e8 !important;
#         color: white !important;
#     }
    
#     /* Style pour la boîte des pourcentages */
#     .percentage-box {
#         background-color: rgba(255, 255, 255, 0.9);
#         padding: 10px 15px;
#         border-radius: 8px;
#         border: 1px solid #e0e0e0;
#         margin-bottom: 15px;
#         text-align: center;
#         font-size: 14px;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Vérifier si l'utilisateur est connecté
# if 'logged_in' not in st.session_state or not st.session_state.logged_in:
#     st.warning("⚠️ Vous devez vous connecter pour accéder à cette page.")
#     st.info("Retournez à la page d'accueil pour vous connecter.")
#     st.stop()

# # En-tête de la page avec animation
# st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
# st.markdown(f"""
# <div style="display: flex; align-items: center; margin-bottom: 1rem;">
#     <h1 style="margin: 0; font-size: 2rem;">
#         <span style="color: #1a73e8; margin-right: 10px;">📊</span> 
#         Tableau de bord d'adhérence
#     </h1>
#     <div style="margin-left: auto; padding: 8px 15px; background-color: #e8f0fe; border-radius: 30px; display: flex; align-items: center;">
#         <span style="color: #1a73e8; margin-right: 8px;">👤</span>
#         <span style="font-weight: 500;">{st.session_state.username}</span>
#         <span style="margin: 0 5px; color: #949494;">|</span>
#         <span style="color: #666; font-size: 0.9rem;">{st.session_state.role}</span>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Barre de navigation
# col1, col2, col3 = st.columns([1, 1, 1])
# with col1:
#     if st.session_state.role == "admin" and st.button("👑 Administration"):
#         st.switch_page("pages/Admin.py")
        
# with col2:
#     if st.button("📈 Real Time Adherence"):
#         st.switch_page("pages/Real_Time_Adherence.py")
        
# with col3:
#     if st.button("🚪 Déconnexion"):
#         st.session_state.logged_in = False
#         st.session_state.username = ""
#         st.session_state.role = ""
#         st.switch_page("Home.py")

# # Ligne de séparation
# st.markdown('<hr style="margin: 1rem 0; border: none; height: 1px; background-color: #e0e0e0;">', unsafe_allow_html=True)

# # Fonction pour charger les données
# @st.cache_data(ttl=600)
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
        
#         # Récupérer toutes les feuilles du classeur
#         all_worksheets = spreadsheet.worksheets()
        
#         # Liste pour stocker tous les DataFrames
#         all_dfs = []
        
#         # Pour chaque feuille, récupérer les données
#         for worksheet in all_worksheets:
#             sheet_name = worksheet.title
            
#             # Récupérer les données
#             all_data = worksheet.get_all_records()
            
#             # Vérifier si la feuille contient des données
#             if all_data:
#                 # Créer un DataFrame
#                 df = pd.DataFrame(all_data)
                
#                 # Ajouter le nom de la feuille comme colonne pour identification
#                 df['source_sheet'] = sheet_name
                
#                 # S'assurer que la colonne Date est au format datetime
#                 if 'Date' in df.columns:
#                     try:
#                         df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
#                     except:
#                         st.warning(f"Problème de conversion de date dans la feuille {sheet_name}")
                
#                 # Conversion des durées
#                 time_cols = ['Prod', 'Pause_planning', 'Lunch', 'Pause_realise', 'prod_realise']
#                 for col in time_cols:
#                     if col in df.columns:
#                         try:
#                             df[col] = pd.to_timedelta(df[col]).dt.total_seconds()
#                         except:
#                             # Si erreur, continuer sans bloquer
#                             pass
                
#                 # Ajouter le DataFrame à la liste
#                 all_dfs.append(df)
        
#         # Combiner tous les DataFrames
#         if all_dfs:
#             df_combined = pd.concat(all_dfs, ignore_index=True)
#             return df_combined
#         else:
#             st.warning("Aucune donnée n'a été trouvée dans les feuilles du classeur.")
#             return pd.DataFrame()
            
#     except Exception as e:
#         st.error(f"Erreur lors du chargement des données : {e}")
#         return pd.DataFrame()

# # Charger les données
# with st.spinner("Chargement des données..."):
#     data = load_data()

# # Vérifier si les données sont chargées correctement
# if data.empty:
#     st.warning("Aucune donnée n'a été chargée. Vérifiez la connexion à Google Sheets.")
# else:
#     # Section des filtres dans la sidebar
#     st.sidebar.markdown("""
#     <div style="background-color: #1a73e8; padding: 10px; border-radius: 8px; color: white; text-align: center; margin-bottom: 20px; font-weight: 600;">
#         FILTRES
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Obtenir les dates uniques des données
#     unique_dates = sorted(data['Date'].dt.date.unique())
    
#     # Sélecteur de date de début parmi les dates uniques
#     st.sidebar.markdown("### Période d'analyse")
#     start_date_index = st.sidebar.selectbox(
#         "Date de début",
#         options=range(len(unique_dates)),
#         format_func=lambda x: unique_dates[x].strftime('%d/%m/%Y'),
#         index=0
#     )
#     start_date = unique_dates[start_date_index]
    
#     # Sélecteur de date de fin
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
    
#     # Filtres additionnels avec séparateurs visuels
#     st.sidebar.markdown('<div style="margin: 15px 0; height: 1px; background: #e0e0e0;"></div>', unsafe_allow_html=True)
#     st.sidebar.markdown("### Filtres additionnels")
    
#     # Extraction et sélection des tranches horaires
#     tranche_values = []
#     for tranche in filtered_data['Tranche'].dropna().unique():
#         if ':' in str(tranche):
#             heure = tranche.split(' ')[-1] if ' ' in str(tranche) else tranche
#             tranche_values.append(heure)
    
#     unique_tranches = sorted(set(tranche_values))
#     if unique_tranches:
#         selected_tranches = st.sidebar.multiselect(
#             "Tranches horaires",
#             options=unique_tranches,
#             default=None,
#             placeholder="Sélectionnez une ou plusieurs tranches horaires"
#         )
        
#         if selected_tranches:
#             tranche_filter = filtered_data['Tranche'].astype(str).apply(
#                 lambda x: any(tranche in x for tranche in selected_tranches)
#             )
#             filtered_data = filtered_data[tranche_filter]
    
#     # Autres filtres
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
    
#     # Bouton de rafraîchissement des données
#     st.sidebar.markdown('<div style="margin: 15px 0; height: 1px; background: #e0e0e0;"></div>', unsafe_allow_html=True)
#     if st.sidebar.button("🔄 Rafraîchir les données"):
#         st.cache_data.clear()
#         st.rerun()
    
#     # Afficher un résumé des filtres appliqués
#     filter_info = []
#     if start_date == end_date:
#         filter_info.append(f"Date: {start_date.strftime('%d/%m/%Y')}")
#     else:
#         filter_info.append(f"Période: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")
    
#     if selected_tranches:
#         filter_info.append(f"Tranches: {', '.join(selected_tranches)}")
#     if files:
#         filter_info.append(f"Files: {', '.join(files)}")
#     if tls:
#         filter_info.append(f"TLS: {', '.join(tls)}")
#     if ops:
#         filter_info.append(f"OPS: {', '.join(ops)}")
    
#     # Vérifier si des données existent après filtrage
#     if filtered_data.empty:
#         st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
#     else:
#         # Afficher les filtres appliqués
#         st.info(f"📌 Filtres appliqués: {' | '.join(filter_info)}")
        
#         # Affichage des KPIs en haut de la page
#         st.markdown("## Indicateurs clés de performance")
        
#         # Calculer les KPIs
#         agent_adherence = filtered_data.groupby('Nom Agent')['Adherence'].apply(
#             lambda x: x.str.rstrip('%').astype(float).mean()
#         )
#         avg_adherence = agent_adherence.mean()
#         num_agents = filtered_data['Nom Agent'].nunique()
#         num_days = filtered_data['Date'].dt.date.nunique()
#         agents_above_90 = (agent_adherence >= 90).sum()
#         total_agents = len(agent_adherence)
#         good_adherence_percent = (agents_above_90 / total_agents) * 100 if total_agents > 0 else 0
        
#         # Afficher les KPIs dans des cartes modernes
#         kpi_cols = st.columns(4)
#         with kpi_cols[0]:
#             st.metric(
#                 label="Adhérence Moyenne",
#                 value=f"{avg_adherence:.2f}%",
#                 delta=None
#             )
        
#         with kpi_cols[1]:
#             st.metric(
#                 label="Nombre d'Agents",
#                 value=num_agents,
#                 delta=None
#             )
        
#         with kpi_cols[2]:
#             st.metric(
#                 label="Période Analysée",
#                 value=f"{num_days} jours",
#                 delta=None
#             )
        
#         with kpi_cols[3]:
#             st.metric(
#                 label="Agents avec ≥90% Adhérence",
#                 value=f"{good_adherence_percent:.2f}%",
#                 delta=None
#             )
        
#         # Graphiques du dashboard dans des sections distinctes
#         st.markdown("## Analyse de l'Adhérence")
        
#         # Première ligne de graphiques
#         graph_cols1 = st.columns(2)
        
#         with graph_cols1[0]:
#             # Graphique 1: Évolution de l'adhérence dans le temps
#             st.markdown("---")
#             st.subheader("Évolution de l'Adhérence")
            
#             # Préparation des données
#             adherence_by_date_agent = filtered_data.groupby([filtered_data['Date'].dt.date, 'Nom Agent'])['Adherence'].apply(
#                 lambda x: x.str.rstrip('%').astype(float).mean()
#             ).reset_index()
            
#             adherence_by_date = adherence_by_date_agent.groupby('Date')['Adherence'].mean().reset_index()
#             adherence_by_date.columns = ['Date', 'Adhérence Moyenne']
            
#             # Graphique avec style amélioré
#             fig = px.line(
#                 adherence_by_date, 
#                 x='Date', 
#                 y='Adhérence Moyenne',
#                 markers=True,
#                 line_shape='linear'
#             )
#             fig.update_layout(
#                 yaxis_range=[0, 100],
#                 title=None,
#                 plot_bgcolor='rgba(0,0,0,0)',
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 font=dict(family="Poppins, sans-serif"),
#                 margin=dict(l=10, r=10, t=10, b=10),
#                 hovermode="x unified",
#                 xaxis=dict(
#                     title="Date",
#                     gridcolor='rgba(211,211,211,0.3)',
#                     tickformat='%d/%m/%Y'
#                 ),
#                 yaxis=dict(
#                     title="Adhérence Moyenne (%)",
#                     gridcolor='rgba(211,211,211,0.3)'
#                 )
#             )
#             fig.update_traces(
#                 line_color='#1a73e8',
#                 marker=dict(size=8, color='#0d47a1')
#             )
#             # Ajouter ligne de référence à 90%
#             fig.add_hline(
#                 y=90, 
#                 line_dash="dash", 
#                 line_color="#4caf50",
#                 annotation_text="Objectif 90%",
#                 annotation_position="top right"
#             )
#             st.plotly_chart(fig, use_container_width=True)
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         with graph_cols1[1]:
#             # Graphique 2: Distribution de l'adhérence
#             st.markdown("---")
#             st.subheader("Distribution de l'Adhérence")
            
#             # Créer des tranches d'adhérence
#             bins = [0, 70, 80, 90, 100]
#             labels = ['<70%', '70-80%', '80-90%', '≥90%']
#             adherence_bins = pd.cut(agent_adherence, bins=bins, labels=labels)
            
#             # Compter le nombre d'agents dans chaque tranche
#             adherence_counts = adherence_bins.value_counts().reset_index()
#             adherence_counts.columns = ['Tranche', 'Nombre']
            
#             # Couleurs selon la tranche avec une palette moderne
#             colors = {
#                 '<70%': '#f44336',  # Rouge
#                 '70-80%': '#ff9800',  # Orange
#                 '80-90%': '#ffc107',  # Jaune
#                 '≥90%': '#4caf50'   # Vert
#             }
            
#             # Créer le graphique avec style amélioré
#             fig = px.bar(
#                 adherence_counts,
#                 x='Tranche',
#                 y='Nombre',
#                 color='Tranche',
#                 color_discrete_map=colors,
#                 text='Nombre'
#             )
#             fig.update_layout(
#                 title=None,
#                 plot_bgcolor='rgba(0,0,0,0)',
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 font=dict(family="Poppins, sans-serif"),
#                 margin=dict(l=10, r=10, t=10, b=10),
#                 xaxis=dict(
#                     title="Niveau d'adhérence",
#                     gridcolor='rgba(211,211,211,0.3)'
#                 ),
#                 yaxis=dict(
#                     title="Nombre d'agents",
#                     gridcolor='rgba(211,211,211,0.3)'
#                 ),
#                 legend_title_text=None
#             )
#             fig.update_traces(textposition='outside')
#             st.plotly_chart(fig, use_container_width=True)
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         # Deuxième ligne de graphiques
#         graph_cols2 = st.columns(2)
        
#         with graph_cols2[0]:
#             # Graphique 3: Top 10 meilleurs agents en adhérence
#             st.markdown("---")
#             st.subheader("Top 10 - Meilleure Adhérence")
            
#             # Préparation des données
#             agent_adherence_df = agent_adherence.reset_index()
#             agent_adherence_df.columns = ['Nom Agent', 'Adhérence Moyenne']
            
#             # Trier et prendre les 10 meilleurs
#             top_agents = agent_adherence_df.sort_values('Adhérence Moyenne', ascending=False).head(10)
            
#             # Graphique avec style amélioré
#             fig = px.bar(
#                 top_agents,
#                 x='Adhérence Moyenne',
#                 y='Nom Agent',
#                 orientation='h',
#                 text='Adhérence Moyenne',
#                 color='Adhérence Moyenne',
#                 color_continuous_scale=[(0, '#ff9800'), (0.5, '#8bc34a'), (1, '#4caf50')]
#             )
#             fig.update_layout(
#                 title=None,
#                 plot_bgcolor='rgba(0,0,0,0)',
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 font=dict(family="Poppins, sans-serif"),
#                 margin=dict(l=10, r=10, t=10, b=10),
#                 xaxis=dict(
#                     title="Adhérence Moyenne (%)",
#                     range=[0, 100],
#                     gridcolor='rgba(211,211,211,0.3)'
#                 ),
#                 yaxis=dict(
#                     title=None,
#                     autorange="reversed"
#                 ),
#                 coloraxis_showscale=False
#             )
#             fig.update_traces(
#                 texttemplate='%{text:.2f}%', 
#                 textposition='outside',
#                 marker_line_width=0
#             )
#             st.plotly_chart(fig, use_container_width=True)
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         with graph_cols2[1]:
#             # Graphique 4: Adhérence moyenne par File
#             st.markdown("---")
#             st.subheader("Adhérence par File")
            
#             # Préparation des données
#             file_agent_adherence = filtered_data.groupby(['File', 'Nom Agent'])['Adherence'].apply(
#                 lambda x: x.str.rstrip('%').astype(float).mean()
#             ).reset_index()
            
#             file_adherence = file_agent_adherence.groupby('File')['Adherence'].mean().reset_index()
#             file_adherence.columns = ['File', 'Adhérence Moyenne']
#             file_adherence = file_adherence.sort_values('Adhérence Moyenne', ascending=False)
            
#             # Graphique avec style amélioré
#             fig = px.bar(
#                 file_adherence,
#                 x='File',
#                 y='Adhérence Moyenne',
#                 text='Adhérence Moyenne',
#                 color='Adhérence Moyenne',
#                 color_continuous_scale=[(0, '#ff9800'), (0.5, '#8bc34a'), (1, '#4caf50')]
#             )
#             fig.update_layout(
#                 title=None,
#                 plot_bgcolor='rgba(0,0,0,0)',
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 font=dict(family="Poppins, sans-serif"),
#                 margin=dict(l=10, r=10, t=10, b=10),
#                 xaxis=dict(
#                     title="File",
#                     tickangle=45,
#                     gridcolor='rgba(211,211,211,0.3)'
#                 ),
#                 yaxis=dict(
#                     title="Adhérence Moyenne (%)",
#                     range=[0, 100],
#                     gridcolor='rgba(211,211,211,0.3)'
#                 ),
#                 coloraxis_showscale=False
#             )
#             fig.update_traces(
#                 texttemplate='%{text:.2f}%', 
#                 textposition='outside',
#                 marker_line_width=0
#             )
#             fig.add_hline(
#                 y=90, 
#                 line_dash="dash", 
#                 line_color="#4caf50",
#                 annotation_text="Objectif 90%",
#                 annotation_position="top right"
#             )
#             st.plotly_chart(fig, use_container_width=True)
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         # Troisième ligne de graphiques
#         graph_cols3 = st.columns(2)
        
#         with graph_cols3[0]:
#             # Graphique 3: Top 10 agents avec adhérence la plus faible
#             st.markdown("---")
#             st.subheader("10 Agents - Adhérence la Plus Faible")
            
#             # Préparation des données
#             agent_adherence_df = agent_adherence.reset_index()
#             agent_adherence_df.columns = ['Nom Agent', 'Adhérence Moyenne']
            
#             # Trier et prendre les 10 plus faibles (au lieu des 10 meilleurs)
#             bottom_agents = agent_adherence_df.sort_values('Adhérence Moyenne', ascending=True).head(10)
            
#             # Graphique avec style amélioré et couleurs adaptées pour indiquer des scores faibles
#             fig = px.bar(
#                 bottom_agents,
#                 x='Adhérence Moyenne',
#                 y='Nom Agent',
#                 orientation='h',
#                 text='Adhérence Moyenne',
#                 color='Adhérence Moyenne',
#                 # Palette de couleurs inversée pour indiquer les performances faibles
#                 color_continuous_scale=[(0, '#f44336'), (0.5, '#ff9800'), (1, '#ffc107')]
#             )
#             fig.update_layout(
#                 title=None,
#                 plot_bgcolor='rgba(0,0,0,0)',
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 font=dict(family="Poppins, sans-serif"),
#                 margin=dict(l=10, r=10, t=10, b=10),
#                 xaxis=dict(
#                     title="Adhérence Moyenne (%)",
#                     range=[0, 100],
#                     gridcolor='rgba(211,211,211,0.3)'
#                 ),
#                 yaxis=dict(
#                     title=None,
#                     autorange="reversed"
#                 ),
#                 coloraxis_showscale=False
#             )
#             fig.update_traces(
#                 texttemplate='%{text:.2f}%', 
#                 textposition='outside',
#                 marker_line_width=0
#             )
            
#             # Ajout d'une ligne de seuil pour indiquer l'objectif de 90%
#             fig.add_vline(
#                 x=90,
#                 line_dash="dash", 
#                 line_color="#4caf50",
#                 annotation_text="Objectif 90%",
#                 annotation_position="top"
#             )
            
#             st.plotly_chart(fig, use_container_width=True)
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         with graph_cols3[1]:
#             # Graphique 6: Répartition des temps par type
#             st.markdown("---")
#             st.subheader("Répartition des Temps de Travail")
            
#             # Préparation des données
#             agent_times = filtered_data.groupby('Nom Agent').agg({
#                 'Prod': 'sum',
#                 'Pause_planning': 'sum',
#                 'Lunch': 'sum',
#                 'prod_realise': 'sum',
#                 'Pause_realise': 'sum'
#             }).reset_index()
            
#             # Calculer les totaux
#             total_prod_planning = agent_times['Prod'].sum()
#             total_pause_planning = agent_times['Pause_planning'].sum()
#             total_lunch_planning = agent_times['Lunch'].sum()
#             total_prod_realise = agent_times['prod_realise'].sum()
#             total_pause_realise = agent_times['Pause_realise'].sum()
            
#             # Calculer le temps de lunch réalisé
#             total_time_planning = total_prod_planning + total_pause_planning + total_lunch_planning
#             total_time_realise = total_prod_realise + total_pause_realise
#             total_lunch_realise = total_time_planning - total_time_realise if total_time_realise < total_time_planning else 0
            
#             # Préparer les données pour le graphique
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
            
#             time_data = pd.concat([planning_data, realise_data])
            
#             # Calculer les pourcentages
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
            
#             # Afficher les pourcentages en HTML avant le graphique
#             st.markdown(f"""
#             <div class="percentage-box">
#                 <p style="margin: 0;">
#                     <b>Prévu:</b> Production {prod_planning_pct:.1f}%, Pause {pause_planning_pct:.1f}%, Déjeuner {lunch_planning_pct:.1f}%<br>
#                     <b>Réalisé:</b> Production {prod_realise_pct:.1f}%, Pause {pause_realise_pct:.1f}%, Déjeuner {lunch_realise_pct:.1f}%
#                 </p>
#             </div>
#             """, unsafe_allow_html=True)
            
#             # Couleurs modernes pour les catégories
#             colors = {
#                 'Production': '#1a73e8',  # Bleu
#                 'Pause': '#00bcd4',       # Turquoise
#                 'Déjeuner': '#ff9800'     # Orange
#             }
            
#             # Graphique avec style amélioré
#             fig = px.bar(
#                 time_data,
#                 x='Type',
#                 y='Temps (heures)',
#                 color='Catégorie',
#                 barmode='group',
#                 color_discrete_map=colors,
#                 text='Temps (heures)'
#             )
#             fig.update_layout(
#                 title=None,
#                 plot_bgcolor='rgba(0,0,0,0)',
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 font=dict(family="Poppins, sans-serif"),
#                 margin=dict(l=10, r=10, t=10, b=10),
#                 xaxis=dict(
#                     title=None,
#                     gridcolor='rgba(211,211,211,0.3)'
#                 ),
#                 yaxis=dict(
#                     title="Durée (heures)",
#                     gridcolor='rgba(211,211,211,0.3)'
#                 ),
#                 legend_title=None
#             )
#             fig.update_traces(texttemplate='%{text:.1f}h', textposition='outside')
            
#             # Pas d'annotation dans le graphique, car nous avons déjà affiché les pourcentages en HTML
            
#             st.plotly_chart(fig, use_container_width=True)
#             st.markdown('</div>', unsafe_allow_html=True)
        
        
        
# st.markdown('</div>', unsafe_allow_html=True)  # Fermeture du container principal






#####################################code final de rta ################################
import streamlit as st
import gspread
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuration de la page
st.set_page_config(
    page_title="Real Time Adherence",
    page_icon="📈",
    layout="wide"
)
# The function I'm adding will convert time strings like "00:14:35" to seconds
def time_to_seconds(time_str):
    if not time_str or time_str == "":
        return 0
    try:
        # Split the time string into hours, minutes, and seconds
        hours, minutes, seconds = time_str.split(':')
        # Convert to total seconds
        total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        return total_seconds
    except:
        return 0

# The function to format seconds back to a readable time format (HH:MM:SS)
def seconds_to_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}h {minutes:02d}min {secs:02d}sec"
# CSS personnalisé pour améliorer l'apparence
st.markdown("""
<style>
    /* Styles globaux */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Fond global */
    .stApp {
        background: linear-gradient(140deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Style de la sidebar */
    section[data-testid="stSidebar"] {
        background-color: #fff;
        border-right: 1px solid rgba(0, 0, 0, 0.08);
    }
    
    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
    }
    
    /* Style des cartes */
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Style des en-têtes */
    h1 {
        color: #212121;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 2rem;
    }
    
    h2, h3 {
        color: #424242;
        font-weight: 500;
    }
    
    /* Style des boutons */
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        border-radius: 25px;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #0d47a1;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Style des selects et filters */
    .stSelectbox, .stMultiSelect {
        background-color: white;
        border-radius: 8px;
        padding: 0.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    /* Style des alertes et messages */
    div[data-testid="stAlert"] {
        border-radius: 8px;
        font-size: 0.9rem;
    }
    
    /* Style des panneaux d'agent */
    .agent-container {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border-left: 4px solid #1a73e8;
    }
    
    .agent-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    .agent-header {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .agent-name {
        font-weight: 600;
        font-size: 16px;
        color: #212121;
    }
    
    .agent-meta {
        color: #757575;
        font-size: 13px;
        margin-top: 3px;
    }
    
    .adherence-value {
        font-size: 24px;
        font-weight: 600;
        text-align: center;
    }
    
    .high-adherence {
        color: #4caf50;
    }
    
    .low-adherence {
        color: #f44336;
    }
    
    /* Style de la légende */
    .legend-container {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        margin: 0 0 20px 0;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
    }
    
    .legend-item {
        display: flex;
        align-items: center;
        margin: 5px;
    }
    
    .legend-color {
        width: 16px;
        height: 16px;
        border-radius: 4px;
        margin-right: 6px;
    }
    
    .legend-label {
        font-size: 14px;
        color: #424242;
    }
    
    /* Animation de transition */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .dashboard-container {
        animation: fadeIn 0.5s ease forwards;
    }
    
    /* Style pour les titres de section dans la sidebar */
    .sidebar-section-title {
        background-color: #f5f7fa;
        padding: 8px 15px;
        border-radius: 8px;
        font-weight: 500;
        color: #424242;
        margin: 15px 0 10px 0;
        font-size: 14px;
        border-left: 3px solid #1a73e8;
    }
</style>
""", unsafe_allow_html=True)

# Vérifier si l'utilisateur est connecté
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Vous devez vous connecter pour accéder à cette page.")
    st.info("Retournez à la page d'accueil pour vous connecter.")
    st.stop()

# Container principal avec animation
st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)

# En-tête de la page avec style
st.markdown(f"""
<div style="display: flex; align-items: center; margin-bottom: 1rem;">
    <div style="display: flex; align-items: center;">
        <div style="font-size: 2.5rem; margin-right: 10px; color: #00bcd4;">📈</div>
        <h1 style="margin: 0; font-size: 2rem;">Real Time Adherence</h1>
    </div>
    <div style="margin-left: auto; padding: 8px 15px; background-color: #e0f7fa; border-radius: 30px; display: flex; align-items: center;">
        <span style="color: #00bcd4; margin-right: 8px;">👤</span>
        <span style="font-weight: 500;">{st.session_state.username}</span>
        <span style="margin: 0 5px; color: #949494;">|</span>
        <span style="color: #666; font-size: 0.9rem;">{st.session_state.role}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Barre de navigation
nav_cols = st.columns(3)
with nav_cols[0]:
    if st.button("📊 Dashboard"):
        st.switch_page("pages/Dashboard.py")

with nav_cols[1]:
    if st.session_state.role == "admin" and st.button("👑 Administration"):
        st.switch_page("pages/Admin.py")

with nav_cols[2]:
    if st.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.switch_page("Home.py")

# Ligne de séparation
st.markdown('<hr style="margin: 1rem 0; border: none; height: 1px; background-color: #e0e0e0;">', unsafe_allow_html=True)

# 2. Connexion à Google Sheets
@st.cache_resource(ttl=600)
def get_google_client():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    return gspread.authorize(creds)

# 3. Charger les données
@st.cache_data(ttl=300)
def load_data():
    try:
        client = get_google_client()
        # Ouvrir le classeur Google Sheets
        spreadsheet = client.open("mydata")
        
        # Récupérer toutes les feuilles du classeur
        all_worksheets = spreadsheet.worksheets()
        
        # Liste pour stocker tous les DataFrames
        all_dfs = []
        
        # Pour chaque feuille, récupérer les données
        for worksheet in all_worksheets:
            # Obtenir le nom de la feuille pour le debug
            sheet_name = worksheet.title
            
            # Récupérer les données
            all_data = worksheet.get_all_records()
            
            # Vérifier si la feuille contient des données
            if all_data:
                # Créer un DataFrame
                df = pd.DataFrame(all_data)
                
                # S'assurer que la colonne Date est au format datetime
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
                
                # Conversion des durées
                time_cols = ['Prod', 'Pause_planning', 'Lunch', 'Pause_realise', 'prod_realise']
                for col in time_cols:
                    if col in df.columns:
                        try:
                            df[col] = pd.to_timedelta(df[col]).dt.total_seconds()
                        except:
                            # En cas d'erreur, on continue sans arrêter le programme
                            st.warning(f"Impossible de convertir la colonne {col} dans la feuille {sheet_name}")
                
                # Ajouter le DataFrame à la liste
                all_dfs.append(df)
        
        # Combiner tous les DataFrames
        if all_dfs:
            combined_df = pd.concat(all_dfs, ignore_index=True)
            return combined_df
        else:
            st.warning("Aucune donnée trouvée dans les feuilles")
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return pd.DataFrame()

# Charger les données avec un spinner
with st.spinner("Chargement des données..."):
    df_combined = load_data()

# Configuration de la sidebar
st.sidebar.markdown("""
<div style="text-align: center; padding: 12px 0; margin-bottom: 20px; background: linear-gradient(90deg, #1a73e8 0%, #00bcd4 100%); color: white; border-radius: 8px; font-weight: 500; font-size: 16px;">
    FILTRES
</div>
""", unsafe_allow_html=True)

# Section de sélection de date
if not df_combined.empty and 'Date' in df_combined.columns:
    # Obtenir les dates uniques des deux dataframes
    all_dates = sorted(df_combined['Date'].unique())
    
    # Formater les dates pour l'affichage
    date_options = [date.strftime('%d/%m/%Y') for date in all_dates]
    date_options = [""] + date_options 
    
    st.sidebar.markdown('<div class="sidebar-section-title">Date</div>', unsafe_allow_html=True)
    
    selected_date = st.sidebar.selectbox(
        "Sélectionner une date",
        options=date_options,
        index=0,
        format_func=lambda x: "Sélectionnez une date" if x == "" else x
    )
    
    if selected_date == "":
        # Si aucune date n'est sélectionnée, afficher un message
        st.sidebar.warning("⚠️ Veuillez sélectionner une date pour afficher les données.")
        date_selected = False
        # Initialiser des listes vides pour les filtres
        selected_files = []
        selected_tlss = []
        selected_ops = []
        min_adherence = 0
        max_adherence = 100
    else:
        # Si une date est sélectionnée, filtrer les données et afficher les filtres
        selected_date_dt = pd.to_datetime(selected_date, format='%d/%m/%Y')
        df = df_combined[df_combined['Date'] == selected_date_dt]
        st.sidebar.success(f"📅 Données du {selected_date}")
        date_selected = True
        
        # Récupérer les valeurs uniques pour chaque filtre à partir des données filtrées par date
        all_files = sorted(df['File'].dropna().unique().tolist())
        all_tlss = sorted(df['Tls'].dropna().unique().tolist())
        all_ops = sorted(df['OPS'].dropna().unique().tolist())

        # Séparateur
        st.sidebar.markdown('<div class="sidebar-section-title">Filtres Additionnels</div>', unsafe_allow_html=True)
        
        # Filtres améliorés
        selected_files = st.sidebar.multiselect(
            "🏢 File",
            options=all_files,
            default=None,
            placeholder="Sélectionnez une ou plusieurs files"
        )

        selected_tlss = st.sidebar.multiselect(
            "👨‍💼 TLS",
            options=all_tlss,
            default=None,
            placeholder="Sélectionnez un ou plusieurs TLS"
        )

        selected_ops = st.sidebar.multiselect(
            "🔧 OPS",
            options=all_ops,
            default=None,
            placeholder="Sélectionnez un ou plusieurs OPS"
        )
        
        # Ajouter un séparateur pour le filtre de recherche par nom d'agent
        st.sidebar.markdown('<div class="sidebar-section-title">Recherche par Nom d\'Agent</div>', unsafe_allow_html=True)

        # Récupérer la liste des noms d'agents pour l'autocomplétion
        all_agents = sorted(df['Nom Agent'].dropna().unique().tolist())

        # Créer une zone de texte pour rechercher un agent
        agent_search = st.sidebar.text_input(
            "🔍 Rechercher un agent",
            value="",
            placeholder="Entrez le nom de l'agent"
        )

        # Offrir des suggestions d'agents dont le nom contient la recherche (autocomplétion)
        if agent_search and len(agent_search) >= 2:  # Commencer les suggestions après 2 caractères
            matching_agents = [agent for agent in all_agents if agent_search.lower() in agent.lower()]
            
            if matching_agents:
                selected_agent = st.sidebar.selectbox(
                    "Agents correspondants",
                    options=matching_agents,
                    format_func=lambda x: x,
                    key="agent_suggestion"
                )
                
                # Bouton pour filtrer par cet agent
                if st.sidebar.button("Afficher cet agent"):
                    # Stocke l'agent sélectionné dans une variable de session
                    st.session_state.selected_agent_name = selected_agent
            elif agent_search:  # Si la recherche ne correspond à aucun agent
                st.sidebar.warning("Aucun agent ne correspond à cette recherche.")
        else:
            # Si le champ est vide, offre une liste complète des agents
            if all_agents:
                # Bouton pour réinitialiser la recherche d'agent
                if 'selected_agent_name' in st.session_state and st.sidebar.button("❌ Réinitialiser la recherche"):
                    # Supprimer l'agent sélectionné de la session
                    if 'selected_agent_name' in st.session_state:
                        del st.session_state.selected_agent_name
                    # Recharger la page
                    st.rerun()


        # Séparateur pour le filtre d'adhérence
        st.sidebar.markdown('<div class="sidebar-section-title">Filtre d\'Adhérence</div>', unsafe_allow_html=True)

        # Créer deux colonnes pour les contrôles min/max
        adh_cols = st.sidebar.columns(2)

        # Définir les valeurs par défaut
        default_min_adherence = 0
        default_max_adherence = 100

        # Créer les sliders pour le minimum et maximum d'adhérence
        with adh_cols[0]:
            min_adherence = st.number_input(
                "Min (%)",
                min_value=0,
                max_value=100,
                value=default_min_adherence,
                step=5
            )

        with adh_cols[1]:
            max_adherence = st.number_input(
                "Max (%)",
                min_value=0,
                max_value=100,
                value=default_max_adherence,
                step=5
            )

        # Assurer que min <= max
        if min_adherence > max_adherence:
            min_adherence, max_adherence = max_adherence, min_adherence
            st.sidebar.warning("Les valeurs min et max ont été inversées.")

        # Afficher la plage sélectionnée
        st.sidebar.markdown(f"""
        <div style="padding: 10px; background-color: #f2f6ff; border-radius: 5px; text-align: center; margin-top: 10px;">
            <span style="font-weight: 500;">Plage: {min_adherence}% - {max_adherence}%</span>
        </div>
        """, unsafe_allow_html=True)
else:
    # Si pas de colonne Date ou dataframe vide
    st.error("⚠️ Aucune donnée n'a été chargée ou la colonne 'Date' est manquante.")
    date_selected = False
    # Initialiser des listes vides pour éviter les erreurs
    selected_files = []
    selected_tlss = []
    selected_ops = []
    min_adherence = 0
    max_adherence = 100
    df = pd.DataFrame()

# Bouton de rafraîchissement
st.sidebar.markdown('<div class="sidebar-section-title">Actions</div>', unsafe_allow_html=True)
if st.sidebar.button("🔄 Rafraîchir les données"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

# Fonction de filtrage améliorée avec filtrage d'adhérence
# Fonction de filtrage améliorée avec filtrage d'adhérence par agent
def apply_filters(data, files=None, tlss=None, ops=None, agent_name=None, min_adherence=0, max_adherence=100):
    filtered = data.copy()
    
    # Appliquer les filtres seulement si des options sont sélectionnées
    if files and len(files) > 0:
        filtered = filtered[filtered['File'].isin(files)]
    if tlss and len(tlss) > 0:
        filtered = filtered[filtered['Tls'].isin(tlss)]
    if ops and len(ops) > 0:
        filtered = filtered[filtered['OPS'].isin(ops)]
    if agent_name:
        filtered = filtered[filtered['Nom Agent'] == agent_name]
    
    # Filtrer par pourcentage d'adhérence MOYENNE PAR AGENT
    if min_adherence > 0 or max_adherence < 100:
        # Calculer l'adhérence moyenne par agent
        agent_adherence = filtered.groupby('Nom Agent')['Adherence'].apply(
            lambda x: x.str.rstrip('%').astype(float).mean()
        )
        
        # Filtrer les agents dont l'adhérence moyenne est dans la plage spécifiée
        agents_in_range = agent_adherence[
            (agent_adherence >= min_adherence) & 
            (agent_adherence <= max_adherence)
        ].index.tolist()
        
        # Appliquer le filtre sur les données
        filtered = filtered[filtered['Nom Agent'].isin(agents_in_range)]
    
    return filtered
# Fonction pour créer les graphiques avec style amélioré
def create_agent_plot(agent_df):
    # Palette de couleurs
    prod_color = "#1a73e8"     # Bleu principal
    pause_color = "#00bcd4"    # Turquoise
    lunch_color = "#ff9800"    # Orange
    adherence_high = "#4caf50" # Vert
    adherence_low = "#f44336"  # Rouge
    deconnexion_color = "#d32f2f"  # Rouge foncé pour la déconnexion
    
    # Créer une figure Plotly avec 3 sous-graphiques
    fig = make_subplots(rows=3, cols=1, 
                        vertical_spacing=0.15,
                        row_heights=[1, 1, 1])
    
    # Définir la hauteur et largeur
    fig.update_layout(height=150, width=500)
    
    # Variable pour suivre la position actuelle
    x_start = 0
    x_end = 0
    
    # Liste pour stocker les heures et les positions
    all_hours = []
    max_time = 0
    
    # Pour chaque ligne dans les données, identifier d'abord toutes les tranches horaires
    for i, row in agent_df.iterrows():
        tranche = row.get('Tranche', '')
        if tranche:
            heure_format = tranche.split(' ')[-1] if ' ' in tranche else tranche
            # Ajouter toutes les heures
            all_hours.append((x_start, heure_format))
        x_start += 900  # 15 minutes = 900 secondes
    
    # Réinitialiser x_start pour la construction des graphiques
    x_start = 0
    max_time = (len(agent_df) * 900) if len(agent_df) > 0 else 0  # Pour calculer la largeur totale
    
    # Préparation des données pour les trois barres
    prev_data = []
    real_data = []
    adh_data = []
    
    # Pour chaque ligne dans les données
    for i, row in agent_df.iterrows():
        # Récupérer la tranche horaire
        tranche = row.get('Tranche', '')
        
        # Calculer la position de fin
        x_end = x_start + 900  # 900 secondes (15 minutes)
        
        # PRÉVU
        if row['Prod'] > 0:
            color = prod_color
            activity = "Production"
        elif row['Pause_planning'] > 0:
            color = pause_color
            activity = "Pause"
        elif row['Lunch'] > 0:
            color = lunch_color
            activity = "Déjeuner"
        else:
            color = "#F7F7F7"
            activity = "Non défini"
        
        prev_data.append({
            'x0': x_start, 
            'x1': x_end, 
            'color': color,
            'activity': activity,
            'tranche': tranche
        })
        
        # RÉALISÉ - Simplifié pour ne stocker que les positions et la tranche
        # Nous n'avons plus besoin de déterminer une couleur dominante ici
        real_data.append({
            'x0': x_start, 
            'x1': x_end, 
            'tranche': tranche
        })
        
        # ADHÉRENCE
        adherence_value = float(str(row['Adherence']).rstrip('%'))
        color = adherence_high if adherence_value >= 90 else adherence_low
        
        adh_data.append({
            'x0': x_start,
            'x1': x_end,
            'color': color,
            'adherence': adherence_value,
            'tranche': tranche
        })
        
        # Mise à jour de la position pour le prochain segment
        x_start = x_end
    
    # Ajouter les rectangles pour PRÉVU
    for segment in prev_data:
        fig.add_shape(
            type="rect",
            x0=segment['x0'], y0=0,
            x1=segment['x1'], y1=1,
            fillcolor=segment['color'],
            line=dict(width=0),
            opacity=0.9,
            row=1, col=1
        )
        # Ajouter des données invisibles pour les tooltips
        fig.add_trace(
            go.Scatter(
                x=[(segment['x0'] + segment['x1']) / 2],
                y=[0.5],
                mode="markers",
                marker=dict(size=0, color="rgba(0,0,0,0)"),
                hoverinfo="text",
                text=f"Tranche: {segment['tranche']}<br>Activité: {segment['activity']}",
                showlegend=False
            ),
            row=1, col=1
        )
    
    # Ajouter les rectangles pour RÉALISÉ (VERSION DÉTAILLÉE)
    for i, segment in enumerate(real_data):
        x0 = segment['x0']
        x1 = segment['x1']
        tranche = segment['tranche']
        
        # Récupérer les valeurs pour cette tranche
        prod_time = agent_df.iloc[i]['prod_realise']
        pause_time = agent_df.iloc[i]['Pause_realise']
        total_realise = prod_time + pause_time
        
        # Récupérer les valeurs du planning pour cette tranche
        lunch_planning = agent_df.iloc[i]['Lunch']
        prod_planning = agent_df.iloc[i]['Prod']
        pause_planning = agent_df.iloc[i]['Pause_planning']
        
        # CAS 1: Aucune activité réalisée (prod_realise et pause_realise sont zéro)
        if total_realise == 0:
            # Sous-cas 1.1: Si un lunch était prévu, c'est un lunch
            if lunch_planning > 0:
                activity = "Déconnexion"  #"Déjeuner"
                segment_color = deconnexion_color
            # Sous-cas 1.2: Si une production ou pause était prévue, c'est une déconnexion
            elif prod_planning > 0 or pause_planning > 0:
                activity = "Déconnexion"
                segment_color = deconnexion_color
            # Sous-cas 1.3: Si rien n'était prévu non plus
            else:
                activity = "Non défini"
                segment_color = "#F7F7F7"  # Gris clair
            
            # Ajouter le segment complet
            fig.add_shape(
                type="rect",
                x0=x0, y0=0,
                x1=x1, y1=1,
                fillcolor=segment_color,
                line=dict(width=0),
                opacity=0.9,
                row=2, col=1
            )
            
            # Tooltip pour le segment
            fig.add_trace(
                go.Scatter(
                    x=[(x0 + x1) / 2],
                    y=[0.5],
                    mode="markers",
                    marker=dict(size=0, color="rgba(0,0,0,0)"),
                    hoverinfo="text",
                    text=f"Tranche: {tranche}<br>Activité: {activity}",
                    showlegend=False
                ),
                row=2, col=1
            )
        
        # CAS 2: Activités réalisées (production et/ou pause)
        else:
            segment_width = x1 - x0
            
            # 2.1. Partie production (si existante)
            if prod_time > 0:
                prod_proportion = prod_time / 900  # 900 secondes = 15 minutes
                prod_width = segment_width * prod_proportion
                
                fig.add_shape(
                    type="rect",
                    x0=x0, y0=0,
                    x1=x0 + prod_width, y1=1,
                    fillcolor=prod_color,
                    line=dict(width=0),
                    opacity=0.9,
                    row=2, col=1
                )
                
                # Tooltip pour la production
                fig.add_trace(
                    go.Scatter(
                        x=[x0 + prod_width/2],
                        y=[0.5],
                        mode="markers",
                        marker=dict(size=0, color="rgba(0,0,0,0)"),
                        hoverinfo="text",
                        text=f"Tranche: {tranche}<br>Production: {int(prod_time/60)} min {int(prod_time%60)} sec",
                        showlegend=False
                    ),
                    row=2, col=1
                )
            
            # 2.2. Partie pause (si existante)
            if pause_time > 0:
                pause_proportion = pause_time / 900
                pause_width = segment_width * pause_proportion
                pause_start = x0 + (prod_time / 900) * segment_width
                
                fig.add_shape(
                    type="rect",
                    x0=pause_start, y0=0,
                    x1=pause_start + pause_width, y1=1,
                    fillcolor=pause_color,
                    line=dict(width=0),
                    opacity=0.9,
                    row=2, col=1
                )
                
                # Tooltip pour la pause
                fig.add_trace(
                    go.Scatter(
                        x=[pause_start + pause_width/2],
                        y=[0.5],
                        mode="markers",
                        marker=dict(size=0, color="rgba(0,0,0,0)"),
                        hoverinfo="text",
                        text=f"Tranche: {tranche}<br>Pause: {int(pause_time/60)} min {int(pause_time%60)} sec",
                        showlegend=False
                    ),
                    row=2, col=1
                )
            
            # 2.3. Partie restante (non utilisée)
            remaining_time = 900 - total_realise
            if remaining_time > 0:
                remaining_proportion = remaining_time / 900
                remaining_width = segment_width * remaining_proportion
                remaining_start = x0 + (total_realise / 900) * segment_width
                
                # Déterminer la couleur pour le temps restant
                if lunch_planning > 0:
                    remaining_color = deconnexion_color #lunch_color
                    remaining_activity = "Déconnexion" #"Déjeuner"
                else:
                    remaining_color = deconnexion_color
                    remaining_activity = "Déconnexion"
                
                fig.add_shape(
                    type="rect",
                    x0=remaining_start, y0=0,
                    x1=remaining_start + remaining_width, y1=1,
                    fillcolor=remaining_color,
                    line=dict(width=0),
                    opacity=0.9,
                    row=2, col=1
                )
                
                # Tooltip pour le temps restant
                fig.add_trace(
                    go.Scatter(
                        x=[remaining_start + remaining_width/2],
                        y=[0.5],
                        mode="markers",
                        marker=dict(size=0, color="rgba(0,0,0,0)"),
                        hoverinfo="text",
                        text=f"Tranche: {tranche}<br>{remaining_activity}: {int(remaining_time/60)} min {int(remaining_time%60)} sec",
                        showlegend=False
                    ),
                    row=2, col=1
                )
    
    # Ajouter les rectangles pour ADHÉRENCE
    for segment in adh_data:
        fig.add_shape(
            type="rect",
            x0=segment['x0'], y0=0,
            x1=segment['x1'], y1=1,
            fillcolor=segment['color'],
            line=dict(width=0),
            opacity=0.9,
            row=3, col=1
        )
        # Ajouter des données invisibles pour les tooltips
        fig.add_trace(
            go.Scatter(
                x=[(segment['x0'] + segment['x1']) / 2],
                y=[0.5],
                mode="markers",
                marker=dict(size=0, color="rgba(0,0,0,0)"),
                hoverinfo="text",
                text=f"Tranche: {segment['tranche']}<br>Adhérence: {segment['adherence']}%",
                showlegend=False
            ),
            row=3, col=1
        )
    
    # Ajouter des lignes verticales pour les heures
    for pos, label in all_hours:
        # Ajouter uniquement des lignes pour les heures pleines ou demi-heures
        if label.endswith(':00') or label.endswith(':30'):
            for row_idx in range(1, 4):
                fig.add_shape(
                    type="line",
                    x0=pos, y0=0,
                    x1=pos, y1=1,
                    line=dict(color="#e0e0e0", width=1, dash="dot"),
                    row=row_idx, col=1
                )
    
    # Filtrer pour n'afficher que quelques heures (pour éviter l'encombrement)
    filtered_hours = []
    for pos, label in all_hours:
        if label.endswith(':00'):  # Afficher toutes les heures pleines
            filtered_hours.append((pos, label))
    
    # Créer les annotations pour les titres à gauche
    title_annotations = [
        dict(
            x=-0.01, 
            y=0.85,  # Position pour le premier graphique
            text="Prévu",
            xref="paper", 
            yref="paper",
            xanchor="right", 
            yanchor="middle",
            showarrow=False,
            font=dict(size=10, color="#424242", family="sans-serif")
        ),
        dict(
            x=-0.01, 
            y=0.5,  # Position pour le deuxième graphique
            text="Réalisé",
            xref="paper", 
            yref="paper",
            xanchor="right", 
            yanchor="middle",
            showarrow=False,
            font=dict(size=10, color="#424242", family="sans-serif")
        ),
        dict(
            x=-0.01, 
            y=0.15,  # Position pour le troisième graphique
            text="Adhérence",
            xref="paper", 
            yref="paper",
            xanchor="right", 
            yanchor="middle",
            showarrow=False,
            font=dict(size=10, color="#424242", family="sans-serif")
        )
    ]
    
    # Créer les annotations pour les heures en haut
    hour_annotations = []
    for pos, label in filtered_hours:
        # Convertir la position en pourcentage de la largeur totale
        x_rel = pos / max_time if max_time > 0 else 0
        
        hour_annotations.append(
            dict(
                x=x_rel,
                y=1,  # Position au-dessus du premier graphique
                text=label,
                showarrow=False,
                xref="x domain", 
                yref="paper",
                xanchor="center",
                yanchor="bottom",
                font=dict(size=8, color="#424242"),
                bgcolor="rgba(255,255,255,0.7)",
                bordercolor="#e0e0e0",
                borderwidth=1,
                borderpad=2
            )
        )
    
    # Mise en page finale
    fig.update_layout(
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#ffffff',
        margin=dict(l=50, r=5, t=25, b=5),
        font=dict(family="sans-serif"),
        showlegend=False,
        hovermode="closest",
        annotations=title_annotations + hour_annotations
    )
    
    # Configurer les axes
    fig.update_xaxes(
        showticklabels=False, 
        showgrid=False, 
        zeroline=False, 
        visible=False,
        range=[0, max_time]  # S'assurer que tous les graphiques ont la même échelle
    )
    
    fig.update_yaxes(
        showticklabels=False, 
        showgrid=False, 
        zeroline=False, 
        visible=False, 
        range=[0, 1]
    )
    
    return fig

# Affichage dans Streamlit
if date_selected:
    # Légende avec design moderne
    st.markdown("""
    <div class="legend-container">
        <div class="legend-item">
            <div class="legend-color" style="background-color: #1a73e8;"></div>
            <div class="legend-label">Production</div>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #00bcd4;"></div>
            <div class="legend-label">Pause</div>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #ff9800;"></div>
            <div class="legend-label">Déjeuner</div>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #d32f2f;"></div>
            <div class="legend-label">Déconnexion</div>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #4caf50;"></div>
            <div class="legend-label">Adhérence ≥ 90%</div>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #f44336;"></div>
            <div class="legend-label">Adhérence < 90%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    selected_agent_name = st.session_state.get('selected_agent_name', None)

    # Appliquer les filtres aux données filtrées par date
    filtered_df = apply_filters(
        df, 
        selected_files, 
        selected_tlss, 
        selected_ops,
        selected_agent_name,  # Ajouter le paramètre pour le nom d'agent
        min_adherence,
        max_adherence
    )
    # Afficher le nombre d'agents après filtrage
    if not filtered_df.empty:
        agent_count = len(filtered_df['Nom Agent'].unique())
        
        # Afficher un résumé des filtres appliqués
        filter_info = []
        filter_info.append(f"Date: {selected_date}")
        
        if selected_files:
            filter_info.append(f"Files: {', '.join(selected_files)}")
        if selected_tlss:
            filter_info.append(f"TLS: {', '.join(selected_tlss)}")
        if selected_ops:
            filter_info.append(f"OPS: {', '.join(selected_ops)}")
        if min_adherence > 0 or max_adherence < 100:
            filter_info.append(f"Adhérence: {min_adherence}% - {max_adherence}%")
        
        # Résumé des filtres avec badge du nombre d'agents
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; background-color: #e3f2fd; padding: 10px 15px; border-radius: 8px; margin-bottom: 20px;">
            <div>📌 <b>Filtres appliqués:</b> {' | '.join(filter_info)}</div>
            <div style="background-color: #1a73e8; color: white; padding: 3px 10px; border-radius: 12px; font-size: 14px;">
                {agent_count} agents
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Afficher la liste des agents avec un style amélioré
        st.markdown("## Adhérence des agent")
        
        # Séparateur entre agents
       # Séparateur entre agents
        for i, agent_name in enumerate(filtered_df['Nom Agent'].unique()):
            agent_data = filtered_df[filtered_df['Nom Agent'] == agent_name]
            
            # Calculer l'adhérence moyenne
            adherence_mean = agent_data['Adherence'].str.rstrip('%').astype(float).mean()
            adherence = f"{adherence_mean:.1f}%"
            adherence_class = "high-adherence" if adherence_mean >= 90 else "low-adherence"
            adherence_color = "#4caf50" if adherence_mean >= 90 else "#f44336"
            
            # AJOUT ICI: Calculer la durée totale de traitement
            total_treatment_seconds = agent_data['Traitement'].apply(time_to_seconds).sum()
            total_treatment_time = seconds_to_time(total_treatment_seconds)
            
            # Calculer le temps de traitement en heures avec décimales
            treatment_hours = total_treatment_seconds / 3600
            
            # Récupérer les métadonnées de l'agent
            file_name = agent_data['File'].iloc[0]
            tls_name = agent_data['Tls'].iloc[0]
            ops_name = agent_data['OPS'].iloc[0]
            
            # Créer le conteneur de l'agent avec colonnes et design amélioré
            with st.container():
                cols = st.columns([2, 6, 1])
        
        # Colonne 1: Infos de l'agent - MODIFIÉE POUR INCLURE LA DURÉE TOTALE DE TRAITEMENT
                with cols[0]:
                    st.markdown(f"""
                    <div style="padding: 15px; background-color: white; border-radius: 10px; height: 100%; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                        <div style="font-weight: 600; font-size: 16px; color: #212121; margin-bottom: 5px;">{agent_name}</div>
                        <div style="font-weight: 500; font-size: 14px; color: #333; margin-bottom: 10px; padding: 5px; background-color: #f2f6ff; border-radius: 5px; border-left: 3px solid #1a73e8;">
                            Temps de traitement: {total_treatment_time} 
                        </div>
                        <div style="color: #757575; font-size: 13px; margin-top: 5px; display: flex; align-items: center;">
                            <div style="width: 8px; height: 8px; background-color: #1a73e8; border-radius: 50%; margin-right: 5px;"></div>
                            File: {file_name}
                        </div>
                        <div style="color: #757575; font-size: 13px; margin-top: 5px; display: flex; align-items: center;">
                            <div style="width: 8px; height: 8px; background-color: #00bcd4; border-radius: 50%; margin-right: 5px;"></div>
                            TLS: {tls_name}
                        </div>
                        <div style="color: #757575; font-size: 13px; margin-top: 5px; display: flex; align-items: center;">
                            <div style="width: 8px; height: 8px; background-color: #ff9800; border-radius: 50%; margin-right: 5px;"></div>
                            OPS: {ops_name}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                # Colonne 2: Visualisation du planning
                with cols[1]:
                    fig = create_agent_plot(agent_data)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Colonne 3: Adhérence
                with cols[2]:
                    st.markdown(f"""
                    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; padding: 15px; background-color: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                        <div style="font-size: 14px; margin-bottom: 8px; color: #757575;">Adhérence</div>
                        <div style="position: relative; width: 70px; height: 70px; margin: 5px 0;">
                            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 50%; background: conic-gradient({adherence_color} 0% {adherence_mean}%, #f3f3f3 {adherence_mean}% 100%);"></div>
                            <div style="position: absolute; top: 5px; left: 5px; width: calc(100% - 10px); height: calc(100% - 10px); border-radius: 50%; background-color: white; display: flex; align-items: center; justify-content: center;">
                                <span style="font-size: 18px; font-weight: 600; color: {adherence_color};">{adherence}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Ajouter un séparateur plus léger entre les agents
            if i < len(filtered_df['Nom Agent'].unique()) - 1:
                st.markdown('<div style="height: 1px; background-color: #f0f0f0; margin: 10px 0;"></div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Aucun agent ne correspond aux critères de filtrage sélectionnés.")
else:
    # Si aucune date n'est sélectionnée, afficher un message d'accueil
    st.markdown("""
    <div style="text-align: center; background-color: white; padding: 40px 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); margin: 20px 0;">
        <div style="font-size: 80px; margin-bottom: 20px;">⏰</div>
        <h2 style="color: #1a73e8; margin-bottom: 20px; font-weight: 600;">Bienvenue sur la visualisation en temps réel</h2>
        <p style="color: #616161; font-size: 16px; margin-bottom: 30px; line-height: 1.6;">
            Cette page vous permet de visualiser l'adhérence des agents en temps réel, avec une représentation graphique 
            de leur planification et de leur activité effective.
        </p>
        <div style="background-color: #f2f6ff; border-left: 4px solid #1a73e8; padding: 15px; border-radius: 5px; text-align: left;">
            <p style="margin: 0; color: #424242; font-size: 15px;">
                <span style="font-weight: 600; color: #1a73e8;">Astuce:</span> 
                Commencez par sélectionner une date dans le menu latéral pour afficher les données des agents.
                Vous pourrez ensuite filtrer par File, TLS ou OPS.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Pied de page
st.markdown("""
<div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #e0e0e0; text-align: center; color: #9e9e9e; font-size: 0.8rem;">
    Système de suivi d'adhérence en temps réel | © 2024 Tous droits réservés
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Fermeture du container principal
