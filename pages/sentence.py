import json
import numpy as np
import streamlit as st
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from sklearn.metrics.pairwise import cosine_similarity
from streamlit_lottie import st_lottie

from sidebar.nav import Navbar

# Configuration de la page
st.set_page_config(
    page_title="Sentence Similarity",
    layout="wide"
)


# Fonction pour charger une animation Lottie locale
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


# Charger l'animation Lottie
lottie_similarity = load_lottiefile("animation/sentence.json")

# Charger le modèle de similarité
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-mpnet-base-v2')


# Fonction de pooling pour obtenir les embeddings de phrase
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def main():
    Navbar()

    st.title("Vérification de Similarité de Phrases avec MPNet")

    st.sidebar.header("Sentence Similarity")
    with st.sidebar:
        st_lottie(lottie_similarity, speed=1, width=250, height=200, key="similarity-lottie")

    # Initialiser l'état pour les phrases secondaires
    if 'secondary_sentences' not in st.session_state:
        st.session_state.secondary_sentences = [""]

    # Phrase principale
    main_sentence = st.text_area("Entrez la phrase principale", height=100)

    # Interface dynamique pour les phrases secondaires
    st.subheader("Phrases secondaires")

    # Gestion dynamique des phrases secondaires
    to_remove = None
    for i, sentence in enumerate(st.session_state.secondary_sentences):
        cols = st.columns([4, 1])
        with cols[0]:
            st.session_state.secondary_sentences[i] = st.text_area(f"Phrase {i + 1}", sentence, key=f"sentence_{i}")
        with cols[1]:
            if st.button("Retirer", key=f"remove_{i}"):
                to_remove = i

    # Retirer la phrase si un bouton est cliqué
    if to_remove is not None:
        del st.session_state.secondary_sentences[to_remove]

    # Ajouter une nouvelle phrase secondaire
    if st.button("Ajouter une phrase secondaire"):
        st.session_state.secondary_sentences.append("")

    # Calcul de similarité
    if st.button("Calculer la similarité"):
        if main_sentence and st.session_state.secondary_sentences:
            with st.spinner("Calcul de la similarité en cours..."):
                try:
                    # Encoder la phrase principale
                    encoded_main = tokenizer(main_sentence, return_tensors='pt', padding=True, truncation=True)
                    with torch.no_grad():
                        main_output = model(**encoded_main)
                    main_embedding = mean_pooling(main_output, encoded_main['attention_mask'])

                    # Encoder toutes les phrases secondaires
                    encoded_secondary = tokenizer(st.session_state.secondary_sentences, return_tensors='pt',
                                                  padding=True, truncation=True)
                    with torch.no_grad():
                        secondary_output = model(**encoded_secondary)
                    secondary_embeddings = mean_pooling(secondary_output, encoded_secondary['attention_mask'])

                    # Normalisation des embeddings
                    main_embedding = F.normalize(main_embedding, p=2, dim=1)
                    secondary_embeddings = F.normalize(secondary_embeddings, p=2, dim=1)

                    # Calcul de la similarité cosinus
                    similarities = cosine_similarity(main_embedding, secondary_embeddings)

                    # Afficher les résultats sous forme de barre de progression avec pourcentage
                    st.subheader("Résultat de la similarité :")
                    for i, similarity in enumerate(similarities[0]):
                        percent_similarity = similarity.item() * 100
                        st.write(
                            f"**Phrase {i + 1}** : {st.session_state.secondary_sentences[i]} — **{percent_similarity:.2f}%**")
                        st.progress(float(similarity.item()))

                except Exception as e:
                    st.error(f"Erreur lors du calcul de la similarité : {e}")
        else:
            st.warning("Veuillez entrer une phrase principale et au moins une phrase secondaire.")


if __name__ == '__main__':
    main()