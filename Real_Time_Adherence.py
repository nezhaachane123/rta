# ######################## code final#############################
# # 1. Importer les bibliothèques
# import streamlit as st
# import gspread
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# from oauth2client.service_account import ServiceAccountCredentials
# from datetime import datetime

# # Configuration de la page
# st.set_page_config(
#     page_title="Real Time Adherence",
#     page_icon="📊",
#     layout="wide"
# )
# # Vérifier si l'utilisateur est connecté
# if 'logged_in' not in st.session_state or not st.session_state.logged_in:
#     st.warning("⚠️ Vous devez vous connecter pour accéder à cette page.")
#     st.info("Retournez à la page d'accueil pour vous connecter.")
#     st.stop()

# # Titre de l'application avec icône
# st.title(f"📊 Real Time Adherence- Bienvenue {st.session_state.username}!")


# if st.session_state.role == "admin":
#     if st.button("Page d'Administration"):
#         st.switch_page("pages/Admin.py")

# # Bouton de déconnexion
# if st.button("Déconnexion"):
#     st.session_state.logged_in = False
#     st.session_state.username = ""
#     st.session_state.role = ""
#     st.switch_page("Home.py") 


# # CSS personnalisé pour améliorer l'apparence
# st.markdown("""
# <style>
#     .main .block-container {
#         padding-top: 1rem;
#         padding-bottom: 1rem;
#     }
#     .stApp {
#         background-color: #f9f7f4;
#     }
#     .sidebar .sidebar-content {
#         background-color: #f0ece3;
#     }
#     .agent-container {
#         background-color: white;
#         border-radius: 8px;
#         padding: 15px;
#         margin-bottom: 15px;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.05);
#         border-left: 4px solid #785D32;
#     }
#     .agent-header {
#         display: flex;
#         align-items: center;
#         margin-bottom: 10px;
#     }
#     .agent-name {
#         font-weight: bold;
#         font-size: 18px;
#         color: #3E160C;
#     }
#     .agent-meta {
#         color: #6c757d;
#         font-size: 13px;
#         margin-top: 5px;
#     }
#     .adherence-value {
#         font-size: 22px;
#         font-weight: bold;
#         text-align: center;
#     }
#     .high-adherence {
#         color: #198754;
#     }
#     .low-adherence {
#         color: #3E160C;
#     }
#     .legend-container {
#         background-color: white;
#         border-radius: 8px;
#         padding: 10px;
#         margin: 10px 0 20px 0;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.05);
#     }
#     .date-selector {
#         background-color: white;
#         border-radius: 8px;
#         padding: 15px;
#         margin-bottom: 20px;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.05);
#     }
#     .stButton>button {
#         background-color: #785D32;
#         color: white;
#         border: none;
#         border-radius: 4px;
#         padding: 0.5rem 1rem;
#     }
#     .stButton>button:hover {
#         background-color: #5d4826;
#     }
#     .stSelectbox>div>div {
#         background-color: white;
#     }
#     .stMultiSelect>div>div {
#         background-color: white;
#     }
#     .stSidebar .stButton>button {
#         width: 100%;
#     }
#     .time-marker {
#         font-size: 9px;
#         color: #3E160C;
#         font-weight: bold;
#     }
#     .stMetric {
#         background-color: #f9f7f4;
#         padding: 10px;
#         border-radius: 8px;
#     }
#     .stMetric > div {
#         justify-content: center;
#     }
#     .stMetric [data-testid="stMetricLabel"] {
#         display: none;
#     }
#     .stMetric [data-testid="stMetricValue"] {
#         font-size: 28px !important;
#     }
#     .divider {
#         margin: 0;
#         padding: 0;
#         height: 1px;
#     }
#     .title-container {
#         display: flex;
#         align-items: center;
#         margin-bottom: 20px;
#         background-color: white;
#         padding: 15px;
#         border-radius: 8px;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.05);
#     }
#     .title-icon {
#         font-size: 24px;
#         margin-right: 10px;
#     }
#     .title-text {
#         font-size: 24px;
#         font-weight: bold;
#         color: #3E160C;
#     }
# </style>
# """, unsafe_allow_html=True)

# # 2. Connexion à Google Sheets
# @st.cache_resource(ttl=600)
# def get_google_client():
#     scope = [
#         "https://spreadsheets.google.com/feeds",
#         "https://www.googleapis.com/auth/drive"
#     ]
#     creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
#     return gspread.authorize(creds)

