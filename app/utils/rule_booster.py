RULES = [
    {
        "fault": "brake_issue",
        "symptoms": ["Scârțâit la frânare", "Tremură la frânare"],
        "boost": 0.35,
    },
    {
        "fault": "brake_issue",
        "symptoms": ["Pedală frână moale", "Mașina trage la frânare"],
        "boost": 0.40,
    },
    {
        "fault": "suspension_issue",
        "symptoms": ["Zgomot la denivelări", "Bătaie în roată"],
        "boost": 0.35,
    },
    {
        "fault": "suspension_issue",
        "symptoms": ["Zgomot metalic", "Mașina trage într-o parte"],
        "boost": 0.25,
    },
    {
        "fault": "steering_issue",
        "symptoms": ["Joc în volan", "Mașina trage într-o parte"],
        "boost": 0.35,
    },
    {
        "fault": "wheel_alignment_issue",
        "symptoms": ["Mașina trage într-o parte", "Volanul tremură"],
        "boost": 0.35,
    },
    {
        "fault": "wheel_bearing_issue",
        "symptoms": ["Zgomot metalic", "Bătaie în roată"],
        "boost": 0.35,
    },
    {
        "fault": "oil_consumption",
        "symptoms": ["Fum albastru", "Consumă ulei"],
        "boost": 0.45,
    },
    {
        "fault": "turbo_issue",
        "symptoms": ["Lipsă putere", "Fluierat turbo"],
        "boost": 0.35,
    },
    {
        "fault": "turbo_issue",
        "symptoms": ["Presiune turbo scăzută", "Limp mode"],
        "boost": 0.40,
    },
    {
        "fault": "dpf_issue",
        "symptoms": ["Martor DPF aprins", "Regenerări dese DPF"],
        "boost": 0.45,
    },
    {
        "fault": "battery_issue",
        "symptoms": ["Baterie slabă", "Electromotor învârte greu"],
        "boost": 0.35,
    },
    {
        "fault": "alternator_issue",
        "symptoms": ["Alternator nu încarcă", "Martor baterie aprins"],
        "boost": 0.45,
    },
    {
        "fault": "starter_issue",
        "symptoms": ["Electromotor învârte greu", "Pornire grea"],
        "boost": 0.35,
    },
    {
        "fault": "misfire",
        "symptoms": ["Rateuri", "Motorul merge în 3 cilindri"],
        "boost": 0.45,
    },
    {
        "fault": "coolant_leak",
        "symptoms": ["Pierdere antigel", "Supraîncălzire"],
        "boost": 0.40,
    },
    {
        "fault": "thermostat_issue",
        "symptoms": ["Temperatura motorului scade în mers", "Motorul se încălzește greu"],
        "boost": 0.45,
    },
]


def apply_rule_boost(results: list, selected_symptoms: list, top_n: int = 2):
    scores = {item["fault"]: float(item["probability"]) for item in results}

    selected_set = set(selected_symptoms)

    for rule in RULES:
        required = set(rule["symptoms"])

        if required.issubset(selected_set):
            fault = rule["fault"]
            scores[fault] = scores.get(fault, 0.0) + rule["boost"]

    total = sum(scores.values())

    if total > 0:
        boosted_results = [
            {
                "fault": fault,
                "probability": score / total
            }
            for fault, score in scores.items()
        ]
    else:
        boosted_results = results

    boosted_results.sort(key=lambda x: x["probability"], reverse=True)

    return boosted_results[:top_n]