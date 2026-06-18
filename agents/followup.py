from graph.state import PatientState


def followup_agent(state: PatientState):
    print("Follow-up Agent Running...")

    missing = state.get("missing_fields", [])

    return {
        "followup_message": f"Please provide: {', '.join(missing)}"
    }