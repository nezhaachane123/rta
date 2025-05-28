
                                ####code 
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px

def connect_to_sheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    # Utiliser les credentials pour la feuille users
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client

# Configuration de la page
st.set_page_config(
    page_title="Visualisation de Production",
    page_icon="📊",
    layout="wide"
)

# CSS personnalisé pour améliorer l'apparence - en cohérence avec les autres pages
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
    
    /* Styles personnalisés pour les expandeurs */
    div.stExpander {
        border: 1px solid #f0f0f0;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    
    div.stExpander > div:first-child {
        background-color: #f8f9fa;
    }
    
    .highlight-box {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    
    .excellent {
        background-color: rgba(5, 150, 105, 0.1);
    }
    
    .good {
        background-color: rgba(2, 132, 199, 0.1);
    }
    
    .average {
        background-color: rgba(217, 119, 6, 0.1);
    }
    
    .poor {
        background-color: rgba(220, 38, 38, 0.1);
    }
    
    /* Style pour la légende */
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
        <div style="font-size: 2.5rem; margin-right: 10px; color: #1a73e8;">📊</div>
        <h1 style="margin: 0; font-size: 2rem;">Suivi de Production</h1>
    </div>
    <div style="margin-left: auto; padding: 8px 15px; background-color: #e8f0fe; border-radius: 30px; display: flex; align-items: center;">
        <span style="color: #1a73e8; margin-right: 8px;">👤</span>
        <span style="font-weight: 500;">{st.session_state.username}</span>
        <span style="margin: 0 5px; color: #949494;">|</span>
        <span style="color: #666; font-size: 0.9rem;">{st.session_state.role}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Barre de navigation
nav_cols = st.columns(6)
with nav_cols[0]:
    if st.button("📊 Dashboard"):
        st.switch_page("pages/Dashboard.py")

with nav_cols[1]:
    if st.button("📈 Real Time Adherence"):
        st.switch_page("pages/Real_Time_Adherence.py")

with nav_cols[2]:
    if st.session_state.role == "admin" and st.button("👑 Administration"):
        st.switch_page("pages/Admin.py")

with nav_cols[3]:
    if st.button("📊 detection_anomalies"):
        st.switch_page("pages/detection_anomalies.py")

with nav_cols[4]:
    if st.button("📊 predictions"):
        st.switch_page("pages/predictions.py")

with nav_cols[5]:
    if st.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.switch_page("Home.py")
# Ligne de séparation
st.markdown('<hr style="margin: 1rem 0; border: none; height: 1px; background-color: #e0e0e0;">', unsafe_allow_html=True)

# Fonction pour formater les durées
def format_duration(duration_str):
    if not duration_str or duration_str == "0:00:00":
        return "0h 00m"
    try:
        parts = duration_str.split(":")
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return f"{hours}h {minutes}m"
        return duration_str
    except:
        return duration_str

# Fonction pour formater les nombres avec virgule
def format_decimal(value):
    try:
        # Si c'est déjà une chaîne avec virgule, la retourner telle quelle
        if isinstance(value, str) and ',' in value:
            return value
            
        # Sinon, convertir en float et formater avec virgule
        num_value = float(str(value).replace(',', '.'))
        # Diviser par 100 si la valeur est supérieure à 100 (pour corriger le problème de décimale manquante)
        if num_value > 100:
            num_value = num_value / 100
        return f"{num_value:.2f}".replace('.', ',')
    except:
        # En cas d'erreur, retourner la valeur telle quelle
        return value

# Fonction pour déterminer l'emoji selon la performance
def get_performance_emoji(value, metric_type):
    # Convertir la valeur en nombre si nécessaire
    try:
        if isinstance(value, str):
            numerical_value = float(value.replace(',', '.'))
        else:
            numerical_value = float(value)
            
        # Si la valeur semble être multipliée par 100, la diviser
        if numerical_value > 100 and metric_type == "prod":
            numerical_value = numerical_value / 100
    except:
        numerical_value = 0
    
    if metric_type == "prod":
        if numerical_value >= 15:
            return "🟢"  # excellent
        elif numerical_value >= 12:
            return "🔵"  # bon
        elif numerical_value >= 10:
            return "🟠"  # moyen
        else:
            return "🔴"  # faible
    elif metric_type == "occupation":
        try:
            if isinstance(value, str) and "%" in value:
                value = float(value.replace("%", ""))
            else:
                value = float(value)
                
            if value >= 90:
                return "🟢"  # excellent
            elif value >= 80:
                return "🔵"  # bon
            elif value >= 70:
                return "🟠"  # moyen
            else:
                return "🔴"  # faible
        except:
            return "⚪"
    return "⚪"

# Fonction pour parser les pourcentages
def parse_percentage(value):
    try:
        if isinstance(value, str) and "%" in value:
            return float(value.replace("%", ""))
        return float(value)
    except:
        return 0

# Fonction pour normaliser les valeurs de productivité (division par 100 si nécessaire)
def normalize_productivity(value):
    try:
        if isinstance(value, str):
            value = float(value.replace(',', '.'))
        else:
            value = float(value)
            
        # Si la valeur semble être multipliée par 100, la diviser
        if value > 100:
            return value / 100
        return value
    except:
        return value

# Connexion à Google Sheets et récupération des données
with st.spinner("Chargement des données depuis Google Sheets..."):
    try:
        client = connect_to_sheets()
        
        # Ouvrir le classeur Google Sheets
        spreadsheet = client.open("prod_data")
        
        # Récupérer la première feuille
        sheet1 = spreadsheet.sheet1
        data = sheet1.get_all_records()
        
        # Vérifier si des données ont été récupérées
        if not data:
            st.error("Aucune donnée n'a été trouvée dans la feuille Google Sheets.")
        else:
            # Convertir en DataFrame pour faciliter la manipulation
            df = pd.DataFrame(data)
            
            # Filtres dans la barre latérale
            with st.sidebar:
                st.markdown("""
                <div style="text-align: center; padding: 12px 0; margin-bottom: 20px; background: linear-gradient(90deg, #1a73e8 0%, #00bcd4 100%); color: white; border-radius: 8px; font-weight: 500; font-size: 16px;">
                    FILTRES
                </div>
                """, unsafe_allow_html=True)
                
                # Sélection de date
                if "Date" in df.columns:
                    st.markdown('<div class="sidebar-section-title">Date</div>', unsafe_allow_html=True)
                    dates = sorted(df["Date"].unique())
                    selected_date = st.selectbox("Sélectionner une date", dates)
                    filtered_df = df[df["Date"] == selected_date]
                else:
                    filtered_df = df
                    st.warning("Aucune colonne 'Date' trouvée")
                
                # Filtre par superviseur
                if "Tls" in df.columns:
                    st.markdown('<div class="sidebar-section-title">Superviseur</div>', unsafe_allow_html=True)
                    supervisors = sorted(filtered_df["Tls"].unique())
                    selected_supervisors = st.multiselect(
                        "Filtrer par superviseur",
                        options=supervisors,
                        default=supervisors
                    )
                    if selected_supervisors:
                        filtered_df = filtered_df[filtered_df["Tls"].isin(selected_supervisors)]
                
                # Options de tri
                st.markdown('<div class="sidebar-section-title">Tri</div>', unsafe_allow_html=True)
                sort_options = [
                    "Productivité nette (décroissant)",
                    "Productivité brute (décroissant)",
                    "Taux d'occupation (décroissant)",
                    "Nom (A-Z)"
                ]
                sort_options = [""] + sort_options
                sort_by = st.selectbox("Trier par", sort_options)
                
                # Appliquer le tri
                if "nette" in sort_by:
                    # Pour le tri, convertir les valeurs en nombres et les normaliser
                    filtered_df["Prod_nette_num"] = filtered_df["Prod nette"].apply(normalize_productivity)
                    filtered_df = filtered_df.sort_values("Prod_nette_num", ascending=False)
                elif "brute" in sort_by:
                    filtered_df["Prod_brute_num"] = filtered_df["Prod brute"].apply(normalize_productivity)
                    filtered_df = filtered_df.sort_values("Prod_brute_num", ascending=False)
                elif "occupation" in sort_by:
                    # Convertir le taux d'occupation en nombre pour le tri
                    filtered_df["Taux_num"] = filtered_df["Taux d'occupation"].apply(parse_percentage)
                    filtered_df = filtered_df.sort_values("Taux_num", ascending=False)
                elif "Nom (A-Z)" in sort_by:  # Tri par nom
                    filtered_df = filtered_df.sort_values("Nom Agent")
                
                # Bouton de rafraîchissement
                st.markdown('<div class="sidebar-section-title">Actions</div>', unsafe_allow_html=True)
                if st.sidebar.button("🔄 Rafraîchir les données"):
                    st.cache_data.clear()
                    st.rerun()
                    
            # Calculer les métriques
            num_employees = len(filtered_df)
            
            # Taux d'occupation moyen
            if "Taux d'occupation" in filtered_df.columns:
                avg_occupation = filtered_df["Taux d'occupation"].apply(parse_percentage).mean()
            else:
                avg_occupation = 0
            
            # Productivité moyenne - convertir les valeurs en nombres pour le calcul
            if "Prod brute" in filtered_df.columns:
                try:
                    prod_brute_values = filtered_df["Prod brute"].apply(normalize_productivity)
                    avg_prod_brute = prod_brute_values.mean()
                except:
                    avg_prod_brute = 0
            else:
                avg_prod_brute = 0
                
            if "Prod nette" in filtered_df.columns:
                try:
                    prod_nette_values = filtered_df["Prod nette"].apply(normalize_productivity)
                    avg_prod_nette = prod_nette_values.mean()
                except:
                    avg_prod_nette = 0
            else:
                avg_prod_nette = 0
            
            # Afficher les métriques avec le même format que les données d'origine (virgule comme séparateur décimal)
            avg_prod_brute_formatted = f"{avg_prod_brute:.2f}".replace('.', ',')
            avg_prod_nette_formatted = f"{avg_prod_nette:.2f}".replace('.', ',')
            
            # Légende des couleurs (ajoutée au début)
            st.markdown("""
            <div class="legend-container">
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #4caf50;"></div>
                    <div class="legend-label">Excellent: ≥15 (prod) / ≥90% (occupation)</div>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #1a73e8;"></div>
                    <div class="legend-label">Bon: ≥12 (prod) / ≥80% (occupation)</div>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #ff9800;"></div>
                    <div class="legend-label">Moyen: ≥10 (prod) / ≥70% (occupation)</div>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #f44336;"></div>
                    <div class="legend-label">Faible: <10 (prod) / <70% (occupation)</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Afficher un tableau de bord récapitulatif
            st.header("Indicateurs clés de performance")
            
            # Récupérer les emojis/couleurs pour les KPIs
            prod_brute_emoji = get_performance_emoji(avg_prod_brute, "prod")
            prod_nette_emoji = get_performance_emoji(avg_prod_nette, "prod")
            occupation_emoji = get_performance_emoji(avg_occupation, "occupation")
            
            # Afficher les métriques avec le style cohérent avec les autres pages
            metric_cols = st.columns(4)
            with metric_cols[0]:
                st.metric(
                    label="Nombre d'agents",
                    value=f"{num_employees}"
                )
            with metric_cols[1]:
                st.metric(
                    label="Taux d'occupation moyen",
                    value=f"{avg_occupation:.1f}%",
                    delta=f"{occupation_emoji}"
                )
            with metric_cols[2]:
                st.metric(
                    label="Productivité brute moyenne",
                    value=avg_prod_brute_formatted,
                    delta=f"{prod_brute_emoji}"
                )
            with metric_cols[3]:
                st.metric(
                    label="Productivité nette moyenne",
                    value=avg_prod_nette_formatted,
                    delta=f"{prod_nette_emoji}"
                )
            
            # Séparateur
            st.markdown("---")
            
            # Profils des employés
            st.header("Profils des employés")
            
            # Créer une grille pour les profils (3 colonnes)
            for i in range(0, len(filtered_df), 3):
                cols = st.columns(3)
                
                # Afficher jusqu'à 3 profils par ligne
                for j in range(3):
                    if i + j < len(filtered_df):
                        employee = filtered_df.iloc[i + j]
                        
                        # Récupérer les données de l'employé
                        nom = employee.get("Nom Agent", "Nom inconnu")
                        matricule = employee.get("Matricule RH", "")
                        file = employee.get("File", "")
                        
                        # Superviseur et opérations
                        tls = employee.get("Tls", "")
                        ops = employee.get("OPS", "")
                        
                        # Données de performance - formatage avec virgule
                        prod_brute = employee.get("Prod brute", 0)
                        prod_nette = employee.get("Prod nette", 0)
                        taux_occupation = employee.get("Taux d'occupation", "0%")
                        dmt = employee.get("DMT", "")
                        
                        # Emojis pour les performances
                        prod_brute_emoji = get_performance_emoji(prod_brute, "prod")
                        prod_nette_emoji = get_performance_emoji(prod_nette, "prod")
                        occupation_emoji = get_performance_emoji(taux_occupation, "occupation")
                        
                        # Formatage des valeurs avec virgule
                        prod_brute_display = format_decimal(prod_brute)
                        prod_nette_display = format_decimal(prod_nette)
                        
                        # Temps
                        temps_presence = format_duration(employee.get("Temps de présence", ""))
                        temps_travail = format_duration(employee.get("Temps de travail", ""))
                        appel_entrant = format_duration(employee.get("Appel entrant", ""))
                        en_attente = format_duration(employee.get("Attente", ""))
                        post_travail = format_duration(employee.get("Post-travail", ""))
                        break_time = format_duration(employee.get("Break", ""))
                        
                        # Afficher la carte pour cet employé
                        with cols[j]:
                            # Utiliser des éléments Streamlit natifs au lieu de HTML personnalisé
                            with st.container():
                                # En-tête avec style
                                st.markdown(f"""
                                <div style="background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%); 
                                         padding: 15px; border-radius: 10px; color: white; margin-bottom: 15px;">
                                    <h3 style="margin:0; font-size: 1.3rem;">{nom}</h3>
                                    <p style="margin:0; opacity: 0.9; font-size: 0.9rem;">Matricule: {matricule} | File: {file}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Expander pour les détails
                                with st.expander("Informations générales", expanded=True):
                                    st.markdown(f"""
                                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                                        <span style="margin-right: 10px;">👨‍💼</span>
                                        <div>
                                            <div style="font-size: 0.8rem; color: #6b7280;">Superviseur (TLS)</div>
                                            <div style="font-weight: 600;">{tls}</div>
                                        </div>
                                    </div>
                                    <div style="display: flex; align-items: center;">
                                        <span style="margin-right: 10px;">🔄</span>
                                        <div>
                                            <div style="font-size: 0.8rem; color: #6b7280;">Opérations (OPS)</div>
                                            <div style="font-weight: 600;">{ops}</div>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                with st.expander("Performance", expanded=True):
                                    # Déterminer les classes CSS pour les performances
                                    prod_brute_class = ""
                                    if prod_brute_emoji == "🟢":
                                        prod_brute_class = "excellent"
                                    elif prod_brute_emoji == "🔵":
                                        prod_brute_class = "good"
                                    elif prod_brute_emoji == "🟠":
                                        prod_brute_class = "average"
                                    elif prod_brute_emoji == "🔴":
                                        prod_brute_class = "poor"
                                        
                                    prod_nette_class = ""
                                    if prod_nette_emoji == "🟢":
                                        prod_nette_class = "excellent"
                                    elif prod_nette_emoji == "🔵":
                                        prod_nette_class = "good"
                                    elif prod_nette_emoji == "🟠":
                                        prod_nette_class = "average"
                                    elif prod_nette_emoji == "🔴":
                                        prod_nette_class = "poor"
                                        
                                    occupation_class = ""
                                    if occupation_emoji == "🟢":
                                        occupation_class = "excellent"
                                    elif occupation_emoji == "🔵":
                                        occupation_class = "good"
                                    elif occupation_emoji == "🟠":
                                        occupation_class = "average"
                                    elif occupation_emoji == "🔴":
                                        occupation_class = "poor"
                                    
                                    # Affichage avec mise en forme et valeurs formatées avec virgule
                                    st.markdown(f"""
                                    <div class="highlight-box {prod_brute_class}">
                                        <div style="font-size: 0.8rem; color: #6b7280;">Productivité brute</div>
                                        <div style="font-size: 1.1rem; font-weight: 600;">{prod_brute_emoji} {prod_brute_display}</div>
                                    </div>
                                    <div class="highlight-box {prod_nette_class}">
                                        <div style="font-size: 0.8rem; color: #6b7280;">Productivité nette</div>
                                        <div style="font-size: 1.1rem; font-weight: 600;">{prod_nette_emoji} {prod_nette_display}</div>
                                    </div>
                                    <div class="highlight-box {occupation_class}">
                                        <div style="font-size: 0.8rem; color: #6b7280;">Taux d'occupation</div>
                                        <div style="font-size: 1.1rem; font-weight: 600;">{occupation_emoji} {taux_occupation}</div>
                                    </div>
                                    <div class="highlight-box">
                                        <div style="font-size: 0.8rem; color: #6b7280;">DMT</div>
                                        <div style="font-size: 1.1rem; font-weight: 600;">⏱️ {dmt}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                with st.expander("Répartition du temps", expanded=True):
                                    # Créer une grille de 2x3 pour les temps
                                    time_cols1 = st.columns(2)
                                    with time_cols1[0]:
                                        st.markdown(f"""
                                        <div style="font-size: 0.8rem; color: #6b7280;">Temps de présence</div>
                                        <div style="font-size: 1.1rem; font-weight: 600;">⌛ {temps_presence}</div>
                                        """, unsafe_allow_html=True)
                                    with time_cols1[1]:
                                        st.markdown(f"""
                                        <div style="font-size: 0.8rem; color: #6b7280;">Temps de travail</div>
                                        <div style="font-size: 1.1rem; font-weight: 600;">⏰ {temps_travail}</div>
                                        """, unsafe_allow_html=True)
                                    
                                    time_cols2 = st.columns(2)
                                    with time_cols2[0]:
                                        st.markdown(f"""
                                        <div style="font-size: 0.8rem; color: #6b7280;">Appels entrants</div>
                                        <div style="font-size: 1.1rem; font-weight: 600;">📞 {appel_entrant}</div>
                                        """, unsafe_allow_html=True)
                                    with time_cols2[1]:
                                        st.markdown(f"""
                                        <div style="font-size: 0.8rem; color: #6b7280;">En attente</div>
                                        <div style="font-size: 1.1rem; font-weight: 600;">⏳ {en_attente}</div>
                                        """, unsafe_allow_html=True)
                                    
                                    time_cols3 = st.columns(2)
                                    with time_cols3[0]:
                                        st.markdown(f"""
                                        <div style="font-size: 0.8rem; color: #6b7280;">Post-travail</div>
                                        <div style="font-size: 1.1rem; font-weight: 600;">📝 {post_travail}</div>
                                        """, unsafe_allow_html=True)
                                    with time_cols3[1]:
                                        st.markdown(f"""
                                        <div style="font-size: 0.8rem; color: #6b7280;">Pause</div>
                                        <div style="font-size: 1.1rem; font-weight: 600;">☕ {break_time}</div>
                                        """, unsafe_allow_html=True)                              
    except Exception as e:
        st.error(f"Une erreur est survenue lors de la connexion à Google Sheets: {e}")
        st.info("Vérifiez que votre fichier 'credentials.json' est correctement configuré et que le nom du classeur 'prod_data' est exact.")

            
