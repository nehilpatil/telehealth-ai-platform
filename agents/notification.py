from graph.state import PatientState


def notification_agent(state: PatientState):
    print("Notification Agent Running...")

    clinician = state.get("assigned_clinician")
    patient = state.get("patient_name")
    risk = state.get("risk_level")

    print(
        f"Notify {clinician}: "
        f"Patient {patient} assigned "
        f"(Risk: {risk})"
    )

    return {
        "notification_sent": True
    }