# # 3. Charger les données
# @st.cache_data(ttl=300)
# def load_data():
#     try:
#         client = get_google_client()
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
                
#         return pd.concat([df1, df2])
#     except Exception as e:
#         st.error(f"Erreur lors du chargement des données : {e}")
#         return pd.DataFrame()

# # Charger les données
# df_combined = load_data()



# # Sidebar avec style amélioré
# st.sidebar.markdown("""
# <div style="text-align: center; padding: 10px 0; margin-bottom: 20px; background-color: #785D32; color: white; border-radius: 5px;">
#     <h2 style="margin: 0; font-size: 20px;">Filtres</h2>
# </div>
# """, unsafe_allow_html=True)

# # Section de sélection de date
# if not df_combined.empty and 'Date' in df_combined.columns:
#     # Obtenir les dates uniques des deux dataframes
#     all_dates = sorted(df_combined['Date'].unique())
    
#     # Formater les dates pour l'affichage
#     date_options = [date.strftime('%d/%m/%Y') for date in all_dates]
#     date_options = [""] + date_options 
    
#     st.sidebar.markdown("""
#     <div style="font-weight: bold; margin-bottom: 5px; color: #3E160C;">Sélectionner une date</div>
#     """, unsafe_allow_html=True)
    
#     selected_date = st.sidebar.selectbox(
#         "",
#         options=date_options,
#         index=0,
#     )
    
#     if selected_date == "":
#         # Si aucune date n'est sélectionnée, afficher un message
#         st.sidebar.warning("⚠️ Veuillez sélectionner une date pour afficher les données et activer les filtres.")
#         date_selected = False
#         # Initialiser des listes vides pour les filtres
#         selected_files = []
#         selected_tlss = []
#         selected_ops = []
#     else:
#         # Si une date est sélectionnée, filtrer les données et afficher les filtres
#         selected_date_dt = pd.to_datetime(selected_date, format='%d/%m/%Y')
#         df = df_combined[df_combined['Date'] == selected_date_dt]
#         st.sidebar.success(f"Affichage des données du {selected_date}")
#         date_selected = True
        
#         # Récupérer les valeurs uniques pour chaque filtre à partir des données filtrées par date
#         all_files = sorted(df['File'].dropna().unique().tolist())
#         all_tlss = sorted(df['Tls'].dropna().unique().tolist())
#         all_ops = sorted(df['OPS'].dropna().unique().tolist())

#         # Séparateur
#         st.sidebar.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        
#         # Créer les multiselect dans la sidebar avec des titres améliorés
#         st.sidebar.markdown("""
#         <div style="font-weight: bold; margin-bottom: 5px; color: #3E160C;">Filtrer par File</div>
#         """, unsafe_allow_html=True)
#         selected_files = st.sidebar.multiselect(
#             "",
#             options=all_files,
#             default=None,
#             placeholder="Sélectionnez une ou plusieurs files"
#         )

#         st.sidebar.markdown("""
#         <div style="font-weight: bold; margin-bottom: 5px; margin-top: 15px; color: #3E160C;">Filtrer par TLS</div>
#         """, unsafe_allow_html=True)
#         selected_tlss = st.sidebar.multiselect(
#             "",
#             options=all_tlss,
#             default=None,
#             placeholder="Sélectionnez un ou plusieurs TLS"
#         )

#         st.sidebar.markdown("""
#         <div style="font-weight: bold; margin-bottom: 5px; margin-top: 15px; color: #3E160C;">Filtrer par OPS</div>
#         """, unsafe_allow_html=True)
#         selected_ops = st.sidebar.multiselect(
#             "",
#             options=all_ops,
#             default=None,
#             placeholder="Sélectionnez un ou plusieurs OPS"
#         )
# else:
#     # Si pas de colonne Date ou dataframe vide
#     st.error("Aucune donnée n'a été chargée ou la colonne 'Date' est manquante.")
#     date_selected = False
#     # Initialiser des listes vides pour éviter les erreurs
#     selected_files = []
#     selected_tlss = []
#     selected_ops = []
#     df = pd.DataFrame()

# # Bouton de rafraîchissement
# st.sidebar.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
# if st.sidebar.button("🔄 Rafraîchir les données"):
#     st.cache_data.clear()
#     st.cache_resource.clear()
#     st.rerun()


# # 5. Fonction de filtrage améliorée
# def apply_filters(data, files=None, tlss=None, ops=None):
#     filtered = data.copy()
    
