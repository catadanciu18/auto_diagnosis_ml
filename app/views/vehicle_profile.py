import streamlit as st


def vehicle_profile_page():
    st.header("1. Date vehicul")

    st.write("Completează informațiile despre mașină.")

    brand = st.text_input(
        "Marcă",
        value=st.session_state.vehicle_data.get("brand", "")
    )

    model = st.text_input(
        "Model",
        value=st.session_state.vehicle_data.get("model", "")
    )

    engine_type = st.text_input(
        "Motor",
        value=st.session_state.vehicle_data.get("engine_type", "")
    )

    engine_code = st.text_input(
        "Cod motor",
        value=st.session_state.vehicle_data.get("engine_code", "")
    )

    vin = st.text_input(
        "Serie VIN opțional",
        value=st.session_state.vehicle_data.get("vin", "")
    )

    if st.button("Salvează date vehicul"):
        if not brand or not model or not engine_type or not engine_code:
            st.error("Completează marca, modelul, motorul și codul motor.")
            return

        st.session_state.vehicle_data = {
            "brand": brand,
            "model": model,
            "engine_type": engine_type,
            "engine_code": engine_code,
            "vin": vin,
        }

        st.success("Datele vehiculului au fost salvate.")