
# #################################################################code final 6
# import streamlit as st
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import pandas as pd

# # Configuration de la page
# st.set_page_config(
#     page_title="Administration",
#     page_icon="👑",
#     layout="wide",
# )

# # Vérifier si l'utilisateur est connecté
# if 'logged_in' not in st.session_state or not st.session_state.logged_in:
#     st.warning("⚠️ Vous devez vous connecter pour accéder à cette page.")
#     st.info("Retournez à la page d'accueil pour vous connecter.")
#     st.stop()

# # Vérifier si l'utilisateur a le rôle d'admin
# if st.session_state.role != "admin":
#     st.error("🚫 Accès refusé! Vous n'avez pas les droits administrateur nécessaires.")
#     st.info("Cette page est réservée aux administrateurs. Retournez au Dashboard utilisateur.")
#     st.stop()  # Arrêter l'exécution du reste du script si l'utilisateur n'est pas admin

# # Si le code continue ici, l'utilisateur est connecté et a le rôle admin
# st.title(f" Administration - Bienvenue {st.session_state.username}!")

# # Fonction pour se connecter à Google Sheets
# def connect_to_sheets():
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
#     client = gspread.authorize(creds)
#     return client

# # Connexion à Google Sheets et récupération des données
# client = connect_to_sheets()
# spreadsheet_id = "1Pk0p-lsFHUPUq8MUWcSNEQFPCFgl-C8TH73i76zqjbE"
# sheet = client.open_by_key(spreadsheet_id).sheet1
# data = sheet.get_all_records()

# # Interface d'administration
# st.header("Gestion des utilisateurs")

# # Créer un tableau des utilisateurs (sans afficher les mots de passe pour la sécurité)
# users_data = []
# for row in data:
#     users_data.append({
#         "Nom d'utilisateur": row['username'],
#         "Rôle": row['role']
#     })

# # Afficher les données dans un tableau interactif
# st.dataframe(users_data)

# # Ajout d'un nouvel utilisateur (formulaire)
# st.subheader("Ajouter un nouvel utilisateur")
# with st.form("add_user_form"):
#     new_username = st.text_input("Nom d'utilisateur")
#     new_password = st.text_input("Mot de passe", type="password")
#     new_role = st.selectbox("Rôle", options=["user", "admin"])
#     submit_button = st.form_submit_button("Ajouter l'utilisateur")
    
#     if submit_button:
#         if new_username and new_password:
#             # Vérifier si l'utilisateur existe déjà
#             user_exists = any(row['username'] == new_username for row in data)
            
#             if user_exists:
#                 st.error(f"L'utilisateur '{new_username}' existe déjà!")
#             else:
#                 # Ajouter le nouvel utilisateur
#                 try:
#                     new_row = [new_username, new_password, new_role]
#                     sheet.append_row(new_row)
#                     st.success(f"Utilisateur '{new_username}' ajouté avec succès!")
#                     st.rerun()  # Recharger la page pour voir le nouvel utilisateur
#                 except Exception as e:
#                     st.error(f"Erreur lors de l'ajout de l'utilisateur: {e}")
#         else:
#             st.warning("Veuillez remplir tous les champs!")

# #modifier un utilisateur

# st.subheader("Modifier un utilisateur existant")
# user_to_edit = st.selectbox("Sélectionner un utilisateur à modifier", options=[row['username'] for row in data], key="edit_user")

# if user_to_edit:
#     # Récupérer les données de l'utilisateur sélectionné
#     selected_user = next((row for row in data if row['username'] == user_to_edit), None)
    
#     if selected_user:
#         with st.form("edit_user_form"):
#             # Le nom d'utilisateur n'est pas modifiable
#             st.text_input("Nom d'utilisateur", value=selected_user['username'], disabled=True)
            
#             # Nouveau mot de passe (vide = ne pas changer)
#             new_password = st.text_input("Nouveau mot de passe (laisser vide pour ne pas modifier)", type="password")
            
#             # Rôle actuel et option pour le modifier
#             current_role = selected_user['role']
#             new_role = st.selectbox("Rôle", options=["user", "admin"], index=0 if current_role == "user" else 1)
            
#             submit = st.form_submit_button("Mettre à jour")
            
#             if submit:
#                 try:
#                     # Trouver la ligne de l'utilisateur
#                     for i, row in enumerate(data, start=2):
#                         if row['username'] == user_to_edit:
#                             # Préparer les données modifiées
#                             row_data = [user_to_edit]
                            
