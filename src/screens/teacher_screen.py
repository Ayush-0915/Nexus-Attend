import streamlit as st

from src.ui.style_base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    
    teacher_screen_login()
    
    
    
def teacher_screen_login():
        c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
        with c1:
                header_dashboard()
        with c2:
                if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="ctrl+backspace"):
                       st.session_state['login_type'] = None
                       st.rerun()

        st.markdown(
                """
                <style>
                        .teacher-login-title {
                                white-space: nowrap;
                                text-align: center;
                                font-size: 2rem !important;
                        }
                </style>
                <h1 class="teacher-login-title">Login using password</h1>
                """,
                unsafe_allow_html=True,
        )
        st.space()
        st.space()
        
        
        teacher_username = st.text_input("Enter your username", placeholder="Username")
    
        teacher_pass = st.text_input("Enter your password", type="password", placeholder="Enter Password")
        
        st.divider()
        
        btnc1, btnc2 = st.columns(2)
        
        with btnc1:
                st.button('Login', icon=':material/passkey:', shortcut='ctrl+enter', width='stretch')
        with btnc2:
                st.button('Register Instead',type='primary', icon=':material/passkey:', width='stretch')
        footer_dashboard()
        
        
        
def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
            header_dashboard()
    with c2:
            if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="ctrl+backspace"):
                    st.session_state['Login_type'] = None
                    st.rerun()
                    
    st.title("Register your teacher Profile", text_alignment="center")
    
    st.space()
    st.space()
            
            
    teacher_username = st.text_input("Enter your username", placeholder="Username")
        
    teacher_pass = st.text_input("Enter your password", type="password", placeholder="Enter Password")
            
    st.divider()
            
    btnc1, btnc2 = st.columns(2)
            
    with btnc1:
        st.button('Login', icon=':material/passkey:', shortcut='ctrl+enter', width='stretch')
    with btnc2:
        st.button('Register Instead',type='primary', icon=':material/passkey:', width='stretch')
    footer_dashboard()