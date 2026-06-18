from graph.state import PatientState
from database.repository import get_patient_history


def history_agent(state: PatientState):
    print("History Agent Running...")

    patient_name = state.get("patient_name")

    history_records = get_patient_history(patient_name)

    history_text = ""

    for record in history_records:
        history_text += (
            f"Symptoms: {record.symptoms}, "
            f"Risk: {record.risk_level}, "
            f"Specialty: {record.specialty}\n"
        )

    return {
        "patient_history": history_text
    }