#     # Appliquer les filtres seulement si des options sont sélectionnées
#     if files:
#         filtered = filtered[filtered['File'].isin(files)]
#     if tlss:
#         filtered = filtered[filtered['Tls'].isin(tlss)]
#     if ops:
#         filtered = filtered[filtered['OPS'].isin(ops)]
    
#     return filtered

# # 6. Fonction pour créer les graphiques avec les nouvelles couleurs
# def create_agent_plot(agent_df, agent_name):
#     # Nouvelles couleurs de la palette
#     prod_color = "#050A30"    # Off-Navy
#     pause_color = "#E8D9CA"   # Pale
#     lunch_color = "#785D32"   # Gold
#     adherence_high = "#198754"  # Vert pour adhérence élevée
#     adherence_low = "#3E160C"   # Rough pour adhérence basse
    
#     fig, (ax_prev, ax_real, ax_ad) = plt.subplots(3, 1, figsize=(15, 2.5))
#     plt.subplots_adjust(hspace=0.5)
#     fig.patch.set_facecolor('#ffffff')

#     # Planning prévu
#     x_start = 0
#     current_hour = None
#     hour_positions = {}  # Pour stocker les positions des heures entières
    
#     for i, row in agent_df.iterrows():
#         # Récupérer l'heure de la tranche
#         tranche = row.get('Tranche', '')
        
#         # Extraire l'heure depuis la tranche (format: "HH:MM")
#         if tranche:
#             heure_format = tranche.split(' ')[-1] if ' ' in tranche else tranche
#             # Extraire seulement l'heure (partie avant les ":")
#             heure_principale = heure_format.split(':')[0] if ':' in heure_format else heure_format
            
#             # Vérifier si c'est une nouvelle heure entière (et non une fraction de 15 min)
#             if heure_format.endswith(':00') and heure_principale != current_hour:
#                 current_hour = heure_principale
#                 hour_positions[x_start] = heure_principale + ':00'  # Marquer cette position pour l'heure
        
#         # Dessiner la barre avec la couleur appropriée
#         if row['Prod'] > 0:
#             color = prod_color
#         elif row['Pause_planning'] > 0:
#             color = pause_color
#         elif row['Lunch'] > 0:
#             color = lunch_color
#         else:
#             color = "#F7F7F7"
            
#         # Dessiner la barre
#         ax_prev.barh(0, 900, left=x_start, color=color, edgecolor='none')
#         x_start += 900
    
#     # Ajouter les heures entières aux positions calculées
#     for pos, heure in hour_positions.items():
#         ax_prev.text(pos + 450, 0.7, heure, 
#                      ha='center', va='center', fontsize=9, 
#                      color='#3E160C', fontweight='bold')

#     # Réalisé
#     x_start = 0
#     for _, row in agent_df.iterrows():
#         if row['Pause_realise'] > row['prod_realise']:
#             color = pause_color
#         elif row['prod_realise'] > row['Pause_realise']:
#             color = prod_color
#         elif row['Pause_realise'] == 0 and row['prod_realise'] == 0:
#             color = lunch_color
#         else:
#             color = "#F7F7F7"
#         ax_real.barh(0, 900, left=x_start, color=color, edgecolor='none')
#         x_start += 900

#     # Adhérence
#     x_start = 0
#     for _, row in agent_df.iterrows():
#         adherence_value = float(str(row['Adherence']).rstrip('%'))
#         color = adherence_high if adherence_value >= 90 else adherence_low
#         ax_ad.barh(0, 900, left=x_start, color=color, edgecolor='none')
#         x_start += 900

#     # Config
#     for ax in [ax_prev, ax_real, ax_ad]:
#         ax.set_xlim(0, x_start)
#         ax.set_yticks([])
#         ax.axis('off')

#     ax_prev.set_title(f"Prévu", loc='left', pad=5, fontsize=10, color='#3E160C')
#     ax_real.set_title("Réalisé", loc='left', pad=5, fontsize=10, color='#3E160C')
#     ax_ad.set_title("Adhérence", loc='left', pad=5, fontsize=10, color='#3E160C')

#     return fig

