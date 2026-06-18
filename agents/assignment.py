from graph.state import PatientState
from database.repository import (
    get_earliest_available_clinician
)


def assignment_agent(state: PatientState):
    print("Assignment Agent Running...")

    specialty = state.get("specialty")

    doctor = get_earliest_available_clinician(
    state["specialty"]
   )

    return {
        "assigned_clinician": doctor.name,
        "assigned_clinician_id": doctor.id
    }


