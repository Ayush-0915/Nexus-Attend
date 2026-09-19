import streamlit as st

from src.ui.style_base_layout import style_background_dashboard

def student_screen():
    style_background_dashboard()
    st.title("Student Screen")