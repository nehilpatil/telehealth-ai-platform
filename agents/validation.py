from graph.state import PatientState


def validation_agent(state: PatientState):
    print("Validation Agent Running...")

    required_fields = [
        "patient_name",
        "age",
        "symptoms"
    ]

    missing_fields = []

    for field in required_fields:
        if not state.get(field):
            missing_fields.append(field)

    if missing_fields:
        return {
            "validation_status": "invalid",
            "missing_fields": missing_fields
        }

    return {
        "validation_status": "valid",
        "missing_fields": []
    }