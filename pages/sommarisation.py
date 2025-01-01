import streamlit as st
import ollama
import json
from streamlit_lottie import st_lottie
from sidebar.nav import Navbar

# Configuration de la page
st.set_page_config(
    layout="wide"
)

# Fonction pour charger une animation Lottie locale
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Charger l'animation Lottie
lottie_summary = load_lottiefile("animation/summary.json")

def main():
    Navbar()

    # Titre de l'application
    st.title("🔍 Sommarisation de texte avec LLaMA 3.1")

    # Titre personnalisé dans la barre latérale
    st.sidebar.header("🔍 Sommarisation")

    # Afficher l'animation Lottie sous le titre dans la barre latérale
    with st.sidebar:
        st_lottie(lottie_summary, speed=1, width=250, height=200, key="summary-lottie")

    # Champ de texte pour l'entrée utilisateur
    text_input = st.text_area("Entrez le texte à résumer :", height=150)

    # Bouton de sommarisation
    if st.button("📝 Résumer"):
        if text_input:
            with st.spinner("Sommarisation en cours..."):
                try:
                    response = ollama.chat(model='llama3.1', messages=[{'role': 'user', 'content': f"Summarize this text: {text_input}"}])
                    # Afficher la réponse du modèle
                    st.subheader("Résumé :")
                    st.write(response['message']['content'])
                except Exception as e:
                    st.error(f"Erreur lors de la sommarisation : {e}")
        else:
            st.warning("Veuillez entrer un texte avant de résumer.")

if __name__ == '__main__':
    main()