import json
import streamlit as st

from app.utils.storage import get_history_for_user, delete_diagnosis
from app.utils.fault_explanations import get_fault_info


def history_page():
    st.header("Istoric diagnoze")

    if not st.session_state.logged_in:
        st.warning("Istoricul este disponibil doar pentru utilizatorii logați.")
        return

    history = get_history_for_user(st.session_state.user_id)

    if not history:
        st.info("Nu există diagnoze salvate.")
        return

    for entry in history:
        (
            diagnosis_id,
            brand,
            model,
            engine_type,
            engine_code,
            vin,
            symptoms,
            obd_data,
            prediction_results,
            created_at,
        ) = entry

        symptoms_list = json.loads(symptoms)
        predictions = json.loads(prediction_results)

        with st.container(border=True):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.subheader(f"{brand} {model}")
                st.write(f"Data: {created_at}")
                st.write(f"Motor: {engine_type}")
                st.write(f"Cod motor: {engine_code}")

                if vin:
                    st.write(f"VIN: {vin}")

            with col2:
                if st.button("Șterge", key=f"delete_{diagnosis_id}", use_container_width=True):
                    delete_diagnosis(diagnosis_id, st.session_state.user_id)
                    st.success("Diagnoza a fost ștearsă.")
                    st.rerun()

            st.write("Simptome:")
            for symptom in symptoms_list:
                st.write(f"- {symptom}")

            st.write("Rezultate:")

            for result in predictions[:2]:
                fault_info = get_fault_info(result["fault"])
                probability = round(result["probability"] * 100, 2)

                st.write(f"- {fault_info['name']} - {probability}%")