import streamlit as st

from app.utils.predictor import predict_faults
from app.utils.storage import save_diagnosis
from app.utils.fault_explanations import get_fault_info
from app.utils.rule_booster import apply_rule_boost

SYMPTOM_MAP = {
    "Lipsă putere": "symptom_power_loss",
    "Pornire grea": "symptom_hard_start",
    "Ralanti instabil": "symptom_rough_idle",
    "Fum negru": "symptom_black_smoke",
    "Fum albastru": "symptom_blue_smoke",
    "Fum alb": "symptom_white_smoke",
    "Consum mare": "symptom_high_consumption",
    "Check engine aprins": "symptom_check_engine",
    "Vibrații motor": "symptom_engine_vibration",
    "Rateuri": "symptom_misfire_feel",
    "Motorul se oprește la relanti": "symptom_stalls_idle",
    "Supraîncălzire": "symptom_overheating",
    "Pornire grea la cald": "symptom_hard_start_hot",
    "Pornire grea la rece": "symptom_hard_start_cold",
    "Accelerație întârziată": "symptom_slow_acceleration",
    "Miros puternic de combustibil": "symptom_fuel_smell",
    "Turație oscilantă": "symptom_rpm_fluctuation",
    "Motorul merge în 3 cilindri": "symptom_three_cylinders",
    "Pierdere antigel": "symptom_coolant_loss",
    "Presiune turbo scăzută": "symptom_low_turbo_pressure",
    "Fluierat turbo": "symptom_turbo_whistle",
    "Limp mode": "symptom_limp_mode",
    "Pedală accelerație fără răspuns": "symptom_no_throttle_response",
    "Baterie slabă": "symptom_weak_battery",
    "Electromotor învârte greu": "symptom_slow_crank",
    "Alternator nu încarcă": "symptom_alternator_not_charging",
    "Martor baterie aprins": "symptom_battery_light",
    "Ventilator radiator pornește des": "symptom_fan_runs_often",
    "Temperatura motorului scade în mers": "symptom_temp_drops_while_driving",
    "Motorul se încălzește greu": "symptom_slow_warmup",
    "Zgomot lanț distribuție": "symptom_timing_chain_noise",
    "Martor DPF aprins": "symptom_dpf_light",
    "Regenerări dese DPF": "symptom_frequent_dpf_regen",
    "Miros de sulf": "symptom_sulfur_smell",
    "Cutie schimbă greu": "symptom_hard_shifting",
    "Smucituri la schimbarea vitezelor": "symptom_gearbox_jerks",
    "Consumă ulei": "symptom_oil_consumption",

    "Zgomot metalic": "symptom_metallic_noise",
    "Tremură la frânare": "symptom_brake_vibration",
    "Mașina trage într-o parte": "symptom_pulls_side",
    "ABS aprins": "symptom_abs_light",
    "ESP aprins": "symptom_esp_light",
    "Scârțâit la frânare": "symptom_brake_squeal",
    "Pedală frână moale": "symptom_soft_brake_pedal",
    "Volanul tremură": "symptom_steering_wheel_vibration",
    "Zgomot la denivelări": "symptom_noise_over_bumps",
    "Bătaie în roată": "symptom_wheel_knock",
    "Joc în volan": "symptom_steering_play",
    "Mașina trage la frânare": "symptom_pulls_when_braking",
}


def build_payload():
    selected = st.session_state.selected_symptoms
    vehicle = st.session_state.vehicle_data
    obd = st.session_state.obd_data

    payload = {
        "brand": vehicle.get("brand", ""),
        "model": vehicle.get("model", ""),
        "engine_type": vehicle.get("engine_type", ""),
        "engine_code": vehicle.get("engine_code", ""),

        "obd_available": 1 if obd else 0,

        "rpm": obd.get("rpm", 0),
        "speed": obd.get("speed", 0),
        "coolant_temp": obd.get("coolant_temp", 0),
        "intake_temp": obd.get("intake_temp", 0),
        "throttle_pos": obd.get("throttle_pos", 0),
        "engine_load": obd.get("engine_load", 0),
        "map": obd.get("map", 0),
        "maf": obd.get("maf", 0),
        "short_fuel_trim": obd.get("short_fuel_trim", 0),
        "long_fuel_trim": obd.get("long_fuel_trim", 0),
        "o2_voltage": obd.get("o2_voltage", 0),
        "dtc_count": obd.get("dtc_count", 0),
    }

    for feature_name in SYMPTOM_MAP.values():
        payload[feature_name] = 0

    for symptom in selected:
        feature_name = SYMPTOM_MAP.get(symptom)
        if feature_name:
            payload[feature_name] = 1

    return payload


def prediction_page():
    st.header("4. Diagnoză")

    if not st.session_state.vehicle_data:
        st.warning("Completează mai întâi datele vehiculului.")
        return

    if not st.session_state.selected_symptoms:
        st.warning("Selectează cel puțin un simptom.")
        return

    if st.session_state.obd_data:
        st.success("Datele OBD-II vor fi folosite în diagnoză.")
    else:
        st.info("Nu există date OBD-II. Diagnoza va folosi doar simptomele și datele vehiculului.")

    if st.button("Rulează diagnoza"):
        payload = build_payload()

        try:
            raw_results = predict_faults(payload, top_n=10)
            results = apply_rule_boost(
                raw_results,
                st.session_state.selected_symptoms,
                top_n=2
            )
            st.session_state.prediction_results = results  
            
            if st.session_state.logged_in:
                save_diagnosis(
                    st.session_state.user_id,
                    st.session_state.vehicle_data,
                    st.session_state.selected_symptoms,
                    st.session_state.obd_data,
                    results,
                )
                st.success("Diagnoza a fost salvată în istoric.")
            else:
                st.info("Mod guest: diagnoza nu se salvează în istoric.")

        except FileNotFoundError as e:
            st.error(str(e))
            st.info("Rulează mai întâi: python -m scripts.train_model")
            return

        except ValueError as e:
            st.error("Modelul și aplicația nu au aceleași coloane.")
            st.code(str(e))
            st.info("Rulează din nou: python scripts/generate_dataset.py și apoi python -m scripts.train_model")
            return

    if st.session_state.prediction_results:
        st.subheader("Defecțiuni probabile")

        for index, item in enumerate(st.session_state.prediction_results, start=1):
            probability_percent = round(item["probability"] * 100, 2)
            fault_info = get_fault_info(item["fault"])

            with st.container(border=True):
                st.subheader(f"{index}. {fault_info['name']}")
                st.progress(min(item["probability"], 1.0))
                st.write(f"Probabilitate: {probability_percent}%")
                st.write(f"Explicație: {fault_info['description']}")
                st.write(f"Recomandare: {fault_info['recommendation']}")