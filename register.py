import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Inscription", page_icon="📝", layout="centered")

st.title("Créer un compte")

new_username = st.text_input("Nom d'utilisateur")
new_password = st.text_input("Mot de passe", type="password")

if st.button("S'inscrire"):
    response = requests.post(f"{BASE_URL}/register/", json={
        "username": new_username,
        "password": new_password
    })

    if response.status_code == 200:
        st.success("Inscription réussie! Connecte-toi maintenant.")
        st.switch_page("login")
    else:
        st.error(response.json().get("detail"))

st.markdown("Déjà inscrit ? [Se connecter](#)", unsafe_allow_html=True)
if st.button("Se connecter ici"):
    st.switch_page("login")