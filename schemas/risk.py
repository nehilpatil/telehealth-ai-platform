from pydantic import BaseModel


class RiskAssessment(BaseModel):
    risk_level: str
    reasoning: str