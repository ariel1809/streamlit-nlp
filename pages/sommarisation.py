import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie

from sidebar.nav import Navbar

# Configuration de la page
st.set_page_config(
    page_title="Sommarisation de texte",
    layout="wide"
)

# Fonction pour charger une animation Lottie locale
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Charger l'animation Lottie
lottie_summary = load_lottiefile("animation/summary.json")

# Configuration de l'API Hugging Face pour la sommarisation
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {
    "Authorization": "Bearer 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"
}

# Fonction pour envoyer une requête à l'API Hugging Face pour la sommarisation
def query(payload):
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()  # Lève une exception si la requête échoue
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de requête : {e}")
        return None
    except json.JSONDecodeError:
        st.error("Erreur lors du décodage JSON de la réponse de l'API.")
        return None

# Interface principale de l'application Streamlit
def main():
    Navbar()

    # Titre de l'application
    st.title("Sommarisation de texte avec BART")

    # Titre personnalisé dans la barre latérale
    st.sidebar.header("Sommarisation de texte")

    # Afficher l'animation Lottie sous le titre dans la barre latérale
    with st.sidebar:
        st_lottie(lottie_summary, speed=1, width=250, height=200, key="summary-lottie")

    # Champ de texte pour l'entrée utilisateur
    text_input = st.text_area("Entrez le texte à résumer :", height=150)

    # Bouton de sommarisation
    if st.button("Résumer"):
        if text_input:
            with st.spinner("Sommarisation en cours..."):
                try:
                    # Préparer les données pour l'API
                    payload = {"inputs": text_input}
                    response = query(payload)

                    # Vérifier si la réponse contient le résumé
                    if response and isinstance(response, list) and len(response) > 0 and 'summary_text' in response[0]:
                        summary = response[0]['summary_text']
                        st.subheader("Résumé :")
                        st.write(summary)
                    else:
                        st.error("Réponse invalide de l'API. Aucune sommarisation disponible.")
                except Exception as e:
                    st.error(f"Erreur lors de la sommarisation : {e}")
        else:
            st.warning("Veuillez entrer un texte avant de résumer.")

if __name__ == '__main__':
    main()