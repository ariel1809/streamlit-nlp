import streamlit as st


def Navbar():
    with st.sidebar:
            st.image("images/app_nlp.png", use_container_width=True)
            st.page_link('app.py', label='Home', icon='🏠')
            st.page_link('pages/generate.py', label='Générateur de texte', icon='📝')
            st.page_link('pages/sentence.py', label='Sentence Similarity', icon='📊')
            st.page_link('pages/sommarisation.py', label='Sommarisation', icon='🔍')
            st.page_link('pages/audio.py', label='Text To Speech', icon='🔊')