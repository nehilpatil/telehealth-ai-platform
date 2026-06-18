from langgraph.graph import StateGraph
from graph.state import PatientState
from graph.router import validation_router

from agents.extraction import extraction_agent
from agents.validation import validation_agent
from agents.followup import followup_agent
from agents.risk import risk_agent
from agents.specialty import specialty_agent
from agents.assignment import assignment_agent
from agents.notification import notification_agent
from agents.history import history_agent
from agents.appointment import appointment_agent


builder = StateGraph(PatientState)

builder.add_node("extract", extraction_agent)
builder.add_node("validate", validation_agent)
builder.add_node("followup", followup_agent)
builder.add_node("risk", risk_agent)
builder.add_node("specialty", specialty_agent)
builder.add_node("assignment", assignment_agent)
builder.add_node("notification", notification_agent)
builder.add_node("history", history_agent)
builder.add_node("appointment", appointment_agent)
builder.set_entry_point("extract")

builder.add_edge("extract", "validate")

builder.add_conditional_edges(
    "validate",
    validation_router,
    {
        "valid": "history",
        "invalid": "followup"
    }
)

builder.add_edge("history", "risk")
builder.add_edge("risk", "specialty")
builder.add_edge("specialty", "assignment")
builder.add_edge("assignment", "appointment")
builder.add_edge("appointment", "notification")
builder.set_finish_point("notification")
builder.set_finish_point("followup")

graph = builder.compile()