#                             # Mettre à jour le mot de passe si spécifié
#                             if new_password:
#                                 row_data.append(new_password)
#                             else:
#                                 row_data.append(selected_user['password'])
                            
#                             # Ajouter le rôle
#                             row_data.append(new_role)
                            
#                             # Mettre à jour la ligne
#                             sheet.update(f'A{i}:C{i}', [row_data])
#                             st.success("Utilisateur mis à jour avec succès!")
#                             st.rerun()
#                             break
#                 except Exception as e:
#                     st.error(f"Erreur lors de la mise à jour: {e}")

# # Fonctionnalité de suppression d'utilisateur
# st.subheader("Supprimer un utilisateur")
# usernames = [row['username'] for row in data]
# username_to_delete = st.selectbox("Sélectionnez un utilisateur à supprimer", options=usernames)

# if st.button("Supprimer l'utilisateur"):
#     # Confirmer la suppression
#     confirm = st.checkbox("Je confirme la suppression de cet utilisateur")
    
#     if confirm:
#         try:
#             # Trouver l'index de l'utilisateur dans la feuille
#             for i, row in enumerate(data, start=2):  # start=2 car Google Sheets commence à 1 et il y a un en-tête
#                 if row['username'] == username_to_delete:
#                     sheet.delete_rows(i)
#                     st.success(f"Utilisateur '{username_to_delete}' supprimé avec succès!")
#                     st.rerun()  # Recharger la page
#                     break
#         except Exception as e:
#             st.error(f"Erreur lors de la suppression: {e}")

# #recherche des utilisateurs
# st.subheader("Rechercher des utilisateurs")
# col1, col2 = st.columns(2)
# with col1:
#     search_term = st.text_input("Rechercher par nom d'utilisateur", "")
# with col2:
#     role_filter = st.selectbox("Filtrer par rôle", options=["Tous", "admin", "user"])

# # Appliquer la recherche et le filtrage
# filtered_data = []
# for row in data:
#     if search_term.lower() in row['username'].lower():
#         if role_filter == "Tous" or row['role'] == role_filter:
#             filtered_data.append(row)

# # Afficher les résultats
# st.dataframe(
#     pd.DataFrame([{
#         "Nom d'utilisateur": row['username'],
#         "Rôle": row['role'],
#     } for row in filtered_data])
# )

# ############### Statistiques
# st.header("Statistiques du système")
# col1, col2,col3 = st.columns(3)
# with col1:
#     st.metric(label="Nombre total d'utilisateurs", value=len(data))
# with col2:
#     admin_count = sum(1 for row in data if row['role'] == 'admin')
#     user_count = len(data) - admin_count
#     st.metric(label="Admins", value=admin_count)
# with col3:
#     st.metric(label="Users", value=user_count)

# # Bouton de déconnexion dans la barre latérale


# if st.button("Retour au Dashboard"):
#     st.switch_page("pages/Dashboard.py")

# if st.button("Déconnexion"):
#     st.session_state.logged_in = False
#     st.session_state.username = ""
#     st.session_state.role = ""
#     st.switch_page("Home.py")  # Redirection vers la page d'accueil





import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Administration",
    page_icon="👑",
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
    
    /* Fond global */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Style des cartes */
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
    }
    
    .admin-card {
        border-top: 4px solid #ff5722;
    }
    
    .user-card {
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
    
    .delete-button>button {
        background-color: #f44336;
    }
    
    .delete-button>button:hover {
        background-color: #d32f2f;
    }
    
    /* Style des formulaires */
    div[data-testid="stForm"] {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
    }
    
    .stTextInput > div > div > input, 
    .stSelectbox > div > div,
    div[data-baseweb="input"] {
        border-radius: 6px;
        transition: border 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1a73e8;
        box-shadow: 0 0 0 2px rgba(26, 115, 232, 0.2);
    }
    
    /* Style des tableaux */
    div[data-testid="stDataFrame"] > div {
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        overflow: hidden;
    }
    
    div[data-testid="stDataFrame"] th {
        background-color: #f5f7fa;
        font-weight: 600;
        color: #424242;
    }
    
    div[data-testid="stDataFrame"] tr:nth-of-type(even) {
        background-color: #f9f9f9;
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
    }
    
    /* Animation de transition */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .admin-container {
        animation: fadeIn 0.5s ease forwards;
    }
    
    /* Alertes et messages */
    div[data-testid="stAlert"] {
        border-radius: 8px;
        font-size: 0.9rem;
    }
    
    /* Badges pour les rôles */
    .role-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
        color: white;
        font-weight: 500;
    }
    .role-admin {
        background-color: #ff5722;
    }
    .role-user {
        background-color: #1a73e8;
    }
