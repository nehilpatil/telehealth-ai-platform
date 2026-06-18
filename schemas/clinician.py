from pydantic import BaseModel

class ClinicianCreate(BaseModel):
    name: str
    email: str
    password: str
    specialty: str