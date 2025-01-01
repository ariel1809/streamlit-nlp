import streamlit as st
import ollama
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
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
lottie_similarity = load_lottiefile("animation/sentence.json")


def main():
    Navbar()

    # Titre de la page
    st.title("Vérification de Similarité de Phrases avec LLaMA 3.1")

    # Titre personnalisé dans la barre latérale
    st.sidebar.header("Sentence Similarity")

    # Afficher l'animation Lottie sous le titre
    with st.sidebar:
        st_lottie(lottie_similarity, speed=1, width=250, height=200, key="similarity-lottie")

    # Champ de texte pour les phrases utilisateur
    sentence_1 = st.text_area("Entrez la première phrase", height=100)
    sentence_2 = st.text_area("Entrez la deuxième phrase", height=100)

    # Bouton de calcul de similarité
    if st.button("Calculer la similarité"):
        if sentence_1 and sentence_2:
            with st.spinner("Calcul de la similarité en cours..."):
                try:
                    # Utiliser LLaMA pour générer les embeddings de chaque phrase
                    response_1 = ollama.chat(model='llama3.1', messages=[{'role': 'user', 'content': sentence_1}])
                    response_2 = ollama.chat(model='llama3.1', messages=[{'role': 'user', 'content': sentence_2}])

                    # Extraire les embeddings (l'output de la génération de LLaMA)
                    embedding_1 = np.array(response_1['message']['content'].split(), dtype=float)
                    embedding_2 = np.array(response_2['message']['content'].split(), dtype=float)

                    # Calcul de la similarité cosinus entre les embeddings des deux phrases
                    similarity = cosine_similarity([embedding_1], [embedding_2])

                    # Afficher la similarité
                    st.subheader("Résultat de la similarité")
                    st.write(f"La similarité entre les deux phrases est : {similarity[0][0]:.4f}")

                except Exception as e:
                    st.error(f"Erreur lors de la génération ou du calcul : {e}")
        else:
            st.warning("Veuillez entrer deux phrases pour comparer.")


if __name__ == '__main__':
    main()