import streamlit as st
import json
from streamlit_lottie import st_lottie
from sidebar.nav import Navbar

# Configuration de la page
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

st.set_page_config(
    page_title="Accueil - Application NLP",
    layout="wide"
)

# Charger l'animation Lottie
lottie_home = load_lottiefile("animation/home.json")

def main():
    Navbar()

    # Fonction pour créer une carte avec icône, titre et description
    def create_card(icon_class, title, description):
        card_html = f"""
        <div style="background-color: #f9f9f9; padding: 20px; border-radius: 16px; 
                    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); margin-bottom: 20px;
                    display: flex; align-items: center;">
            <div style="margin-right: 15px;">
                <i class="{icon_class}" style="font-size: 50px;"></i>
            </div>
            <div>
                <h5 style="margin: 0px; padding: 0px;">{title}</h5>
                <p style="margin: 5px 0px;">{description}</p>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    # Titre de la page d'accueil
    st.markdown('<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">',
                unsafe_allow_html=True)
    st.title("🚀 Bienvenue sur l'application NLP avancée")

    # Titre personnalisé dans la barre latérale
    st.sidebar.header("Accueil")

    # Afficher l'animation Lottie sous le titre
    with st.sidebar:
        st_lottie(lottie_home, speed=1, width=250, height=200, key="home-lottie")

    # Titre de la section
    st.markdown('### 🛠️ Fonctionnalités de application:', unsafe_allow_html=True)

    # Trois colonnes pour organiser les cartes
    features = st.columns(2)

    # Génération de texte
    with features[0]:
        create_card("bi bi-pencil-square",
                    "Génération de texte",
                    "Générer des paragraphes cohérents et créatifs à partir d'une simple entrée utilisateur.")

    # Sommarisation
    with features[1]:
        create_card("bi bi-journal-text",
                    "Sommarisation de texte",
                    "Résumer automatiquement de longs textes tout en conservant les idées principales.")

    # Similarité de phrases
    with features[0]:
        create_card("bi bi-graph-up-arrow",
                    "Similarité de phrases",
                    "Comparer la similarité entre deux phrases pour évaluer leur degré de correspondance.")

    # Text-to-Speech (Synthèse vocale)
    with features[1]:
        create_card("bi bi-mic",
                    "Text-to-Speech",
                    "Convertir du texte en audio pour une expérience plus immersive.")

    # Footer
    st.markdown("""
        <div style="text-align: center; margin-top: 50px; font-size: 14px; color: grey;">
            © 2025 - Application NLP par Ariel Kuetche
        </div>
    """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()