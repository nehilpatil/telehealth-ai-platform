from graph.state import PatientState
from llm import llm
from schemas.patient import PatientInfo


def extraction_agent(state: PatientState):
    print("Extraction Agent Running...")

    intake_form = state["intake_form"]

    structured_llm = llm.with_structured_output(PatientInfo)

    result = structured_llm.invoke(
        f"""
        Extract patient information from this intake form.

        Intake Form:
        {intake_form}
        """
    )

    return {
        "patient_name": result.patient_name,
        "age": result.age,
        "symptoms": result.symptoms,
        "duration": result.duration,
    }