# # Affichage dans Streamlit
# if date_selected:
#     # Légende avec les nouvelles couleurs
#     legend_html = """
#     <div class="legend-container">
#         <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin: 5px 0;">
#             <div style="display: flex; align-items: center;">
#                 <div style="width: 15px; height: 15px; background-color: #050A30; margin-right: 5px; border-radius: 3px;"></div>
#                 <span>Production</span>
#             </div>
#             <div style="display: flex; align-items: center;">
#                 <div style="width: 15px; height: 15px; background-color: #E8D9CA; margin-right: 5px; border-radius: 3px;"></div>
#                 <span>Pause</span>
#             </div>
#             <div style="display: flex; align-items: center;">
#                 <div style="width: 15px; height: 15px; background-color: #785D32; margin-right: 5px; border-radius: 3px;"></div>
#                 <span>Lunch</span>
#             </div>
#             <div style="display: flex; align-items: center;">
#                 <div style="width: 15px; height: 15px; background-color: #198754; margin-right: 5px; border-radius: 3px;"></div>
#                 <span>Adhérence ≥ 90%</span>
#             </div>
#             <div style="display: flex; align-items: center;">
#                 <div style="width: 15px; height: 15px; background-color: #3E160C; margin-right: 5px; border-radius: 3px;"></div>
#                 <span>Adhérence < 90%</span>
#             </div>
#         </div>
#     </div>
#     """
#     st.markdown(legend_html, unsafe_allow_html=True)
    
#     # Appliquer les filtres aux données filtrées par date
#     filtered_df = apply_filters(df, selected_files, selected_tlss, selected_ops)
    
#     if not filtered_df.empty:
#         st.sidebar.success(f"{len(filtered_df['Nom Agent'].unique())} agents correspondent aux filtres")
        
#         # Afficher les agents
#         for agent_name in filtered_df['Nom Agent'].unique():
#             agent_data = filtered_df[filtered_df['Nom Agent'] == agent_name]
            
#             # Calculer l'adhérence
#             adherence_mean = agent_data['Adherence'].str.rstrip('%').astype(float).mean()
#             adherence = f"{adherence_mean:.1f}%"
#             adherence_class = "high-adherence" if adherence_mean >= 90 else "low-adherence"
#             adherence_color = "#198754" if adherence_mean >= 90 else "#3E160C"
            
#             # Récupérer les métadonnées de l'agent
#             file_name = agent_data['File'].iloc[0]
#             tls_name = agent_data['Tls'].iloc[0]
#             ops_name = agent_data['OPS'].iloc[0]
            
#             # Créer le conteneur de l'agent avec colonnes
#             with st.container():
#                 cols = st.columns([2, 6, 1])
                
#                 # Colonne 1: Infos de l'agent
#                 with cols[0]:
#                     st.markdown(f"""
#                     <div style="padding: 10px; background-color: white; border-radius: 8px; height: 100%; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
#                         <div class="agent-name">{agent_name}</div>
#                         <div class="agent-meta">File: {file_name}</div>
#                         <div class="agent-meta">TLS: {tls_name}</div>
#                         <div class="agent-meta">OPS: {ops_name}</div>
#                     </div>
#                     """, unsafe_allow_html=True)
                
#                 # Colonne 2: Visualisation du planning
#                 with cols[1]:
#                     fig = create_agent_plot(agent_data, agent_name)
#                     st.pyplot(fig, use_container_width=True)
                
#                 # Colonne 3: Adhérence
#                 with cols[2]:
#                     st.markdown(f"""
#                     <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; padding: 10px; background-color: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
#                         <div style="font-size: 14px; margin-bottom: 5px; color: #3E160C;">Adhérence</div>
#                         <div style="font-size: 24px; font-weight: bold; color: {adherence_color};">{adherence}</div>
#                     </div>
#                     """, unsafe_allow_html=True)
            
#             # Ajouter un petit séparateur entre les agents
#             st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
#     else:
#         st.warning("Aucun agent ne correspond aux critères de filtrage sélectionnés.")
# else:
#     # Si aucune date n'est sélectionnée, afficher le message principal
#     st.markdown("""
#     <div style="text-align: center; padding: 50px 20px; background-color: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
#         <div style="font-size: 50px; margin-bottom: 20px;">⏰</div>
#         <h2 style="color: #3E160C; margin-bottom: 20px;">Bienvenue sur la page de visualisation des donnees </h2>
#         <p style="color: #6c757d; font-size: 16px; margin-bottom: 10px;">⚠️ Veuillez sélectionner une date dans le menu latéral pour afficher les données.</p>
#         <p style="color: #6c757d; font-size: 14px;">Une fois une date sélectionnée, vous pourrez également filtrer par File, TLS ou OPS.</p>
#     </div>
#     """, unsafe_allow_html=True)

