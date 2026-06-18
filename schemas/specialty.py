from pydantic import BaseModel


class SpecialtyAssessment(BaseModel):
    specialty: str
    reasoning: str