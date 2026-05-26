import streamlit as st
from app.utils.obd_reader import read_obd_snapshot, is_obd_available


def validate_obd_data(data: dict):
    warnings = []

    checks = {
        "rpm": (0, 8000, "RPM"),
        "speed": (0, 300, "Viteză"),
        "coolant_temp": (-40, 130, "Temperatură lichid răcire"),
        "intake_temp": (-40, 100, "Temperatură aer admisie"),
        "throttle_pos": (0, 100, "Poziție accelerație"),
        "engine_load": (0, 100, "Sarcină motor"),
        "map": (0, 300, "MAP"),
        "maf": (0, 300, "MAF"),
        "short_fuel_trim": (-40, 40, "Short Fuel Trim"),
        "long_fuel_trim": (-40, 40, "Long Fuel Trim"),
        "o2_voltage": (0, 1.2, "Tensiune senzor O2"),
        "dtc_count": (0, 50, "Număr coduri DTC"),
    }

    for key, (min_value, max_value, label) in checks.items():
        value = data.get(key, 0)

        if value < min_value or value > max_value:
            warnings.append(
                f"{label} are valoare nerealistă: {value}. Interval acceptat: {min_value} - {max_value}."
            )

    return warnings


def obd_input_page():
    st.header("3. Date OBD-II opționale")

    st.write("Poți introduce valori OBD-II manual sau poți încerca citirea live prin adaptor ELM327.")

    use_obd = st.checkbox(
        "Vreau să folosesc date OBD-II",
        value=bool(st.session_state.obd_data)
    )

    if not use_obd:
        st.session_state.obd_data = {}
        st.info("Datele OBD-II nu vor fi folosite. Diagnoza va folosi doar simptomele.")
        return

    st.subheader("Citire live OBD-II")

    if is_obd_available():
        st.success("Biblioteca OBD este instalată.")
    else:
        st.warning("Biblioteca OBD nu este instalată. Poți introduce datele manual.")

    port = st.text_input(
        "Port OBD opțional",
        placeholder="Ex: COM3, COM4"
    )

    if st.button("Citește date live din OBD-II"):
        success, message, data = read_obd_snapshot(port if port else None)

        if success:
            warnings = validate_obd_data(data)

            if warnings:
                for warning in warnings:
                    st.warning(warning)
            else:
                st.session_state.obd_data = data
                st.success(message)
                st.rerun()
        else:
            st.error(message)

    st.divider()
    st.subheader("Introducere manuală OBD-II")

    col1, col2 = st.columns(2)

    with col1:
        rpm = st.number_input("RPM", min_value=0.0, max_value=8000.0, value=float(st.session_state.obd_data.get("rpm", 850.0)))
        speed = st.number_input("Viteză", min_value=0.0, max_value=300.0, value=float(st.session_state.obd_data.get("speed", 0.0)))
        coolant_temp = st.number_input("Temperatură lichid răcire", min_value=-40.0, max_value=130.0, value=float(st.session_state.obd_data.get("coolant_temp", 85.0)))
        intake_temp = st.number_input("Temperatură aer admisie", min_value=-40.0, max_value=100.0, value=float(st.session_state.obd_data.get("intake_temp", 25.0)))
        throttle_pos = st.number_input("Poziție accelerație", min_value=0.0, max_value=100.0, value=float(st.session_state.obd_data.get("throttle_pos", 12.0)))
        engine_load = st.number_input("Sarcină motor", min_value=0.0, max_value=100.0, value=float(st.session_state.obd_data.get("engine_load", 20.0)))

    with col2:
        map_value = st.number_input("MAP", min_value=0.0, max_value=300.0, value=float(st.session_state.obd_data.get("map", 35.0)))
        maf = st.number_input("MAF", min_value=0.0, max_value=300.0, value=float(st.session_state.obd_data.get("maf", 8.0)))
        short_fuel_trim = st.number_input("Short Fuel Trim", min_value=-40.0, max_value=40.0, value=float(st.session_state.obd_data.get("short_fuel_trim", 0.0)))
        long_fuel_trim = st.number_input("Long Fuel Trim", min_value=-40.0, max_value=40.0, value=float(st.session_state.obd_data.get("long_fuel_trim", 0.0)))
        o2_voltage = st.number_input("Tensiune senzor O2", min_value=0.0, max_value=1.2, value=float(st.session_state.obd_data.get("o2_voltage", 0.45)))
        dtc_count = st.number_input("Număr coduri eroare DTC", min_value=0, max_value=50, value=int(st.session_state.obd_data.get("dtc_count", 0)))

    obd_data = {
        "rpm": rpm,
        "speed": speed,
        "coolant_temp": coolant_temp,
        "intake_temp": intake_temp,
        "throttle_pos": throttle_pos,
        "engine_load": engine_load,
        "map": map_value,
        "maf": maf,
        "short_fuel_trim": short_fuel_trim,
        "long_fuel_trim": long_fuel_trim,
        "o2_voltage": o2_voltage,
        "dtc_count": dtc_count,
    }

    if st.button("Salvează date OBD-II"):
        warnings = validate_obd_data(obd_data)

        if warnings:
            for warning in warnings:
                st.warning(warning)
            return

        st.session_state.obd_data = obd_data
        st.success("Datele OBD-II au fost salvate.")

    if st.session_state.obd_data:
        st.subheader("Date OBD curente")
        st.json(st.session_state.obd_data)