</style>
""", unsafe_allow_html=True)

# Vérifier si l'utilisateur est connecté
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Vous devez vous connecter pour accéder à cette page.")
    st.info("Retournez à la page d'accueil pour vous connecter.")
    st.stop()

# Vérifier si l'utilisateur a le rôle d'admin
if st.session_state.role != "admin":
    st.error("🚫 Accès refusé! Vous n'avez pas les droits administrateur nécessaires.")
    st.info("Cette page est réservée aux administrateurs. Retournez au Dashboard utilisateur.")
    st.stop()

# Container principal avec animation
st.markdown('<div class="admin-container">', unsafe_allow_html=True)

# En-tête de la page avec style
st.markdown(f"""
<div style="display: flex; align-items: center; margin-bottom: 1rem;">
    <div style="display: flex; align-items: center;">
        <div style="font-size: 2.5rem; margin-right: 10px; color: #ff5722;">👑</div>
        <h1 style="margin: 0; font-size: 2rem;">Administration</h1>
    </div>
    <div style="margin-left: auto; padding: 8px 15px; background-color: #fff3e0; border-radius: 30px; display: flex; align-items: center;">
        <span style="color: #ff5722; margin-right: 8px;">👤</span>
        <span style="font-weight: 500;">{st.session_state.username}</span>
        <span style="margin: 0 5px; color: #949494;">|</span>
        <span style="color: #ff5722; font-size: 0.9rem; font-weight: 500;">Admin</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Barre de navigation
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("📊 Dashboard"):
        st.switch_page("Dashboard.py")
        
with col2:
    if st.button("📈 Real Time Adherence"):
        st.switch_page("Real_Time_Adherence.py")
        
with col3:
    if st.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.switch_page("Home.py")

# Ligne de séparation
st.markdown('<hr style="margin: 1rem 0; border: none; height: 1px; background-color: #e0e0e0;">', unsafe_allow_html=True)

# Fonction pour se connecter à Google Sheets
def connect_to_sheets():
    scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        # Utiliser les credentials pour la feuille users
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client

# Connexion à Google Sheets et récupération des données
with st.spinner("Chargement des données..."):
    client = connect_to_sheets()
      # Ouvrir le classeur Google Sheets "users"
    spreadsheet = client.open("users_data")  # Remplacez "users" par le nom exact de votre feuille de calcul
    # Récupérer la première feuille
    sheet1 = spreadsheet.sheet1
    data = sheet1.get_all_records()
  

# Tableau de bord d'administration
st.markdown("""
<div class="card">
    <h2 style="margin-top: 0;">Tableau de bord d'administration</h2>
    <p style="color: #666; margin-bottom: 20px;">
        Bienvenue dans le panneau d'administration. Vous pouvez gérer les utilisateurs et consulter les statistiques du système.
    </p>
</div>
""", unsafe_allow_html=True)

# Statistiques sur les utilisateurs
st.markdown("## Statistiques du système")
stat_cols = st.columns(3)

admin_count = sum(1 for row in data if row['role'] == 'admin')
user_count = len(data) - admin_count

# Affichage des métriques avec styles personnalisés
with stat_cols[0]:
    st.metric(
        label="Nombre total d'utilisateurs",
        value=len(data),
        delta=None
    )
with stat_cols[1]:
    st.metric(
        label="Administrateurs",
        value=admin_count,
        delta=None
    )
with stat_cols[2]:
    st.metric(
        label="Utilisateurs standard",
        value=user_count,
        delta=None
    )

# Ajout d'un graphique pour visualiser la répartition des rôles
pie_data = pd.DataFrame({
    "Rôle": ["Administrateurs", "Utilisateurs standard"],
    "Nombre": [admin_count, user_count]
})

