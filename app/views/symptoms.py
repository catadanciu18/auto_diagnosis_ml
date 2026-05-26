import streamlit as st
from app.utils.symptom_catalog import SYMPTOM_OPTIONS


def symptoms_page():
    st.header("2. Simptome")
    st.write("Selectează simptomele observate la mașină.")

    if "selected_symptoms" not in st.session_state:
        st.session_state.selected_symptoms = []

    unique_symptoms = list(dict.fromkeys(SYMPTOM_OPTIONS))

    search_term = st.text_input(
        "Caută simptom",
        placeholder="Ex: zgomot, frânare, fum, pornire..."
    )

    filtered_symptoms = [
        symptom for symptom in unique_symptoms
        if search_term.lower() in symptom.lower()
    ]



    if not filtered_symptoms:
        st.warning("Nu s-a găsit niciun simptom.")
        return

    cols = st.columns(3)

    for index, symptom in enumerate(filtered_symptoms):
        col = cols[index % 3]

        with col:
            checked = symptom in st.session_state.selected_symptoms

            new_value = st.checkbox(
                symptom,
                value=checked,
                key=f"symptom_checkbox_{index}_{symptom}"
            )

            if new_value and symptom not in st.session_state.selected_symptoms:
                st.session_state.selected_symptoms.append(symptom)

            elif not new_value and symptom in st.session_state.selected_symptoms:
                st.session_state.selected_symptoms.remove(symptom)

    st.divider()

    st.subheader("Simptome selectate")

    if st.session_state.selected_symptoms:
        for symptom in st.session_state.selected_symptoms:
            st.write(f"- {symptom}")

        if st.button("Șterge toate simptomele"):
            st.session_state.selected_symptoms = []
            st.rerun()
    else:
        st.info("Nu ai selectat niciun simptom.")