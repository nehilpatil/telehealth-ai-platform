from graph.state import PatientState


def validation_router(state: PatientState):
    if state["validation_status"] == "valid":
        return "valid"

    return "invalid"