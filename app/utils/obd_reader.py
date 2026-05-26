def is_obd_available():
    try:
        import obd
        return True
    except ImportError:
        return False


def read_obd_snapshot(port=None):
    try:
        import obd
    except ImportError:
        return False, "Biblioteca OBD nu este instalată. Rulează: pip install obd", {}

    try:
        connection = obd.OBD(port)

        if not connection.is_connected():
            return False, "Nu s-a putut conecta la adaptorul OBD-II.", {}

        commands = {
            "rpm": obd.commands.RPM,
            "speed": obd.commands.SPEED,
            "coolant_temp": obd.commands.COOLANT_TEMP,
            "intake_temp": obd.commands.INTAKE_TEMP,
            "throttle_pos": obd.commands.THROTTLE_POS,
            "engine_load": obd.commands.ENGINE_LOAD,
            "map": obd.commands.INTAKE_PRESSURE,
            "maf": obd.commands.MAF,
        }

        data = {}

        for key, command in commands.items():
            response = connection.query(command)

            if response.is_null():
                data[key] = 0
            else:
                try:
                    data[key] = float(response.value.magnitude)
                except Exception:
                    data[key] = 0

        dtc_response = connection.query(obd.commands.GET_DTC)

        if dtc_response.is_null():
            data["dtc_count"] = 0
            data["dtc_codes"] = []
        else:
            dtc_codes = dtc_response.value
            data["dtc_count"] = len(dtc_codes)
            data["dtc_codes"] = [code[0] for code in dtc_codes]

        data.setdefault("short_fuel_trim", 0)
        data.setdefault("long_fuel_trim", 0)
        data.setdefault("o2_voltage", 0)

        connection.close()

        return True, "Date OBD-II citite cu succes.", data

    except Exception as e:
        return False, f"Eroare la citirea OBD-II: {e}", {}