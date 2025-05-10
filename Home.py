
# ######################################code final 
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuration de la page
st.set_page_config(
    page_title="Système de Connexion",
    page_icon="🔐",
    layout="centered"
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
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Style des cartes */
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* Style des boutons */
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
        height: 2.8rem;
    }
    
    .stButton>button:hover {
        background-color: #0d47a1;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Style du formulaire */
    div[data-testid="stForm"] {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        transition: border 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1a73e8;
        box-shadow: 0 0 0 2px rgba(26, 115, 232, 0.2);
    }
    
    /* Titres et textes */
    h1 {
        color: #212121;
        font-weight: 600;
        margin-bottom: 2rem;
        font-size: 2.5rem;
        text-align: center;
    }
    
    /* Alertes et messages */
    .element-container div[data-testid="stAlert"] {
        border-radius: 10px;
        padding: 0.8rem;
        margin: 1rem 0;
    }
    
    /* Logo et branding */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    
    .logo {
        width: 100px;
        height: 100px;
        background-color: #1a73e8;
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        box-shadow: 0 8px 15px rgba(26, 115, 232, 0.3);
    }
    
    /* Animation d'entrée */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .login-container {
        animation: fadeIn 0.8s ease forwards;
    }
    
    /* Style du bas de page */
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #757575;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des variables de session
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'role' not in st.session_state:
    st.session_state.role = ""

# Fonction pour vérifier les identifiants
def check_credentials(username, password):
    scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        # Utiliser les credentials pour la feuille users
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
        
        # Ouvrir le classeur Google Sheets "users"
    spreadsheet = client.open("users_data")  # Remplacez "users" par le nom exact de votre feuille de calcul
        
        # Récupérer la première feuille
    sheet1 = spreadsheet.sheet1
    data = sheet1.get_all_records()
    
    # Vérifier les identifiants
    for row in data:
        if row['username'] == username and row['password'] == password:
            return True, row['role']
    return False, None

# Logo et en-tête
st.markdown('<div class="login-container">', unsafe_allow_html=True)
st.markdown('<div class="logo-container"><div class="logo">🔐</div></div>', unsafe_allow_html=True)
st.title("Système d'adhérence")

# Si déjà connecté, afficher un message et proposer d'aller au dashboard
if st.session_state.logged_in:
    st.markdown(f"""
    <div class="card">
        <h3 style="text-align: center; margin-bottom: 1.5rem;">
            Bienvenue, <span style="color: #1a73e8; font-weight: 600;">{st.session_state.username}</span> !
        </h3>
        <p style="text-align: center; margin-bottom: 2rem;">
            Vous êtes connecté en tant que {st.session_state.role}.
            Choisissez votre destination ci-dessous.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Tableau de bord"):
            st.switch_page("Dashboard.py")
    
    # N'afficher le bouton Admin que pour les admins
    with col2:
        if st.session_state.role == "admin":
            if st.button("👑 Administration"):
                st.switch_page("pages/Admin.py")
        else:
            if st.button("📈 Real Time Adherence"):
                st.switch_page("Real_Time_Adherence.py")
    
    # Bouton de déconnexion
    if st.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()
else:
    # Formulaire de connexion
    st.markdown("<p style='text-align: center; margin-bottom: 2rem;'>Connectez-vous pour accéder au système</p>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown("<h3 style='margin-bottom: 1.5rem; font-size: 1.2rem;'>Identifiants</h3>", unsafe_allow_html=True)
        
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button("SE CONNECTER")
        
        if submit:
            authenticated, role = check_credentials(username, password)
            if authenticated:
                # Enregistrer dans la session
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                
                # Message de réussite
                st.success("Connexion réussie ! Redirection...")
                
                # Rediriger automatiquement selon le rôle
                if role == "admin":
                    st.switch_page("pages/Admin.py")
                else:
                    st.switch_page("Dashboard.py")
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect")

# Pied de page
st.markdown('<div class="footer">© 2025 Système de Gestion d\'Adhérence. Tous droits réservés.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
