

import streamlit as st
import pandas as pd
import joblib
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import io


# Configuration de la page
st.set_page_config(
    page_title="detection_anomalies",
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
        Identification Prédictive des Agents Non-Adhérents 
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
col1, col2, col3,col4,col5,col6 = st.columns([1, 1, 1,1,1,1])
with col1:
    if st.session_state.role == "admin" and st.button("👑 Administration"):
        st.switch_page("pages/Admin.py")
        
with col2:
    if st.button("📈 Dashboard"):
        st.switch_page("pages/Dashboard.py")

with col3:
    if st.button("📈 Real Time Adherence"):
        st.switch_page("pages/Real_Time_Adherence.py")

with col4:
    if st.button("📊 Suivi de production"):
        st.switch_page("pages/suivi_production.py")
        
with col5:
    if st.button("📈 detection_anomalies"):
        st.switch_page("pages/detection_anomalies.py")

with col6:
    if st.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.switch_page("Home.py")

# Ligne de séparation
st.markdown('<hr style="margin: 1rem 0; border: none; height: 1px; background-color: #e0e0e0;">', unsafe_allow_html=True)


# --- 1. Chargement modèles et features (même fichier pour les 3) ---
def load_model_joblib(path):
    return joblib.load(path)

@st.cache_resource
def load_models():
    return (
        load_model_joblib('model_adherence_lunch.joblib'),
        load_model_joblib('model_adherence_debut.joblib'),
        load_model_joblib('model_adherence_fin.joblib')
    )

@st.cache_data
def load_features():
    with open('features_used.json', 'r') as f:
        return json.load(f)

model_lunch, model_debut, model_fin = load_models()
features = load_features()

# --- 2. Chargement des données Google Sheets ---
@st.cache_data(ttl=600)
def load_gs_data():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("predict_data")      # <-- Adapter si besoin
    worksheet = spreadsheet.worksheet("Sheet1")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    return df

# st.title("🔮 Prédiction ML - Début, Lunch & Fin (Google Sheets)")

df = load_gs_data()
if df.empty:
    st.warning("Aucune donnée trouvée dans Google Sheets.")
    st.stop()
else:
    # st.success(f"{len(df)} lignes chargées depuis Google Sheets.")

    # --- 3. Feature engineering (une seule fois) ---
    def to_seconds(x):
        try:
            if pd.isna(x) or x in ['NaT', '', None]:
                return 0
            if isinstance(x, (float, int)) and np.isnan(x):
                return 0
            parts = [int(i) for i in str(x).split(':')]
            if len(parts) == 2:
                h, m = parts
                s = 0
            elif len(parts) == 3:
                h, m, s = parts
            else:
                return 0
            return h*3600 + m*60 + s
        except Exception:
            return 0

    if 'Prod' in df.columns:
        df['Prod_s'] = df['Prod'].apply(to_seconds)
    if 'Pause_planning' in df.columns:
        df['Pause_planning_s'] = df['Pause_planning'].apply(to_seconds)
    if 'Lunch' in df.columns:
        df['Lunch_s'] = df['Lunch'].apply(to_seconds)
    if 'Date' in df.columns:
        df['Jour'] = pd.to_datetime(df['Date'], errors='coerce').dt.dayofweek

    # --- 4. Sauvegarder les vraies valeurs pour affichage ---
    affichage_cols = ['Nom Agent', 'Date', 'Tranche', 'File', 'Tls', 'OPS']
    df_affichage = df[affichage_cols].copy()

    # --- 5. Encodage catégoriel pour toutes les features ---
    # for col in features:
    #     if col in df.columns:
    #         df[col] = df[col].astype('category').cat.codes
    for col in ['File', 'Tls', 'OPS', 'Tranche']:
        if col in df.columns:
            df[col] = df[col].astype('category').cat.codes

   
    # --- 6. Prédictions (une seule fois pour toutes les features) ---
    missing_cols = [col for col in features if col not in df.columns]
    if missing_cols:
        st.error(f"Colonnes manquantes dans le DataFrame pour la prédiction : {missing_cols}")
        st.stop()

    X_pred = df[features]

    df_affichage['Pred_Lunch'] = model_lunch.predict(X_pred)
    df_affichage['Pred_Debut'] = model_debut.predict(X_pred)
    df_affichage['Pred_Fin'] = model_fin.predict(X_pred)

    # --- 7. AFFICHAGE CARDS ---
    def display_cards(df, pred_col, color, titre, emoji):
        st.header(titre)
        agents_risque = df[df[pred_col] == 1].drop_duplicates(subset=['Nom Agent'])
        if agents_risque.empty:
            st.success(f"Aucun agent à risque détecté pour {titre.lower()} selon le modèle ML.")
        else:
            for _, row in agents_risque.iterrows():
                st.markdown(f"""
                <div style='background:#fff; border-radius:13px; box-shadow:0 2px 7px rgba(0,0,0,0.06); margin-bottom:1.1rem; padding:1.25rem 1.4rem; display:flex; align-items:center; border-left: 6px solid {color};'>
                    <div style='flex:1'>
                        <div style='font-size:1.13rem; color:#222; font-weight:600;'>{row.get('Nom Agent','')}</div>
                        <div style='margin-top:6px; color:#333;'>
                            <b style="color:{color};">{row.get('Date','')}</b>
                            &nbsp;|&nbsp; <b>Tranche</b>: {row.get('Tranche','')}
                            &nbsp;|&nbsp; <b>File</b>: {row.get('File','')}
                            &nbsp;|&nbsp; <b>TLS</b>: {row.get('Tls','')}
                            &nbsp;|&nbsp; <b>OPS</b>: {row.get('OPS','')}
                        </div>
                    </div>
                    <div>
                        <span style='padding:9px 17px; background:{color}; color:white; border-radius:8px; font-weight:600; font-size:1rem;'>
                            {emoji} Risque
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    display_cards(df_affichage, "Pred_Lunch", "#0060c0", "👁️‍🗨️ Agents à risque de non-respect Lunch", "⚠️")
    display_cards(df_affichage, "Pred_Debut", "#ff7043", "👁️‍🗨️ Agents à risque de non-respect Début", "⏰")
    display_cards(df_affichage, "Pred_Fin", "#00897b", "👁️‍🗨️ Agents à risque de non-respect Fin", "🚩")

    # --- Download bouton Excel ---
    # output = io.BytesIO()
    # with pd.ExcelWriter(output, engine='openpyxl') as writer:
    #     df_affichage.to_excel(writer, index=False)
    # output.seek(0)
    # st.download_button(
    #     "Télécharger les résultats prédits (3 risques)",
    #     data=output,
    #     file_name="resultats_prediction_all.xlsx",
    #     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    # )
