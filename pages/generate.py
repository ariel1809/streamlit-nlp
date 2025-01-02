import json
import streamlit as st
from streamlit_lottie import st_lottie
from sidebar.nav import Navbar

st.set_page_config(layout="wide")

# Fonction pour charger un fichier JSON local
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Charger l'animation Lottie en local
lottie_text_generation = load_lottiefile("animation/generate.json")

if 'generating' not in st.session_state:
    st.session_state.generating = False

def stop_generation():
    st.session_state.generating = False

def main():
    Navbar()
    st.title("Générateur de texte avec LLaMA 3.1")

    st.sidebar.header("Text Generation")
    with st.sidebar:
        if lottie_text_generation:
            st_lottie(lottie_text_generation, speed=1, width=300, height=200, key="text-gen-lottie")
        else:
            st.error("Impossible de charger l'animation.")

    # Champ texte et bouton génération
    prompt = st.text_area("Entrez votre texte ici :", height=150)
    col1, col2 = st.columns([1, 1])

    with col1:
        if not st.session_state.generating and st.button("Générer"):
            if prompt:
                st.session_state.generating = True
            else:
                st.warning("Veuillez entrer un texte avant de générer.")

    if st.session_state.generating:
        with col2:
            if st.button("❌ Arrêter"):
                stop_generation()

if __name__ == '__main__':
    main()