import streamlit as st
import requests
from sidebar.nav import Navbar
from streamlit_extras.switch_page_button import switch_page

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Home",
    layout="wide",
)


def main():
    Navbar()

    st.title("Se connecter")

    # Titre personnalisé dans la barre latérale
    st.sidebar.header("🔍 Sommarisation")

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        response = requests.post(f"{BASE_URL}/login/", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            token = response.json()['access_token']
            st.success("Connexion réussie!")
            st.write("Token JWT : ", token)
        else:
            st.error("Identifiants incorrects")

    st.markdown("Pas encore inscrit ? [Créer un compte](http://localhost:8501/register)", unsafe_allow_html=True)

    if st.button("Créer un compte"):
        switch_page("register")


if __name__ == '__main__':
    main()