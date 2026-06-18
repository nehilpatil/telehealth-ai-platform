from pydantic import BaseModel

class PatientInfo(BaseModel):
    patient_name: str
    age: int
    symptoms: str
    duration: str
    # patient_email: str