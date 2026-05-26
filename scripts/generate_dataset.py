import os
import random
import pandas as pd

OUTPUT_PATH = "data/processed/training_dataset.csv"

FAULT_CLASSES = {
    "normal": {
        "symptoms": [],
        "obd": {}
    },
    "maf_issue": {
        "symptoms": ["power_loss", "high_consumption", "slow_acceleration", "check_engine"],
        "obd": {"maf": (1, 5), "short_fuel_trim": (8, 22), "long_fuel_trim": (8, 20)}
    },
    "o2_sensor_issue": {
        "symptoms": ["high_consumption", "check_engine"],
        "obd": {"o2_voltage": (0.0, 0.1), "short_fuel_trim": (10, 25), "long_fuel_trim": (10, 25)}
    },
    "misfire": {
        "symptoms": ["rough_idle", "engine_vibration", "misfire_feel", "three_cylinders", "check_engine"],
        "obd": {"rpm": (500, 1200)}
    },
    "cooling_issue": {
        "symptoms": ["overheating", "fan_runs_often", "check_engine"],
        "obd": {"coolant_temp": (105, 125)}
    },
    "fuel_system_issue": {
        "symptoms": ["hard_start", "power_loss", "fuel_smell", "check_engine"],
        "obd": {"short_fuel_trim": (15, 30), "long_fuel_trim": (15, 30)}
    },
    "egr_issue": {
        "symptoms": ["rough_idle", "black_smoke", "power_loss", "slow_acceleration"],
        "obd": {"engine_load": (50, 90)}
    },
    "ignition_issue": {
        "symptoms": ["hard_start", "misfire_feel", "engine_vibration", "stalls_idle"],
        "obd": {}
    },
    "injector_issue": {
        "symptoms": ["rough_idle", "high_consumption", "fuel_smell", "black_smoke"],
        "obd": {"short_fuel_trim": (10, 28), "long_fuel_trim": (10, 25)}
    },
    "turbo_issue": {
        "symptoms": ["power_loss", "black_smoke", "slow_acceleration", "low_turbo_pressure", "turbo_whistle", "limp_mode"],
        "obd": {"map": (5, 20), "engine_load": (70, 100)}
    },
    "dpf_issue": {
        "symptoms": ["dpf_light", "frequent_dpf_regen", "limp_mode", "power_loss"],
        "obd": {"engine_load": (65, 100)}
    },
    "battery_issue": {
        "symptoms": ["weak_battery", "slow_crank", "battery_light"],
        "obd": {}
    },
    "alternator_issue": {
        "symptoms": ["alternator_not_charging", "battery_light", "weak_battery"],
        "obd": {}
    },
    "starter_issue": {
        "symptoms": ["slow_crank", "hard_start"],
        "obd": {}
    },
    "thermostat_issue": {
        "symptoms": ["temp_drops_while_driving", "slow_warmup"],
        "obd": {"coolant_temp": (50, 75)}
    },
    "coolant_leak": {
        "symptoms": ["coolant_loss", "overheating", "fan_runs_often", "white_smoke"],
        "obd": {"coolant_temp": (100, 120)}
    },
    "oil_consumption": {
        "symptoms": ["blue_smoke", "oil_consumption"],
        "obd": {}
    },
    "vacuum_leak": {
        "symptoms": ["rough_idle", "rpm_fluctuation", "power_loss"],
        "obd": {"short_fuel_trim": (12, 28), "long_fuel_trim": (10, 25)}
    },
    "throttle_body_issue": {
        "symptoms": ["no_throttle_response", "rough_idle", "rpm_fluctuation"],
        "obd": {"throttle_pos": (0, 5)}
    },
    "catalyst_issue": {
        "symptoms": ["sulfur_smell", "power_loss", "check_engine"],
        "obd": {"o2_voltage": (0.85, 1.0)}
    },
    "abs_sensor_issue": {
        "symptoms": ["abs_light", "esp_light"],
        "obd": {}
    },
    "transmission_issue": {
        "symptoms": ["hard_shifting", "gearbox_jerks"],
        "obd": {}
    },
    "timing_chain_issue": {
        "symptoms": ["timing_chain_noise", "hard_start", "rough_idle", "metallic_noise"],
        "obd": {}
    },
    "brake_issue": {
        "symptoms": ["brake_vibration", "brake_squeal", "soft_brake_pedal", "pulls_when_braking", "metallic_noise"],
        "obd": {}
    },
    "wheel_alignment_issue": {
        "symptoms": ["pulls_side", "steering_wheel_vibration"],
        "obd": {}
    },
    "suspension_issue": {
        "symptoms": ["noise_over_bumps", "metallic_noise", "wheel_knock", "pulls_side"],
        "obd": {}
    },
    "steering_issue": {
        "symptoms": ["steering_play", "pulls_side", "steering_wheel_vibration"],
        "obd": {}
    },
    "wheel_bearing_issue": {
        "symptoms": ["wheel_knock", "metallic_noise", "steering_wheel_vibration"],
        "obd": {}
    },
}

