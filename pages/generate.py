import json
import ollama
import streamlit as st
from streamlit_lottie import st_lottie
from sidebar.nav import Navbar

st.set_page_config(
    page_title="Text Generation",
    layout="wide"
)

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


# Charger l'animation Lottie
lottie_similarity = load_lottiefile("animation/generate.json")


def save_history_to_file(history, filename="history.json"):
    with open(filename, "w") as f:
        json.dump(history, f)


def load_history_from_file(filename="history.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


# Initialisation de l'état
if 'generating' not in st.session_state:
    st.session_state.generating = False
if 'stop' not in st.session_state:
    st.session_state.stop = False
if 'generated_texts' not in st.session_state:
    st.session_state.generated_texts = load_history_from_file()
if 'selected_text' not in st.session_state:
    st.session_state.selected_text = ""


def stop_generation():
    st.session_state.stop = True
    st.session_state.generating = False


def main():
    Navbar()
    st.title("Générateur de texte avec LLaMA 3.1")

    st.sidebar.header("Text Generation")

    with st.sidebar:
        st_lottie(lottie_similarity, speed=1, width=250, height=200, key="generate-lottie")

    prompt = st.text_area("Entrez votre texte ici :", height=150)

    if st.button("Générer"):
        if prompt:
            st.session_state.generating = True
            st.session_state.stop = False

    if st.session_state.generating:
        st.button("Arrêter la génération", on_click=stop_generation)
        with st.spinner("Génération en cours..."):
            try:
                response = ollama.chat(model='llama3.1', messages=[{'role': 'user', 'content': prompt}],
                                       stream=True)

                def stream_text():
                    full_text = ""
                    for chunk in response:
                        if st.session_state.stop:
                            break
                        full_text += chunk['message']['content']
                        yield chunk['message']['content']
                    # Sauvegarde du texte généré avec la question
                    st.session_state.generated_texts.append((prompt, full_text))
                    save_history_to_file(st.session_state.generated_texts)

                st.subheader("Texte généré :")
                st.write_stream(stream_text())
            except Exception as e:
                st.error(f"Erreur lors de la génération : {e}")

            st.session_state.generating = False

    if not st.session_state.generating:
        st.session_state.stop = False

    # Afficher les textes générés précédemment
    if st.session_state.generated_texts:
        st.sidebar.subheader("Historique :")
        for prompt, text in st.session_state.generated_texts:
            if st.sidebar.button(prompt[:40] + "...", key=prompt):
                st.session_state.selected_text = f"Question : {prompt}\n\nRéponse : {text}"

    if st.session_state.selected_text:
        st.subheader("Texte sélectionné :")
        st.text_area("", value=st.session_state.selected_text, height=300)


if __name__ == '__main__':
    main()