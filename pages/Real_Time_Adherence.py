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
def apply_filters(data, files=None, tlss=None, ops=None, min_adherence=0, max_adherence=100):
    filtered = data.copy()
    
    # Appliquer les filtres seulement si des options sont sélectionnées
    if files and len(files) > 0:
        filtered = filtered[filtered['File'].isin(files)]
    if tlss and len(tlss) > 0:
        filtered = filtered[filtered['Tls'].isin(tlss)]
    if ops and len(ops) > 0:
        filtered = filtered[filtered['OPS'].isin(ops)]
    
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
    
    # Appliquer les filtres aux données filtrées par date
    filtered_df = apply_filters(
        df, 
        selected_files, 
        selected_tlss, 
        selected_ops,
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









