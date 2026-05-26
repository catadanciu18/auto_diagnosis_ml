import streamlit as st

from app.auth.session import continue_as_guest
from app.auth.register import register_page
from app.auth.login import login_page


def welcome_page():
    st.title("Sistem inteligent pentru diagnoza auto")
    st.write("Alege modul de utilizare al aplicației.")

    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "welcome"

    if st.session_state.auth_page == "welcome":
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Register", use_container_width=True):
                st.session_state.auth_page = "register"
                st.rerun()

        with col2:
            if st.button("Login", use_container_width=True):
                st.session_state.auth_page = "login"
                st.rerun()

        with col3:
            if st.button("Continue as Guest", use_container_width=True):
                continue_as_guest()
                st.rerun()

        st.info("Guest mode nu salvează diagnozele în history.")

    elif st.session_state.auth_page == "register":
        register_page()

        if st.button("Înapoi"):
            st.session_state.auth_page = "welcome"
            st.rerun()

    elif st.session_state.auth_page == "login":
        login_page()

        if st.button("Înapoi"):
            st.session_state.auth_page = "welcome"
            st.rerun()