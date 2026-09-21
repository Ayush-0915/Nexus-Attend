from pathlib import Path

import streamlit as st


def header_home():
    logo_url = "https://i.ibb.co/5hNpHbYY/Chat-GPT-Image-Sep-20-2026-03-25-50-PM.png"
    st.markdown(
        f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px">
            <img src='{logo_url}' style='height:100px;' />
            <h1 style='text-align:center; color:#E0E3FF'>Nexus<br/>Attend</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
def header_dashboard():

    logo_url = "https://i.ibb.co/5hNpHbYY/Chat-GPT-Image-Sep-20-2026-03-25-50-PM.png"
    
    st.markdown(f"""
        <div style="display:flex; width:100%; align-items:center; justify-content:center; gap:10px;">
            <img src='{logo_url}' style='display:block; height:85px; width:auto;' />
            <h2 style='margin:0; text-align:left; line-height:0.95; color:#5865F2;'>Nexus<br/>Attend</h2>
        </div>   
                
                """, unsafe_allow_html=True)