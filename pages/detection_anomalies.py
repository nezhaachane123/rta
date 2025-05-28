
####################code grp par  agent
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


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
       Détection des Anomalies d’Adhérence
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
    if st.button("📈 Predictions"):
        st.switch_page("pages/predictions.py")

with col6:
    if st.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.switch_page("Home.py")

# Ligne de séparation
st.markdown('<hr style="margin: 1rem 0; border: none; height: 1px; background-color: #e0e0e0;">', unsafe_allow_html=True)



# ========== Chargement des données ========== #
@st.cache_data(ttl=600)
def load_data():
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open("data_ml")
        all_worksheets = spreadsheet.worksheets()
        all_dfs = []
        for worksheet in all_worksheets:
            sheet_name = worksheet.title
            all_data = worksheet.get_all_records()
            if all_data:
                df = pd.DataFrame(all_data)
                df['source_sheet'] = sheet_name
                if 'Date' in df.columns:
                    try:
                        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                    except:
                        st.warning(f"Problème de conversion de date dans {sheet_name}")
                all_dfs.append(df)
        if all_dfs:
            return pd.concat(all_dfs, ignore_index=True)
        else:
            st.warning("Aucune donnée trouvée dans le classeur.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erreur chargement données : {e}")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

# ========== Sidebar filtres et refresh ========== #
with st.sidebar:
    st.markdown("""
    <div style="background-color: #1a73e8; padding: 10px; border-radius: 8px; color: white; text-align: center; margin-bottom: 20px; font-weight: 600;">
        FILTRES
    </div>
    """, unsafe_allow_html=True)
    selected_dates = st.multiselect("Date", sorted(df['Date'].dropna().unique()), default=sorted(df['Date'].dropna().unique()))
    selected_files = st.multiselect("File", sorted(df['File'].dropna().unique()), default=sorted(df['File'].dropna().unique()))
    selected_ops = st.multiselect("OPS", sorted(df['OPS'].dropna().unique()), default=sorted(df['OPS'].dropna().unique()))
    selected_tls = st.multiselect("TLS", sorted(df['Tls'].dropna().unique()), default=sorted(df['Tls'].dropna().unique()))
    st.markdown('<div style="margin: 15px 0; height: 1px; background: #e0e0e0;"></div>', unsafe_allow_html=True)
    if st.button("🔄 Rafraîchir les données"):
        st.cache_data.clear()
        st.rerun()

# ========== Filtrage dynamique ========== #
mask = pd.Series([True] * len(df))
if selected_dates:
    mask &= df['Date'].isin(selected_dates)
if selected_files:
    mask &= df['File'].isin(selected_files)
if selected_ops:
    mask &= df['OPS'].isin(selected_ops)
if selected_tls:
    mask &= df['Tls'].isin(selected_tls)
df_filtered = df[mask]
sort_cols = ['Date', 'File', 'OPS', 'Tls', 'Nom Agent', 'Tranche']

# ---- KPIs cards - Nombre d'agents distincts concernés ----
lunch_agents = df_filtered[df_filtered['Pause_Lunch_Non_Respectee'] == 1]['Nom Agent'].nunique()
debut_agents = df_filtered[df_filtered['Debut_Non_Respecte'] == 1]['Nom Agent'].nunique()
fin_agents = df_filtered[df_filtered['Fin_Non_Respecte'] == 1]['Nom Agent'].nunique()

kpi_cols = st.columns(3)
with kpi_cols[0]:
    st.markdown(
        f"<div class='card' style='border-top:4px solid #0060c0'>"
        f"<span style='font-size:1.5rem; color:#0060c0; font-weight:bold'>{lunch_agents}</span><br>"
        f"<span style='color:#0060c0'>Agents - Non-respect Lunch</span></div>",
        unsafe_allow_html=True)
with kpi_cols[1]:
    st.markdown(
        f"<div class='card' style='border-top:4px solid #ff7043'>"
        f"<span style='font-size:1.5rem; color:#ff7043; font-weight:bold'>{debut_agents}</span><br>"
        f"<span style='color:#ff7043'>Agents - Non-respect Début</span></div>",
        unsafe_allow_html=True)
with kpi_cols[2]:
    st.markdown(
        f"<div class='card' style='border-top:4px solid #00897b'>"
        f"<span style='font-size:1.5rem; color:#00897b; font-weight:bold'>{fin_agents}</span><br>"
        f"<span style='color:#00897b'>Agents - Non-respect Fin</span></div>",
        unsafe_allow_html=True)

st.markdown("---")


# ========== Regroupement agents par anomalie ========== #
def synthese_agents(df_section):
    agg = df_section.groupby(['Nom Agent', 'Date', 'File', 'Tls', 'OPS']).agg({
        'Tranche': 'count'
    }).reset_index()
    agg['Durée non respectée'] = agg['Tranche'] * 15  # 15min par tranche
    return agg

# ========== Section affichage agents en CARTES ========== #
def section_audit(type_label, label_col, color, sort_cols):
    df_section = df_filtered[df_filtered[label_col] == 1].sort_values(sort_cols)
    df_agents = synthese_agents(df_section)
    nb_agents = df_agents['Nom Agent'].nunique()
    st.markdown(f"<h2 style='color:{color}; margin-top:2rem'>{type_label} ({nb_agents} agents)</h2>", unsafe_allow_html=True)
    if df_agents.empty:
        st.info(f"Aucun cas de {type_label.lower()} détecté avec les filtres appliqués.")
    else:
        for _, row in df_agents.iterrows():
            st.markdown(f"""
            <div style='
                background:#fff; 
                border-radius:13px; 
                box-shadow:0 2px 7px rgba(0,0,0,0.06); 
                margin-bottom:1.1rem; 
                padding:1.25rem 1.4rem; 
                display:flex; 
                align-items:center;
                border-left: 6px solid {color};
                '>
                <div style='flex:1'>
                    <div style='font-size:1.13rem; color:#222; font-weight:600;'>{row['Nom Agent']}</div>
                    <div style='margin-top:6px; color:#333;'>
                        <b style="color:#1a73e8;">{row['Date'].strftime('%d/%m/%Y') if not pd.isnull(row['Date']) else ''}</b>
                        &nbsp;|&nbsp; <b>File</b>: {row['File']}
                        &nbsp;|&nbsp; <b>TLS</b>: {row['Tls']}
                        &nbsp;|&nbsp; <b>OPS</b>: {row['OPS']}
                    </div>
                    <div style='margin-top:5px; color:#111;'>
                        <span style="background:#f0f3ff; border-radius:6px; padding:3px 11px; font-size:1rem; color:#1a73e8; font-weight:500;">
                            Durée non respectée : <b>{row['Durée non respectée']}</b> min
                        </span>
                    </div>
                </div>
                <div>
                    <span style='padding:9px 17px; background:{color}; color:white; border-radius:8px; font-weight:600; font-size:1rem;'>
                        ⚠️ {type_label}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

section_audit("Non-respect Lunch", "Pause_Lunch_Non_Respectee", "#0060c0", sort_cols)
section_audit("Non-respect Début", "Debut_Non_Respecte", "#ff7043", sort_cols)
section_audit("Non-respect Fin", "Fin_Non_Respecte", "#00897b", sort_cols)

# ========== Footer ==========
st.markdown(
    "<div style='text-align:right; color:#aaa; font-size:0.8rem; margin-top:2rem;'>Powered by Intelcia WFM | 2024</div>",
    unsafe_allow_html=True
)
