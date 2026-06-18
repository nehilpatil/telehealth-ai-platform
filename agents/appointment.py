from datetime import datetime
from graph.state import PatientState
from database.repository import create_appointment


def appointment_agent(state):
    appointment = create_appointment(
        patient_name=state["patient_name"],
        clinician_id=state["assigned_clinician_id"]
    )

    now = datetime.now()
    wait_minutes = max(0, int((appointment.start_time - now).total_seconds() / 60))

    return {
        "appointment_id": appointment.id,
        "appointment_time": appointment.start_time.strftime("%Y-%m-%d %H:%M"),
        "estimated_wait_minutes": wait_minutes,
    }