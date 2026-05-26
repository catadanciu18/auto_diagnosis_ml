import streamlit as st


def init_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "guest" not in st.session_state:
        st.session_state.guest = False

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "username" not in st.session_state:
        st.session_state.username = None

    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "welcome"

    if "vehicle_data" not in st.session_state:
        st.session_state.vehicle_data = {}

    if "selected_symptoms" not in st.session_state:
        st.session_state.selected_symptoms = []

    if "obd_data" not in st.session_state:
        st.session_state.obd_data = {}

    if "prediction_results" not in st.session_state:
        st.session_state.prediction_results = []


def login_user(user_id: int, username: str):
    st.session_state.logged_in = True
    st.session_state.guest = False
    st.session_state.user_id = user_id
    st.session_state.username = username


def continue_as_guest():
    st.session_state.logged_in = False
    st.session_state.guest = True
    st.session_state.user_id = None
    st.session_state.username = "Guest"


def logout_user():
    st.session_state.logged_in = False
    st.session_state.guest = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.auth_page = "welcome"
    st.session_state.vehicle_data = {}
    st.session_state.selected_symptoms = []
    st.session_state.obd_data = {}
    st.session_state.prediction_results = []


def is_authenticated() -> bool:
    return st.session_state.logged_in or st.session_state.guest