#     st.warning("Pour revenir au dashboard, cliquez sur l'option **Dashboard** dans le menu de gauche")





import streamlit as st
import gspread
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Real Time Adherence",
    page_icon="📈",
    layout="wide"
)

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
        st.switch_page("Dashboard.py")

with nav_cols[1]:
    if st.session_state.role == "admin" and st.button("👑 Administration"):
        st.switch_page("Admin.py")

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
        
        # Récupérer la première feuille
        sheet1 = spreadsheet.sheet1
        all_data1 = sheet1.get_all_records()
        df1 = pd.DataFrame(all_data1)
        
        # Récupérer la deuxième feuille
        sheet2 = spreadsheet.get_worksheet(1)
        all_data2 = sheet2.get_all_records()
        df2 = pd.DataFrame(all_data2)
        
        # S'assurer que la colonne Date est au format datetime
        if 'Date' in df1.columns:
            df1['Date'] = pd.to_datetime(df1['Date'], format='%d/%m/%Y')
        
        if 'Date' in df2.columns:
            df2['Date'] = pd.to_datetime(df2['Date'], format='%d/%m/%Y')
        
        # Conversion des durées
        time_cols = ['Prod', 'Pause_planning', 'Lunch', 'Pause_realise', 'prod_realise']
        for col in time_cols:
            if col in df1.columns:
                df1[col] = pd.to_timedelta(df1[col]).dt.total_seconds()
            if col in df2.columns:
                df2[col] = pd.to_timedelta(df2[col]).dt.total_seconds()
                
        return pd.concat([df1, df2])
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
else:
    # Si pas de colonne Date ou dataframe vide
    st.error("⚠️ Aucune donnée n'a été chargée ou la colonne 'Date' est manquante.")
    date_selected = False
    # Initialiser des listes vides pour éviter les erreurs
    selected_files = []
    selected_tlss = []
    selected_ops = []
    df = pd.DataFrame()