fig = px.pie(
    pie_data, 
    values='Nombre', 
    names='Rôle',
    color='Rôle',
    color_discrete_map={
        'Administrateurs': '#ff5722',
        'Utilisateurs standard': '#1a73e8'
    },
    hole=0.6
)
fig.update_layout(
    title=None,
    margin=dict(t=0, b=0, l=0, r=0),
    legend_title=None,
    font=dict(family="Poppins, sans-serif"),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
fig.update_traces(
    textinfo='percent+label',
    textposition='outside',
    marker=dict(line=dict(color='#ffffff', width=2))
)

st.plotly_chart(fig, use_container_width=True)

# Gestion des utilisateurs
st.markdown("## Gestion des utilisateurs")

# Onglets pour la gestion des utilisateurs
user_tabs = st.tabs(["📋 Liste des utilisateurs", "➕ Ajouter un utilisateur", "✏️ Modifier un utilisateur", "🔍 Rechercher"])

# Onglet 1: Liste des utilisateurs
with user_tabs[0]:
    # Créer un tableau des utilisateurs sans les mots de passe
    users_data = []
    for row in data:
        role_class = "role-admin" if row['role'] == 'admin' else "role-user"
        users_data.append({
            "Nom d'utilisateur": row['username'],
            "Rôle": f"<span class='role-badge {role_class}'>{row['role']}</span>"
        })
    
    # Convertir en DataFrame pour l'affichage
    df_users = pd.DataFrame(users_data)
    
    # Afficher le tableau avec formatage HTML
    st.markdown("### Liste complète des utilisateurs")
    st.write(df_users.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    # Section de suppression d'utilisateur
    st.markdown("### Supprimer un utilisateur")

    delete_cols = st.columns([3, 2])
    with delete_cols[0]:
        username_to_delete = st.selectbox(
            "Sélectionnez un utilisateur à supprimer",
            options=[row['username'] for row in data],
            key="delete_user"
        )
    
    with delete_cols[1]:
        st.markdown('<div class="delete-button">', unsafe_allow_html=True)
        delete_button = st.button("🗑️ Supprimer l'utilisateur")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if delete_button:
        # Confirmer la suppression
        st.warning("⚠️ Cette action est irréversible. Êtes-vous sûr de vouloir supprimer cet utilisateur?")
        confirm = st.checkbox("Je confirme la suppression de cet utilisateur")
        
        if confirm:
            try:
                # Trouver l'index de l'utilisateur dans la feuille
                for i, row in enumerate(data, start=2):  # Google Sheets commence à 1 + en-tête
                    if row['username'] == username_to_delete:
                        sheet1.delete_rows(i)
                        st.success(f"✅ Utilisateur '{username_to_delete}' supprimé avec succès!")
                        st.rerun()  # Recharger la page
                        break
            except Exception as e:
                st.error(f"❌ Erreur lors de la suppression: {e}")

# Onglet 2: Ajouter un nouvel utilisateur
with user_tabs[1]:
    st.markdown("### Ajouter un nouvel utilisateur")
    
    with st.form("add_user_form"):
        st.markdown("""
        <p style="color: #666; margin-bottom: 15px;">
            Complétez le formulaire ci-dessous pour créer un nouvel utilisateur.
        </p>
        """, unsafe_allow_html=True)
        
        new_username = st.text_input("Nom d'utilisateur")
        new_password = st.text_input("Mot de passe", type="password")
        
        role_options = ["user", "admin"]
        new_role = st.selectbox(
            "Rôle",
            options=role_options,
            index=0,
            format_func=lambda x: "Administrateur" if x == "admin" else "Utilisateur standard"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("➕ Ajouter l'utilisateur")
        
        if submit_button:
            if new_username and new_password:
                # Vérifier si l'utilisateur existe déjà
                user_exists = any(row['username'] == new_username for row in data)
                
                if user_exists:
                    st.error(f"❌ L'utilisateur '{new_username}' existe déjà!")
                else:
                    # Ajouter le nouvel utilisateur
                    try:
                        new_row = [new_username, new_password, new_role]
                        sheet1.append_row(new_row)
                        st.success(f"✅ Utilisateur '{new_username}' ajouté avec succès!")
                        st.rerun()  # Recharger la page
                    except Exception as e:
                        st.error(f"❌ Erreur lors de l'ajout de l'utilisateur: {e}")
            else:
                st.warning("⚠️ Veuillez remplir tous les champs!")

# Onglet 3: Modifier un utilisateur existant
with user_tabs[2]:
    st.markdown("### Modifier un utilisateur existant")
    
    user_to_edit = st.selectbox(
        "Sélectionner un utilisateur à modifier",
        options=[row['username'] for row in data],
        key="edit_user"
    )
    
    if user_to_edit:
        # Récupérer les données de l'utilisateur sélectionné
        selected_user = next((row for row in data if row['username'] == user_to_edit), None)
        
        if selected_user:
            with st.form("edit_user_form"):
                st.markdown(f"""
                <p style="color: #666; margin-bottom: 15px;">
                    Modification de l'utilisateur <b>{user_to_edit}</b>
                </p>
                """, unsafe_allow_html=True)
                
                # Le nom d'utilisateur n'est pas modifiable
                st.text_input("Nom d'utilisateur", value=selected_user['username'], disabled=True)
                
                # Nouveau mot de passe (vide = ne pas changer)
                new_password = st.text_input(
                    "Nouveau mot de passe (laisser vide pour ne pas modifier)",
                    type="password",
                    help="Laissez ce champ vide si vous ne souhaitez pas modifier le mot de passe"
                )
                
                # Rôle actuel et option pour le modifier
                current_role = selected_user['role']
                role_options = ["user", "admin"]
                role_index = 1 if current_role == "admin" else 0
                
                new_role = st.selectbox(
                    "Rôle",
                    options=role_options,
                    index=role_index,
                    format_func=lambda x: "Administrateur" if x == "admin" else "Utilisateur standard"
                )
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    submit = st.form_submit_button("✏️ Mettre à jour")
                
                if submit:
                    try:
                        # Trouver la ligne de l'utilisateur
                        for i, row in enumerate(data, start=2):
                            if row['username'] == user_to_edit:
                                # Préparer les données modifiées
                                row_data = [user_to_edit]
                                
                                # Mettre à jour le mot de passe si spécifié
                                if new_password:
                                    row_data.append(new_password)
                                else:
                                    row_data.append(selected_user['password'])
                                
                                # Ajouter le rôle
                                row_data.append(new_role)
                                
                                # Mettre à jour la ligne
                                sheet1.update(f'A{i}:C{i}', [row_data])
                                st.success("✅ Utilisateur mis à jour avec succès!")
                                st.rerun()
                                break
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la mise à jour: {e}")

# Onglet 4: Rechercher des utilisateurs
with user_tabs[3]:
    st.markdown("### Rechercher des utilisateurs")
    
    search_cols = st.columns(2)
    with search_cols[0]:
        search_term = st.text_input("Rechercher par nom d'utilisateur", "")
    
    with search_cols[1]:
        role_filter = st.selectbox(
            "Filtrer par rôle",
            options=["Tous", "admin", "user"],
            format_func=lambda x: "Administrateur" if x == "admin" else ("Utilisateur standard" if x == "user" else x)
        )
    
    # Appliquer la recherche et le filtrage
    filtered_data = []
    for row in data:
        if search_term.lower() in row['username'].lower():
            if role_filter == "Tous" or row['role'] == role_filter:
                filtered_data.append(row)
    
    # Afficher les résultats
    if filtered_data:
        st.markdown(f"### Résultats ({len(filtered_data)} utilisateurs trouvés)")
        
        # Formater les résultats avec badges de rôle
        search_results = []
        for row in filtered_data:
            role_class = "role-admin" if row['role'] == 'admin' else "role-user"
            search_results.append({
                "Nom d'utilisateur": row['username'],
                "Rôle": f"<span class='role-badge {role_class}'>{row['role']}</span>"
            })
        
        # Afficher le tableau des résultats
        df_results = pd.DataFrame(search_results)
        st.write(df_results.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        if search_term or role_filter != "Tous":
            st.info("Aucun utilisateur ne correspond aux critères de recherche.")
        else:
            st.info("Entrez des critères de recherche pour trouver des utilisateurs.")

# Fonctionnalités supplémentaires et documentation
with st.expander("🔍 Aide et fonctionnalités avancées"):
    st.markdown("""
    ### Guide d'administration
    
    Ce panneau d'administration vous permet de gérer les utilisateurs et de surveiller l'activité du système.
    
    #### Fonctionnalités disponibles:
    
    - **Gestion des utilisateurs**: Ajoutez, modifiez et supprimez des utilisateurs
    - **Statistiques**: Consultez les métriques clés du système
    - **Recherche avancée**: Filtrez et trouvez rapidement des informations spécifiques
    
    #### Bonnes pratiques:
    
    - Limitez le nombre d'administrateurs à ce qui est strictement nécessaire
    - Utilisez des mots de passe forts pour tous les comptes, surtout les comptes administrateur
    - Vérifiez régulièrement la liste des utilisateurs pour vous assurer qu'elle est à jour
    
    Pour obtenir de l'aide supplémentaire, contactez l'équipe technique.
    """)

# Pied de page
st.markdown("""
<div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #e0e0e0; text-align: center; color: #9e9e9e; font-size: 0.8rem;">
    Panel d'administration v1.0 | © 2025 Système de Gestion d'Adhérence
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Fermeture du container principal