SYMPTOM_COLUMNS = [
    "symptom_power_loss",
    "symptom_hard_start",
    "symptom_rough_idle",
    "symptom_black_smoke",
    "symptom_blue_smoke",
    "symptom_white_smoke",
    "symptom_high_consumption",
    "symptom_check_engine",
    "symptom_engine_vibration",
    "symptom_misfire_feel",
    "symptom_stalls_idle",
    "symptom_overheating",
    "symptom_hard_start_hot",
    "symptom_hard_start_cold",
    "symptom_slow_acceleration",
    "symptom_fuel_smell",
    "symptom_rpm_fluctuation",
    "symptom_three_cylinders",
    "symptom_coolant_loss",
    "symptom_low_turbo_pressure",
    "symptom_turbo_whistle",
    "symptom_limp_mode",
    "symptom_no_throttle_response",
    "symptom_weak_battery",
    "symptom_slow_crank",
    "symptom_alternator_not_charging",
    "symptom_battery_light",
    "symptom_fan_runs_often",
    "symptom_temp_drops_while_driving",
    "symptom_slow_warmup",
    "symptom_timing_chain_noise",
    "symptom_dpf_light",
    "symptom_frequent_dpf_regen",
    "symptom_sulfur_smell",
    "symptom_hard_shifting",
    "symptom_gearbox_jerks",
    "symptom_oil_consumption",

    "symptom_metallic_noise",
    "symptom_brake_vibration",
    "symptom_pulls_side",
    "symptom_abs_light",
    "symptom_esp_light",
    "symptom_brake_squeal",
    "symptom_soft_brake_pedal",
    "symptom_steering_wheel_vibration",
    "symptom_noise_over_bumps",
    "symptom_wheel_knock",
    "symptom_steering_play",
    "symptom_pulls_when_braking",
]

BRANDS = ["VW", "Audi", "BMW", "Mercedes", "Ford", "Opel", "Toyota", "Skoda", "Renault", "Peugeot"]
MODELS = ["Golf", "A4", "Seria 3", "C Class", "Focus", "Astra", "Avensis", "Octavia", "Megane", "Passat"]
ENGINES = ["1.6 benzina", "1.9 TDI", "2.0 TDI", "2.0 benzina", "1.8 benzina", "2.2 diesel", "1.5 dCi", "1.6 HDI"]
ENGINE_CODES = ["BKC", "BKD", "AXR", "N47", "OM646", "Z19DTH", "1ZZ", "BLS", "K9K", "DV6"]


def random_base_row(fault_label, obd_available=1):
    row = {
        "brand": random.choice(BRANDS),
        "model": random.choice(MODELS),
        "engine_type": random.choice(ENGINES),
        "engine_code": random.choice(ENGINE_CODES),

        "obd_available": obd_available,

        "rpm": random.randint(750, 950) if obd_available else 0,
        "speed": random.randint(0, 120) if obd_available else 0,
        "coolant_temp": random.randint(80, 95) if obd_available else 0,
        "intake_temp": random.randint(20, 45) if obd_available else 0,
        "throttle_pos": round(random.uniform(5, 35), 2) if obd_available else 0,
        "engine_load": round(random.uniform(15, 60), 2) if obd_available else 0,
        "map": round(random.uniform(25, 70), 2) if obd_available else 0,
        "maf": round(random.uniform(5, 35), 2) if obd_available else 0,
        "short_fuel_trim": round(random.uniform(-5, 5), 2) if obd_available else 0,
        "long_fuel_trim": round(random.uniform(-5, 5), 2) if obd_available else 0,
        "o2_voltage": round(random.uniform(0.2, 0.8), 2) if obd_available else 0,
        "dtc_count": random.randint(0, 1) if obd_available else 0,

        "fault_label": fault_label,
    }

    for symptom_col in SYMPTOM_COLUMNS:
        row[symptom_col] = 0

    return row


def add_fault_pattern(row, fault_label):
    pattern = FAULT_CLASSES[fault_label]

    for symptom in pattern["symptoms"]:
        col_name = f"symptom_{symptom}"
        if col_name in row:
            row[col_name] = 1

    if row["obd_available"] == 1:
        for obd_name, value_range in pattern["obd"].items():
            min_value, max_value = value_range

            if obd_name in ["rpm", "coolant_temp", "dtc_count"]:
                row[obd_name] = random.randint(min_value, max_value)
            else:
                row[obd_name] = round(random.uniform(min_value, max_value), 2)

        if fault_label not in ["normal", "battery_issue", "starter_issue", "brake_issue", "suspension_issue", "steering_issue", "wheel_alignment_issue", "wheel_bearing_issue"]:
            row["dtc_count"] = random.randint(1, 4)

    return row


def add_noise(row):
    for symptom_col in SYMPTOM_COLUMNS:
        if row[symptom_col] == 0 and random.random() < 0.015:
            row[symptom_col] = 1

    return row


def generate_dataset(rows_per_class=450):
    all_rows = []

    for fault_label in FAULT_CLASSES.keys():
        for _ in range(rows_per_class):
            obd_available = random.choices([0, 1], weights=[45, 55])[0]

            row = random_base_row(fault_label, obd_available=obd_available)
            row = add_fault_pattern(row, fault_label)
            row = add_noise(row)

            all_rows.append(row)

    random.shuffle(all_rows)

    df = pd.DataFrame(all_rows)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("Dataset generat cu succes.")
    print("Fisier:", OUTPUT_PATH)
    print("Randuri:", len(df))
    print()
    print(df["fault_label"].value_counts())
    print()
    print("OBD availability:")
    print(df["obd_available"].value_counts())


if __name__ == "__main__":
    generate_dataset()