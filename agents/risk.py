from graph.state import PatientState
from llm import llm
from schemas.risk import RiskAssessment
from utils.logger import logger


def risk_agent(state: PatientState):
    logger.info("Risk Agent Running...")

    symptoms = state.get("symptoms", "")
    history = state.get("patient_history", "")

    structured_llm = llm.with_structured_output(
        RiskAssessment
    )

    result = structured_llm.invoke(
    f"""
    You are a medical triage assistant.

    Assess the patient's risk level.

    Current Symptoms:
    {symptoms}

    Previous Patient History:
    {history}

    Consider both the current symptoms and
    previous visits when assessing risk.

    Return:
    - risk_level
    - reasoning
    """
)

    return {
        "risk_level": result.risk_level,
        "risk_reasoning": result.reasoning
    }