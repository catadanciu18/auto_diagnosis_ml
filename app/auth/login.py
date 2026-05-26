import streamlit as st
from app.utils.storage import get_user_by_username_or_email
from app.auth.password_utils import check_password
from app.auth.session import login_user


def login_page():
    st.subheader("Login")

    identifier = st.text_input("Username sau email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not identifier or not password:
            st.error("Completează username/email și parola.")
            return

        user = get_user_by_username_or_email(identifier)

        if user is None:
            st.error("User inexistent.")
            return

        user_id, username, email, password_hash = user

        if check_password(password, password_hash):
            login_user(user_id, username)
            st.success(f"Te-ai logat ca {username}.")
            st.rerun()
        else:
            st.error("Parolă greșită.")