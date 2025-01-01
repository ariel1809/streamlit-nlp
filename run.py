import streamlit as st
import requests

# Backend URL
backend_url = "http://127.0.0.1:8000"

# Fonction pour afficher la page de login
def show_login_page():
    st.subheader("Login Section")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type='password', key="login_password")
    if st.button("Login"):
        response = requests.post(f"{backend_url}/login/", data={"email": email, "password": password})
        if response.status_code == 200:
            st.success("Login successful")
        else:
            st.error("Invalid credentials")
    if st.button("Pas encore de compte? Inscrivez-vous"):
        st.session_state.page = "register"

# Fonction pour afficher la page de register
def show_register_page():
    st.subheader("Register Section")
    name = st.text_input("Name", key="register_name")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type='password', key="register_password")
    confirm_password = st.text_input("Confirm Password", type='password', key="register_confirm_password")
    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match")
        else:
            response = requests.post(f"{backend_url}/register/", json={"name": name, "email": email, "password": password})
            if response.status_code == 200:
                st.success("User registered successfully")
                st.session_state.page = "login"
            else:
                st.error(response.json().get("detail"))
    if st.button("Retour à la connexion"):
        st.session_state.page = "login"

# Fonction principale pour afficher les pages
def main():
    st.title("Application d'authentification")

    if "page" not in st.session_state:
        st.session_state.page = "login"

    if st.session_state.page == "login":
        show_login_page()
    elif st.session_state.page == "register":
        show_register_page()

if __name__ == '__main__':
    main()