def analyze_text(text):
    text_lower = text.lower()

    adverse_events = []

    symptoms = {
        "bleeding_problems": [
            "bleeding", "bleeding gums", "blood in stool", "nosebleed",
            "bruising", "easy bruising"
        ],
        "breathing_problems": [
            "shortness of breath", "can't breathe", "cannot breathe",
            "breathless", "winded", "trouble breathing"
        ],
        "chest_pain": [
            "chest pain", "pressure in chest", "tightness in chest"
        ],
        "constipation": [
            "constipation", "can't go", "not having bowel movements",
            "hard stool"
        ],
        "depression_anxiety": [
            "anxiety", "depressed", "feeling down", "panic", "hopeless",
            "suicidal", "suicidal thoughts"
        ],
        "diarrhea": [
            "diarrhea", "loose stools", "frequent stools",
            "watery stool", "runs"
        ],
        "dizziness_lightheadedness": [
            "dizzy", "lightheaded", "felt faint", "almost passed out"
        ],
        "edema": [
            "swelling", "swollen feet", "swollen ankles",
            "puffy legs", "fluid retention"
        ],
        "headache": [
            "headache", "migraine", "head pain"
        ],
        "infection": [
            "infection", "fever", "chills", "signs of infection"
        ],
        "influenza": [
            "flu", "influenza", "body aches", "viral symptoms"
        ],
        "injection_site_reaction": [
            "injection site reaction", "redness at injection site",
            "bump at injection site", "pain at injection site"
        ],
        "joint_pain": [
            "joint pain", "aching joints", "knees hurt", "elbow pain"
        ],
        "liver_damage": [
            "yellow skin", "yellow eyes", "dark urine",
            "liver pain", "pain on right side"
        ],
        "nausea_vomiting": [
            "nausea", "nauseous", "queasy",
            "vomiting", "throwing up", "threw up",
            "sick to my stomach"
        ],
        "neuropathy": [
            "tingling", "numbness", "burning",
            "pins and needles", "hands feel funny",
            "feet feel funny"
        ],
        "fatigue": [
            "tired", "fatigue", "exhausted",
            "no energy", "worn out", "weak"
        ],
        "weight_loss": [
            "weight loss", "lost weight",
            "not eating", "lost appetite"
        ]
    }

    negations = ["no", "not", "denies", "without", "never"]

    for symptom, keywords in symptoms.items():
        for word in keywords:
            if word in text_lower:
                status = "present"

                for neg in negations:
                    if f"{neg} {word}" in text_lower:
                        status = "negated"

                adverse_events.append({
                    "symptom": symptom,
                    "status": status,
                    "matched_phrase": word
                })

                break

    timing = "unknown"
    if any(word in text_lower for word in ["after", "since", "today", "yesterday", "last"]):
        timing = "reported"

    medication_flag = any(word in text_lower for word in [
        "medication", "med", "drug", "tablet", "pill",
        "treatment", "therapy", "chemo", "injection",
        "abiraterone", "abrilada", "actemra", "acthar gel",
        "adalimumab", "adbry", "adcirca", "afinitor", "alecensa",
        "alkeran", "ambrisentan", "amjevvita", "apomorphine",
        "aubagio", "austedo", "avonex", "bafiertam", "betaseron",
        "bethkis", "bexarotene", "bimzelx", "bosentan",
        "dupixent"

    ])

    serious_triggers = [
        "hospital", "hospitalized", "admitted",
        "er", "emergency room",
        "life threatening",
        "couldn't breathe", "cannot breathe",
        "passed out", "unconscious", "seizure",
        "wheelchair", "blind", "blindness",
        "permanent damage", "permanent impairment",
        "disability", "death", "died", "ambulance"
    ]

    moderate_triggers = [
        "really bad", "bothersome", "getting worse",
        "hard to", "difficult to", "struggling",
        "affecting daily life", "affecting work", "affecting sleep",
        "needed medication", "needed treatment", "needed intervention",
        "had to take something", "missed work", "couldn't function",
        "can't leave my house", "cannot leave my house"
    ]

    mild_triggers = [
        "mild", "a little", "slight", "manageable",
        "not too bad", "comes and goes"
    ]

    severity = "mild"
    severity_reason = "defaulted to mild"

    if any(word in text_lower for word in serious_triggers):
        severity = "severe"
        severity_reason = "serious outcome detected"
    elif any(word in text_lower for word in moderate_triggers):
        severity = "moderate"
        severity_reason = "activity limitation or intervention detected"
    elif any(word in text_lower for word in mild_triggers):
        severity = "mild"
        severity_reason = "mild symptom language detected"

    serious_ae = any(word in text_lower for word in serious_triggers)

    return {
        "input": text,
        "patient_quote": text,
        "adverse_events": adverse_events,
        "timing_detected": timing,
        "medication_mentioned": medication_flag,
        "severity": severity,
        "serious_adverse_event": serious_ae,
        "compliance_flag": len(adverse_events) > 0,
        "severity_reason": severity_reason
    }
