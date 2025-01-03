import streamlit as st
import ollama
from sidebar.nav import Navbar
import json
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Text Generation",
    layout="wide"
)

# Fonction pour charger une animation Lottie locale
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


# Charger l'animation Lottie
lottie_similarity = load_lottiefile("animation/generate.json")

def main():
    Navbar()
    # Titre de l'application
    st.title("Générateur de texte avec LLaMA 3.1")

    # Titre personnalisé dans la barre latérale
    st.sidebar.header("Text Generation")

    # Afficher l'animation Lottie sous le titre
    with st.sidebar:
        st_lottie(lottie_similarity, speed=1, width=250, height=200, key="generate-lottie")

    # Champ de texte pour l'entrée utilisateur
    prompt = st.text_area("Entrez votre texte ici :", height=150)

    # Bouton de génération
    if st.button("Générer"):
        if prompt:
            with st.spinner("Génération en cours..."):
                try:
                    # Utiliser un générateur pour la génération en flux
                    response = ollama.chat(model='llama3.1', messages=[{'role': 'user', 'content': prompt}],
                                           stream=True)

                    # Fonction de flux pour affichage en temps réel
                    def stream_text():
                        for chunk in response:
                            yield chunk['message']['content']

                    # Affiche le texte au fur et à mesure
                    st.subheader("Texte généré :")
                    st.write_stream(stream_text())

                except Exception as e:
                    st.error(f"Erreur lors de la génération : {e}")
        else:
            st.warning("Veuillez entrer un texte avant de générer.")


if __name__ == '__main__':
    main()
