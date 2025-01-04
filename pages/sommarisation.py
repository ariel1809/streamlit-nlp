import json
import streamlit as st
from streamlit_lottie import st_lottie
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

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

# Charger le modèle BART pour la sommarisation
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

# Fonction pour résumer du texte avec BART
def summarize_text(text, max_length=130, min_length=30, length_penalty=2.0, num_beams=4):
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(
        inputs.input_ids,
        max_length=max_length,
        min_length=min_length,
        length_penalty=length_penalty,
        num_beams=num_beams
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

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
                    summary = summarize_text(text_input)
                    # Afficher la réponse du modèle
                    st.subheader("Résumé :")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Erreur lors de la sommarisation : {e}")
        else:
            st.warning("Veuillez entrer un texte avant de résumer.")

if __name__ == '__main__':
    main()