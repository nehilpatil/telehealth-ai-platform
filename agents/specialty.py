from graph.state import PatientState
from llm import llm
from schemas.specialty import SpecialtyAssessment


def specialty_agent(state: PatientState):
    print("Specialty Agent Running...")

    symptoms = state.get("symptoms", "")

    structured_llm = llm.with_structured_output(
        SpecialtyAssessment
    )

    result = structured_llm.invoke(
        f"""
        You are a medical routing assistant.

        Determine which medical specialty should
        handle this patient.

        Symptoms:
        {symptoms}

        Possible specialties:
        - Cardiology
        - Dermatology
        - Neurology
        - General Medicine

        Return:
        - specialty
        - reasoning
        """
    )

    return {
        "specialty": result.specialty,
        "specialty_reasoning": result.reasoning
    }
    
    