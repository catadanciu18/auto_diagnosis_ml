FAULT_EXPLANATIONS = {
    "normal": {
        "name": "Funcționare normală",
        "description": "Valorile și simptomele nu indică o defecțiune evidentă.",
        "recommendation": "Monitorizează în continuare comportamentul mașinii."
    },
    "maf_issue": {
        "name": "Problemă senzor MAF",
        "description": "MAF-ul poate transmite valori incorecte despre aerul admis.",
        "recommendation": "Verifică senzorul MAF, mufa, cablajul și filtrul de aer."
    },
    "o2_sensor_issue": {
        "name": "Problemă senzor oxigen",
        "description": "Senzorul O2 poate afecta amestecul aer-combustibil.",
        "recommendation": "Verifică senzorii lambda și valorile fuel trim."
    },
    "misfire": {
        "name": "Rateuri / misfire",
        "description": "Motorul poate rata aprinderea pe unul sau mai mulți cilindri.",
        "recommendation": "Verifică bujii, bobine, injectoare și compresie."
    },
    "cooling_issue": {
        "name": "Problemă sistem răcire",
        "description": "Temperatura motorului este prea mare sau există risc de supraîncălzire.",
        "recommendation": "Verifică antigelul, termostatul, radiatorul și ventilatoarele."
    },
    "fuel_system_issue": {
        "name": "Problemă alimentare combustibil",
        "description": "Motorul poate primi prea mult sau prea puțin combustibil.",
        "recommendation": "Verifică pompa de combustibil, filtrul, presiunea și injectoarele."
    },
    "egr_issue": {
        "name": "Problemă EGR",
        "description": "Supapa EGR poate fi blocată sau murdară.",
        "recommendation": "Verifică și curăță EGR-ul și admisia."
    },
    "ignition_issue": {
        "name": "Problemă aprindere",
        "description": "Sistemul de aprindere poate cauza pornire grea, vibrații sau opriri.",
        "recommendation": "Verifică bujiile, bobinele și cablajul."
    },
    "injector_issue": {
        "name": "Problemă injectoare",
        "description": "Un injector poate pulveriza incorect sau poate rămâne blocat.",
        "recommendation": "Verifică injectoarele, returul și corecțiile."
    },
    "turbo_issue": {
        "name": "Problemă turbo",
        "description": "Presiunea de supraalimentare poate fi prea mică sau sistemul turbo poate avea pierderi.",
        "recommendation": "Verifică furtunurile de vacuum/boost, actuatorul, intercoolerul și turbina."
    },
    "dpf_issue": {
        "name": "Problemă DPF",
        "description": "Filtrul de particule poate fi încărcat sau regenerările pot fi incomplete.",
        "recommendation": "Verifică încărcarea DPF, senzorul de presiune diferențială și condițiile de regenerare."
    },
    "battery_issue": {
        "name": "Problemă baterie",
        "description": "Bateria poate fi slabă, descărcată sau uzată.",
        "recommendation": "Verifică tensiunea bateriei la repaus și în timpul pornirii."
    },
    "alternator_issue": {
        "name": "Problemă alternator",
        "description": "Alternatorul poate să nu încarce corect bateria.",
        "recommendation": "Verifică tensiunea de încărcare, cureaua de accesorii și conexiunile electrice."
    },
    "starter_issue": {
        "name": "Problemă electromotor",
        "description": "Electromotorul poate învârti greu sau poate avea contact imperfect.",
        "recommendation": "Verifică electromotorul, masa motorului și bornele bateriei."
    },
    "thermostat_issue": {
        "name": "Problemă termostat",
        "description": "Termostatul poate rămâne blocat deschis sau închis.",
        "recommendation": "Verifică temperatura motorului în mers și funcționarea termostatului."
    },
    "coolant_leak": {
        "name": "Pierdere lichid de răcire",
        "description": "Sistemul de răcire poate pierde antigel.",
        "recommendation": "Verifică furtunurile, radiatorul, vasul de expansiune și pompa de apă."
    },
    "oil_consumption": {
        "name": "Consum de ulei",
        "description": "Motorul poate consuma ulei prin segmenți, simeringuri de supape sau turbină.",
        "recommendation": "Verifică nivelul uleiului, compresia și fumul albastru la accelerație."
    },
    "vacuum_leak": {
        "name": "Pierdere vacuum / aer fals",
        "description": "Motorul poate trage aer fals, afectând amestecul aer-combustibil.",
        "recommendation": "Verifică furtunurile de vacuum, admisia și garniturile."
    },
    "throttle_body_issue": {
        "name": "Problemă clapetă accelerație",
        "description": "Clapeta de accelerație poate fi murdară sau poate avea poziție incorectă.",
        "recommendation": "Curăță clapeta și verifică adaptarea acesteia cu testerul."
    },
    "catalyst_issue": {
        "name": "Problemă catalizator",
        "description": "Catalizatorul poate fi înfundat sau ineficient.",
        "recommendation": "Verifică valorile lambda, contrapresiunea evacuării și codurile DTC."
    },
    "abs_sensor_issue": {
        "name": "Problemă senzor ABS",
        "description": "Un senzor ABS poate transmite semnal incorect.",
        "recommendation": "Verifică senzorii ABS, cablajul și inelele ABS."
    },
    "transmission_issue": {
        "name": "Problemă transmisie",
        "description": "Cutia poate schimba greu sau poate avea smucituri.",
        "recommendation": "Verifică nivelul uleiului, erorile TCM și starea ambreiajului/convertizorului."
    },
    "timing_chain_issue": {
        "name": "Problemă lanț distribuție",
        "description": "Lanțul de distribuție poate fi întins sau întinzătorul poate fi uzat.",
        "recommendation": "Verifică zgomotul la pornire, sincronizarea și valorile de fazare."
    },
    "brake_issue": {
        "name": "Problemă sistem frânare",
        "description": "Simptomele indică o posibilă problemă la discuri, plăcuțe, etrier sau sistem hidraulic.",
        "recommendation": "Verifică discurile, plăcuțele, etrierii, lichidul de frână și furtunurile."
    },
    "wheel_alignment_issue": {
        "name": "Problemă geometrie roți",
        "description": "Mașina poate avea geometria dereglată sau uzură neuniformă la anvelope.",
        "recommendation": "Verifică presiunea în anvelope, uzura acestora și fă geometria roților."
    },
    "suspension_issue": {
        "name": "Problemă suspensie",
        "description": "Zgomotele la denivelări sau bătăile pot indica bucșe, bielete, amortizoare sau articulații uzate.",
        "recommendation": "Verifică bucșele, bieletele antiruliu, amortizoarele și articulațiile."
    },
    "steering_issue": {
        "name": "Problemă direcție",
        "description": "Jocul în volan sau faptul că mașina trage într-o parte poate indica probleme la direcție.",
        "recommendation": "Verifică bieletele de direcție, capetele de bară, caseta de direcție și geometria."
    },
    "wheel_bearing_issue": {
        "name": "Problemă rulment roată",
        "description": "Zgomotul metalic sau bătaia în roată poate indica un rulment uzat.",
        "recommendation": "Verifică jocul roții, zgomotul la rotire și starea rulmentului."
    },
}


def get_fault_info(fault_code: str):
    return FAULT_EXPLANATIONS.get(fault_code, {
        "name": fault_code,
        "description": "Nu există explicație definită pentru această defecțiune.",
        "recommendation": "Se recomandă verificare suplimentară."
    })