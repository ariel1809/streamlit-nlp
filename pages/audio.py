import streamlit as st
import torch
from transformers import BarkModel, AutoProcessor
import scipy.io.wavfile as wav
import json
from streamlit_lottie import st_lottie
import os
from sidebar.nav import Navbar

st.set_page_config(
    page_title="Audio Generation",
    layout="wide"
)


# Fonction pour charger une animation Lottie locale
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


# Charger l'animation Lottie
lottie_audio = load_lottiefile("animation/audio.json")

# Initialisation de l'état
if 'generating' not in st.session_state:
    st.session_state.generating = False
if 'stop' not in st.session_state:
    st.session_state.stop = False
if 'generated_audios' not in st.session_state:
    st.session_state.generated_audios = []
if 'selected_audio' not in st.session_state:
    st.session_state.selected_audio = ""

# Créer le dossier outputs s'il n'existe pas
os.makedirs("outputs", exist_ok=True)

# Charger le modèle Bark
model = BarkModel.from_pretrained("suno/bark-small")

# Détecter si CUDA est disponible et charger le modèle sur le bon appareil
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# Charger le processeur pour le modèle Bark
processor = AutoProcessor.from_pretrained("suno/bark")


# Fonction pour sauvegarder l'audio dans un fichier
def save_audio_to_file(prompt, audio_path):
    with open("generated_audios.txt", "a") as f:
        f.write(f"Texte : {prompt}\nAudio : {audio_path}\n\n")


def main():
    Navbar()
    st.title("Générateur de parole avec Bark")

    st.sidebar.header("Audio Generation")

    with st.sidebar:
        st_lottie(lottie_audio, speed=1, width=250, height=200, key="audio-lottie")

    text_input = st.text_area("Texte à convertir en parole", height=150)

    if st.button("Générer la parole"):
        if text_input.strip() != "":
            st.session_state.generating = True
            st.session_state.stop = False

    if st.session_state.generating:
        st.button("Arrêter la génération", on_click=lambda: setattr(st.session_state, 'stop', True))
        with st.spinner("Génération de la parole en cours..."):
            try:
                inputs = processor(text_input)
                speech_output = model.generate(**inputs.to(device))
                sampling_rate = model.generation_config.sample_rate

                audio_path = f"outputs/audio_{len(st.session_state.generated_audios) + 1}.wav"
                wav.write(audio_path, rate=sampling_rate, data=speech_output[0].cpu().numpy())

                st.session_state.generated_audios.append((text_input, audio_path))
                save_audio_to_file(text_input, audio_path)

                st.audio(audio_path, format="audio/wav")
                st.success("Parole générée avec succès!")
            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")

            st.session_state.generating = False

    # Afficher les audios générés précédemment
    if st.session_state.generated_audios:
        st.sidebar.subheader("Historique :")
        for prompt, audio_path in st.session_state.generated_audios:
            if st.sidebar.button(prompt[:40] + "...", key=prompt):
                st.session_state.selected_audio = (prompt, audio_path)

    # Affiche l'audio sélectionné dans la zone principale
    if st.session_state.selected_audio:
        prompt, audio_path = st.session_state.selected_audio
        st.subheader("Texte sélectionné :")
        st.write(prompt)
        st.audio(audio_path, format="audio/wav")


if __name__ == '__main__':
    main()