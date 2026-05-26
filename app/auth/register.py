import streamlit as st
from app.utils.storage import create_user
from app.auth.password_utils import hash_password


def register_page():
    st.subheader("Register")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Create account"):
        if not username or not email or not password:
            st.error("Completează toate câmpurile.")
            return

        if password != confirm_password:
            st.error("Parolele nu coincid.")
            return

        if len(password) < 6:
            st.error("Parola trebuie să aibă minim 6 caractere.")
            return

        hashed = hash_password(password)

        success, message = create_user(username, email, hashed)

        if success:
            st.success(message)
            st.info("Te poți loga acum.")
        else:
            st.error(message)