# Bouton de rafraîchissement
st.sidebar.markdown('<div class="sidebar-section-title">Actions</div>', unsafe_allow_html=True)
if st.sidebar.button("🔄 Rafraîchir les données"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

# Fonction de filtrage améliorée
def apply_filters(data, files=None, tlss=None, ops=None):
    filtered = data.copy()
    
    # Appliquer les filtres seulement si des options sont sélectionnées
    if files and len(files) > 0:
        filtered = filtered[filtered['File'].isin(files)]
    if tlss and len(tlss) > 0:
        filtered = filtered[filtered['Tls'].isin(tlss)]
    if ops and len(ops) > 0:
        filtered = filtered[filtered['OPS'].isin(ops)]
    
    return filtered

# Fonction pour créer les graphiques avec style amélioré
# Fonction pour créer les graphiques avec style amélioré
def create_agent_plot(agent_df):  # Supprimé l'argument agent_name inutilisé
    # Palette de couleurs moderne
    prod_color = "#1a73e8"    # Bleu principal
    pause_color = "#00bcd4"   # Turquoise
    lunch_color = "#ff9800"   # Orange
    adherence_high = "#4caf50"  # Vert
    adherence_low = "#f44336"   # Rouge
    
    fig, (ax_prev, ax_real, ax_ad) = plt.subplots(3, 1, figsize=(15, 2.7))
    plt.subplots_adjust(hspace=0.5)
    fig.patch.set_facecolor('#ffffff')

    # Planning prévu
    x_start = 0
    current_hour = None
    hour_positions = {}  # Pour stocker les positions des heures entières
    
    for i, row in agent_df.iterrows():
        # Récupérer l'heure de la tranche
        tranche = row.get('Tranche', '')
        
        # Extraire l'heure depuis la tranche (format: "HH:MM")
        if tranche:
            heure_format = tranche.split(' ')[-1] if ' ' in tranche else tranche
            # Extraire seulement l'heure (partie avant les ":")
            heure_principale = heure_format.split(':')[0] if ':' in heure_format else heure_format
            
            # Vérifier si c'est une nouvelle heure entière
            if heure_format.endswith(':00') and heure_principale != current_hour:
                current_hour = heure_principale
                hour_positions[x_start] = heure_principale + ':00'
        
        # Dessiner la barre avec la couleur appropriée
        if row['Prod'] > 0:
            color = prod_color
        elif row['Pause_planning'] > 0:
            color = pause_color
        elif row['Lunch'] > 0:
            color = lunch_color
        else:
            color = "#F7F7F7"
            
        # Dessiner la barre
        ax_prev.barh(0, 900, left=x_start, color=color, edgecolor='none', alpha=0.9)
        x_start += 900
    
    # Ajouter les heures entières aux positions calculées
    for pos, heure in hour_positions.items():
        ax_prev.text(pos + 450, 0.7, heure, 
                     ha='center', va='center', fontsize=9, 
                     color='#424242', fontweight='bold',
                     bbox=dict(facecolor='white', edgecolor='none', pad=1, alpha=0.7))

    # Réalisé
    x_start = 0
    for _, row in agent_df.iterrows():
        if row['Pause_realise'] > row['prod_realise']:
            color = pause_color
        elif row['prod_realise'] > row['Pause_realise']:
            color = prod_color
        elif row['Pause_realise'] == 0 and row['prod_realise'] == 0:
            color = lunch_color
        else:
            color = "#F7F7F7"
        ax_real.barh(0, 900, left=x_start, color=color, edgecolor='none', alpha=0.9)
        x_start += 900

    # Adhérence
    x_start = 0
    for _, row in agent_df.iterrows():
        adherence_value = float(str(row['Adherence']).rstrip('%'))
        color = adherence_high if adherence_value >= 90 else adherence_low
        ax_ad.barh(0, 900, left=x_start, color=color, edgecolor='none', alpha=0.9)
        x_start += 900

    # Configuration esthétique
    for ax in [ax_prev, ax_real, ax_ad]:
        ax.set_xlim(0, x_start)
        ax.set_yticks([])
        ax.axis('off')
        # Ajouter un cadre léger
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(0.5)
            spine.set_color('#e0e0e0')

    # Titres des sections
    font_props = {'fontsize': 10, 'fontweight': 'medium', 'fontfamily': 'sans-serif'}
    ax_prev.set_title("Prévu", loc='left', pad=5, color='#424242', **font_props)
    ax_real.set_title("Réalisé", loc='left', pad=5, color='#424242', **font_props)
    ax_ad.set_title("Adhérence", loc='left', pad=5, color='#424242', **font_props)

    # Supprimer le code problématique de bordures arrondies
    # Au lieu d'utiliser set_boxstyle, on peut définir la couleur de fond
    for ax in [ax_prev, ax_real, ax_ad]:
        ax.set_facecolor('#f8f9fa')  # Définir la couleur de fond
        # On peut aussi ajouter un léger padding, mais pas avec boxstyle
        ax.set_frame_on(True)  # S'assurer que le cadre est visible

    # Ajuster l'espacement
    fig.tight_layout()
    
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
            <div class="legend-color" style="background-color: #4caf50;"></div>
            <div class="legend-label">Adhérence ≥ 90%</div>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background-color: #f44336;"></div>
            <div class="legend-label">Adhérence < 90%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Appliquer les filtres aux données filtrées par date
    filtered_df = apply_filters(df, selected_files, selected_tlss, selected_ops)
    
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
        st.markdown("## Adhérence par agent")
        
        # Séparateur entre agents
        for i, agent_name in enumerate(filtered_df['Nom Agent'].unique()):
            agent_data = filtered_df[filtered_df['Nom Agent'] == agent_name]
            
            # Calculer l'adhérence moyenne
            adherence_mean = agent_data['Adherence'].str.rstrip('%').astype(float).mean()
            adherence = f"{adherence_mean:.1f}%"
            adherence_class = "high-adherence" if adherence_mean >= 90 else "low-adherence"
            adherence_color = "#4caf50" if adherence_mean >= 90 else "#f44336"
            
            # Récupérer les métadonnées de l'agent
            file_name = agent_data['File'].iloc[0]
            tls_name = agent_data['Tls'].iloc[0]
            ops_name = agent_data['OPS'].iloc[0]
            
            # Créer le conteneur de l'agent avec colonnes et design amélioré
            with st.container():
                cols = st.columns([2, 6, 1])
                
                # Colonne 1: Infos de l'agent
                with cols[0]:
                    st.markdown(f"""
                    <div style="padding: 15px; background-color: white; border-radius: 10px; height: 100%; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                        <div style="font-weight: 600; font-size: 16px; color: #212121; margin-bottom: 5px;">{agent_name}</div>
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
                    st.pyplot(fig, use_container_width=True)
                
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
