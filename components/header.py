import streamlit as st

def display_header():
    st.markdown(
        '<div class="header">'
        '<h1>🦁 Akoth: Maasai Mara Wildlife Expert</h1>'
        '<p>Discover the wonders of Kenyan wildlife, conservation, and the savanna ecosystem.</p>'
        '</div>',
        unsafe_allow_html=True,
    )