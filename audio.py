import streamlit as st
import torch
from transformers import BarkModel, AutoProcessor
import scipy.io.wavfile as wav

# Charger le modèle Bark
model = BarkModel.from_pretrained("suno/bark-small")

# Détecter si CUDA est disponible et charger le modèle sur le bon appareil
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# Charger le processeur pour le modèle Bark
processor = AutoProcessor.from_pretrained("suno/bark")

# Interface utilisateur Streamlit
st.title("Générateur de parole avec Bark")
st.write("Entrez votre texte ci-dessous et générez de la parole.")

# Zone de texte pour l'entrée utilisateur
text_input = st.text_area("Texte à convertir en parole", "")

# Bouton pour générer la parole
if st.button("Générer la parole"):
    if text_input.strip() != "":
        # Afficher un spinner pendant la génération
        with st.spinner("Génération de la parole..."):
            # Préparer les entrées
            inputs = processor(text_input)

            # Générer la parole
            speech_output = model.generate(**inputs.to(device))

            # Récupérer la fréquence d'échantillonnage
            sampling_rate = model.generation_config.sample_rate

            # Sauvegarder l'audio dans un fichier
            wav.write("bark_output.wav", rate=sampling_rate, data=speech_output[0].cpu().numpy())

            # Afficher le fichier audio dans l'application
            st.audio("bark_output.wav", format="audio/wav")

            st.success("Parole générée avec succès!")
    else:
        st.warning("Veuillez entrer un texte à convertir.")