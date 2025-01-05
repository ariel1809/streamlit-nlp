import json
import requests
import streamlit as st
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

# Configuration de l'API Hugging Face
API_URL = "https://api-inference.huggingface.co/models/cointegrated/rubert-tiny2"
HEADERS = {
    "Authorization": "Bearer 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"  # Remplacer par ton token
}

# Fonction pour envoyer une requête à l'API Hugging Face
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
        st.text("Réponse brute de l'API :")
        st.text(response.text)  # Affiche la réponse brute
        return None

# Fonction principale
def main():
    Navbar()

    st.title("Vérification de Similarité de Phrases avec RUBERT")

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
                    # Préparer les données pour l'API
                    payload = {
                        "inputs": {
                            "source_sentence": main_sentence,
                            "sentences": st.session_state.secondary_sentences
                        }
                    }
                    response = query(payload)

                    if response:

                        # Supposons que la réponse est une liste de scores
                        if isinstance(response, list):
                            similarities = response
                        else:
                            similarities = response.get('similarities', [])

                        if similarities:
                            # Afficher les résultats
                            st.subheader("Résultat de la similarité :")
                            for i, similarity in enumerate(similarities):
                                percent_similarity = similarity * 100
                                st.write(
                                    f"**Phrase {i + 1}** : {st.session_state.secondary_sentences[i]} — **{percent_similarity:.2f}%**")
                                st.progress(similarity)
                        else:
                            st.error("Réponse invalide de l'API. Aucune similarité calculée.")
                except Exception as e:
                    st.error(f"Erreur lors du calcul de la similarité : {e}")
        else:
            st.warning("Veuillez entrer une phrase principale et au moins une phrase secondaire.")

if __name__ == '__main__':
    main()