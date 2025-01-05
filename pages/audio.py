import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie
from sidebar.nav import Navbar
import time
import os

st.set_page_config(
    page_title="Audio Generation",
    layout="wide"
)

# Fichier JSON pour l'historique des audios
HISTORY_FILE = "audio_history.json"


# Fonction pour charger une animation Lottie locale
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


lottie_audio = load_lottiefile("animation/audio.json")


# Fonction pour charger l'historique depuis le fichier JSON
def load_audio_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


# Fonction pour sauvegarder l'historique dans un fichier JSON
def save_audio_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


# Charger l'historique au démarrage
if 'generated_audios' not in st.session_state:
    st.session_state.generated_audios = load_audio_history()
if 'selected_audio' not in st.session_state:
    st.session_state.selected_audio = ""

HUGGINGFACE_API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}


# Fonction pour envoyer une requête à l'API Hugging Face
def query(payload):
    for _ in range(5):  # Réessayer jusqu'à 5 fois
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            return response.content
        elif response.status_code == 503:
            st.warning("Le modèle est en cours de chargement. Nouvelle tentative dans 10 secondes...")
            time.sleep(10)
        else:
            st.error(f"Erreur API: {response.json().get('error', 'Unknown error')}")
            return None
    st.error("Le modèle n'a pas pu être chargé après plusieurs tentatives.")
    return None


# Fonction pour sauvegarder l'audio dans un fichier
def save_audio_to_file(audio_data, audio_path):
    with open(audio_path, "wb") as f:
        f.write(audio_data)


# Fonction principale
def main():
    Navbar()
    st.title("Générateur de parole avec BAYASHI")

    st.sidebar.header("Audio Generation")
    with st.sidebar:
        st_lottie(lottie_audio, speed=1, width=250, height=200, key="audio-lottie")

    text_input = st.text_area("Texte à convertir en parole", height=150)

    if st.button("Générer la parole"):
        if text_input.strip() != "":
            with st.spinner("Génération de la parole en cours..."):
                audio_bytes = query({"inputs": text_input})
                if audio_bytes:
                    # Générer le chemin du fichier
                    audio_path = f"outputs/audio_{len(st.session_state.generated_audios) + 1}.wav"
                    save_audio_to_file(audio_bytes, audio_path)

                    # Ajouter à l'historique de session et sauvegarder
                    new_entry = {"text": text_input, "path": audio_path}
                    st.session_state.generated_audios.append(new_entry)
                    save_audio_history(st.session_state.generated_audios)

                    st.audio(audio_path, format="audio/wav")
                    st.success("Parole générée avec succès!")
        else:
            st.warning("Veuillez entrer un texte.")

    # Afficher les audios générés précédemment
    if st.session_state.generated_audios:
        st.sidebar.subheader("Historique :")
        for audio in st.session_state.generated_audios:
            if st.sidebar.button(audio['text'][:40] + "...", key=audio['text']):
                st.session_state.selected_audio = audio

    # Afficher l'audio sélectionné
    if st.session_state.selected_audio:
        st.subheader("Texte sélectionné :")
        st.write(st.session_state.selected_audio['text'])
        st.audio(st.session_state.selected_audio['path'], format="audio/wav")


if __name__ == '__main__':
    main()