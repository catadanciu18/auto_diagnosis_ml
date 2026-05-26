import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

from app.auth.session import init_session, is_authenticated, logout_user
from app.utils.storage import init_db

from app.views.welcome import welcome_page
from app.views.vehicle_profile import vehicle_profile_page
from app.views.symptoms import symptoms_page
from app.views.obd_input import obd_input_page
from app.views.prediction import prediction_page
from app.views.history import history_page


st.set_page_config(
    page_title="Auto Diagnosis",
    page_icon="car",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()
init_session()


def load_css():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #07111f 0%, #101827 45%, #111827 100%);
            color: white;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        div[data-testid="stSidebarNav"] {
            display: none;
        }

        h1, h2, h3 {
            color: #f8fafc;
        }

        .main-card {
            background: rgba(15, 23, 42, 0.92);
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 22px;
            padding: 32px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.35);
        }

        .step-box {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 18px;
            padding: 18px;
            text-align: center;
        }

        .active-step {
            background: linear-gradient(135deg, #991b1b, #ef4444);
            border-radius: 18px;
            padding: 18px;
            text-align: center;
            color: white;
            font-weight: 700;
            box-shadow: 0 10px 25px rgba(239, 68, 68, 0.25);
        }

        .user-card {
            background: rgba(22, 101, 52, 0.35);
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 20px;
        }

        .stButton > button {
            border-radius: 12px;
            padding: 10px 20px;
            font-weight: 600;
            border: 1px solid rgba(148, 163, 184, 0.3);
        }

        .stTextInput > div > div > input {
            border-radius: 12px;
            background-color: #111827;
            color: white;
            border: 1px solid rgba(148, 163, 184, 0.35);
        }

        .stNumberInput input {
            border-radius: 12px;
            background-color: #111827;
            color: white;
        }

        div[data-testid="stRadio"] label {
            padding: 8px 0;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def go_to_page(page_name):
    st.session_state.current_page = page_name


def step_header():
    steps = [
        ("Date vehicul", "1"),
        ("Simptome", "2"),
        ("OBD-II opțional", "3"),
        ("Diagnoză", "4"),
        ("Istoric", "5"),
    ]

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Date vehicul"

    cols = st.columns(5)

    for col, (name, number) in zip(cols, steps):
        with col:
            active = st.session_state.current_page == name

            if active:
                st.markdown(
                    f"""
                    <div class="active-step">
                        <div style="font-size:22px;">{number}</div>
                        <div>{name}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                if st.button(
                    f"{number}. {name}",
                    key=f"top_nav_{name}",
                    use_container_width=True
                ):
                    go_to_page(name)
                    st.rerun()


def sidebar_menu():
    with st.sidebar:
        st.markdown("## AUTO DIAGNOSIS")
        st.caption("Sistem inteligent diagnoză auto")

        st.divider()

        if st.session_state.get("logged_in"):
            st.markdown(
                f"""
                <div class="user-card">
                    <b>Logat ca:</b> {st.session_state.username}<br>
                    <small>Utilizator autentificat</small>
                </div>
                """,
                unsafe_allow_html=True
            )
        elif st.session_state.get("guest"):
            st.info("Mod Guest")

        st.markdown("### Meniu rapid")

        pages = [
            "Date vehicul",
            "Simptome",
            "OBD-II opțional",
            "Diagnoză",
            "Istoric",
        ]

        if "current_page" not in st.session_state:
            st.session_state.current_page = "Date vehicul"

        selected_page = st.radio(
            "Navigare",
            pages,
            index=pages.index(st.session_state.current_page),
            label_visibility="collapsed"
        )

        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page
            st.rerun()

        st.divider()

        if st.button("Logout", use_container_width=True):
            logout_user()
            st.rerun()

        st.divider()



def main():
    load_css()

    if not is_authenticated():
        welcome_page()
        return

    sidebar_menu()
    step_header()

    page = st.session_state.current_page

    st.write("")

    if page == "Date vehicul":
        vehicle_profile_page()

    elif page == "Simptome":
        symptoms_page()

    elif page == "OBD-II opțional":
        obd_input_page()

    elif page == "Diagnoză":
        prediction_page()

    elif page == "Istoric":
        history_page()


if __name__ == "__main__":
    main()