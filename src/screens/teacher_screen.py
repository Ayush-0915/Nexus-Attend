import streamlit as st

from src.ui.style_base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard


from src.database.db import check_teacher_exists as check_teacher_exists, create_teacher, teacher_login


def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    
    
    if "teacher_data" in st.session_state:
            teacher_dashboard() 
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
            teacher_screen_login()   
        
    elif st.session_state.teacher_login_type == "register":
            teacher_screen_register()
    
def teacher_dashboard():
        teacher_data = st.session_state.teacher_data
        
        st.header(f""" Welcome, {teacher_data['name']}!""")  

def login_teacher(username, password):
        if not username or not password:
                return False
        
        teacher = teacher_login(username, password)
        
        if teacher:
                st.session_state.user_role = "teacher"
                st.session_state.teacher_data = teacher
                st.session_state.is_logged_in = True
                
                return True
        
        
        return False
        
                
   
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
                if st.button('Login', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
                        if login_teacher(teacher_username, teacher_pass):
                                st.toast("welcome back!", icon="👋")
                                import time
                                time.sleep(1)
                                st.rerun()
                        else:
                                st.error("Invalid username and password combo")  
        with btnc2:
                if st.button('Register Instead',type='primary', icon=':material/passkey:', width='stretch'):
                        st.session_state.teacher_login_type = "register"
        footer_dashboard()
        
        
def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confrim):
        if not teacher_username or not teacher_name or not teacher_pass or not teacher_pass_confrim:
                return False, "All fields are required!"
        
        if check_teacher_exists(teacher_username):
                return False, "Username already exists!"
        
        if teacher_pass != teacher_pass_confrim:
                return False, "Passwords do not match!"
        
        try:
                create_teacher(teacher_username, teacher_pass, teacher_name)
                return True, "Successfully Created! Login Now!"
        except Exception as e:
                return False, "Unexpected Error Occured! Please try again later." 
             
def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
            header_dashboard()
    with c2:
            if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="ctrl+backspace"):
                    st.session_state['Login_type'] = None
                    st.rerun()
                    
    st.markdown(
        """
        <style>
                .teacher-register-title {
                        white-space: nowrap;
                        text-align: center;
                        font-size: 2.5rem !important;
                }
        </style>
        <h1 class="teacher-register-title">Register your teacher Profile</h1>
        """,
        unsafe_allow_html=True,
    )
    
    st.space()
    st.space()
            
            
    teacher_username = st.text_input("Enter your username", placeholder="Username")

    teacher_name = st.text_input("Enter your name", placeholder="Name")

    teacher_pass = st.text_input("Enter your password", type="password", placeholder="Enter Password")

    teacher_pass_confrim = st.text_input("Confirm your password", type="password", placeholder="Confirm Password")
    
    st.divider()
            
    btnc1, btnc2 = st.columns(2)
            
    with btnc1:
        if st.button('Register Now', icon=':material/passkey:', shortcut='ctrl+enter', width='stretch'):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confrim)
            if success:
                    st.success(message)
                    import time
                    time.sleep(2)
                    st.session_state.teacher_login_type = "login"
                    st.rerun()
            else:
                st.error(message)
    with btnc2:
        if st.button('Login Instead',type='primary', icon=':material/passkey:', width='stretch'):
                st.session_state.teacher_login_type = 'login'
    footer_dashboard()