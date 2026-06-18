from pydantic import BaseModel


class IntakeRequest(BaseModel):
    intake_form: str