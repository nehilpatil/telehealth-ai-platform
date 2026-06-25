from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from graph.workflow import graph
from database.repository import save_patient_case, update_appointment_status, get_all_patient_cases

from schemas.intake_request import IntakeRequest
from schemas.user import UserRegister
from database.repository import create_user

#User authentication imports
from schemas.user import UserLogin
from database.repository import get_user_by_email
from auth.jwt_handler import create_access_token

#jwt decoding for protected routes
from fastapi import Depends
from auth.dependencies import get_current_user

#admin dependency
from fastapi import Depends
from auth.dependencies import (
    get_current_user,
    require_admin
)
from database.repository import get_all_users
from database.repository import get_all_appointments

#clinician imports
from database.repository import (
    get_clinician_by_user_id,
    get_appointments_by_clinician
)

from schemas.clinician import ClinicianCreate
from auth.dependencies import get_current_user

app = FastAPI()

from config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ALLOW_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



from fastapi import Depends

from auth.dependencies import get_current_user


@app.post("/intake")
def process_intake(
    request: IntakeRequest,
    current_user=Depends(get_current_user)
):

    result = graph.invoke(
        {
            "intake_form": request.intake_form
        }
    )

    user = get_user_by_email(
        current_user["email"]
    )

    save_patient_case(
        result,
        user.id
    )

    return result


class StatusUpdate(BaseModel):
    status: str


@app.patch("/appointments/{appointment_id}/status")
def update_status(appointment_id: int, body: StatusUpdate):
    try:
        appointment = update_appointment_status(appointment_id, body.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return {
        "id": appointment.id,
        "status": appointment.status,
        "patient_name": appointment.patient_name,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/patients")
def get_patients():
    cases = get_all_patient_cases()
    return cases

@app.post("/register")
def register(user: UserRegister):

    created_user = create_user(
        email=user.email,
        hashed_password=user.password,
        role=user.role,
        name=user.name
    )

    return {
        "id": created_user.id,
        "name": created_user.name,
        "email": created_user.email,
        "role": created_user.role
    }
    
@app.post("/login")
def login(user: UserLogin):

    existing_user = get_user_by_email(
        user.email
    )

    if not existing_user:
        return {
            "success": False,
            "message": "User not found"
        }

    if existing_user.hashed_password != user.password:
        return {
            "success": False,
            "message": "Invalid password"
        }

    token = create_access_token(
    {
        "name": existing_user.name,
        "email": existing_user.email,
        "role": existing_user.role
    }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": existing_user.role
    }
    
@app.get("/me")
def me(
    current_user=Depends(
        get_current_user
    )
):
    return current_user
        
@app.get("/admin")
def admin_dashboard(
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    return {
        "message": "Welcome Admin"
    }
    
@app.get("/users")
def get_users(
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    users = get_all_users()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
        for user in users
    ]
    
@app.get("/appointments")
def get_appointments(
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    appointments = get_all_appointments()

    return [
        {
            "id": appointment.id,
            "patient_name": appointment.patient_name,
            "clinician_id": appointment.clinician_id,
            "start_time": appointment.start_time,
            "end_time": appointment.end_time,
            "status": appointment.status
        }
        for appointment in appointments
    ]
    
    
@app.get("/my-appointments")
def my_appointments(
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "clinician":
        return {
            "detail": "Clinician access required"
        }

    user = get_user_by_email(
        current_user["email"]
    )

    clinician = get_clinician_by_user_id(
        user.id
    )

    appointments = get_appointments_by_clinician(
        clinician.id
    )

    return [
        {
            "id": appointment.id,
            "patient_name": appointment.patient_name,
            "start_time": appointment.start_time,
            "status": appointment.status
        }
        for appointment in appointments
    ]
from database.repository import get_patient_cases_by_user_id 
@app.get("/my-history")
def my_history(
    current_user=Depends(get_current_user)
):

    user = get_user_by_email(
        current_user["email"]
    )

    cases = get_patient_cases_by_user_id(
        user.id
    )

    return cases
  
#create clinician endpoint for admin users
from database.repository import (
    create_user,
    create_clinician_record,
    get_user_by_email
)


@app.post("/admin/create-clinician")
def create_clinician(
    clinician: ClinicianCreate,
    current_user=Depends(get_current_user)
):
    
    if current_user["role"] != "admin":
        return {
            "success": False,
            "message": "Admin access required"
        }

    existing_user = get_user_by_email(
    clinician.email
    )

    if existing_user:
        return {
            "success": False,
            "message": "Email already exists"
        }

    user = create_user(
        email=clinician.email,
        hashed_password=clinician.password,
        role="clinician",
        name=clinician.name
    )

    create_clinician_record(
        name=clinician.name,
        specialty=clinician.specialty,
        user_id=user.id
    )

    return {
        "success": True,
        "message": "Clinician created successfully"
    }
    
#Appointment update endpoint for clinicians
from database.repository import update_appointment_status
@app.put("/appointments/{appointment_id}/complete")
def complete_appointment(
    appointment_id: int,
    current_user=Depends(get_current_user)
):

    if current_user["role"] != "clinician":
        return {
            "success": False,
            "message": "Clinician access required"
        }

    appointment = update_appointment_status(
        appointment_id,
        "completed"
    )

    if not appointment:
        return {
            "success": False,
            "message": "Appointment not found"
        }

    return {
        "success": True,
        "message": "Appointment marked as completed"
    }
    
#cancel appointment endpoint for clinicians
@app.put("/appointments/{appointment_id}/cancel")
def cancel_appointment(
    appointment_id: int,
    current_user=Depends(get_current_user)
):

    if current_user["role"] != "clinician":
        return {
            "success": False,
            "message": "Clinician access required"
        }

    appointment = update_appointment_status(
        appointment_id,
        "cancelled"
    )

    if not appointment:
        return {
            "success": False,
            "message": "Appointment not found"
        }

    return {
        "success": True,
        "message": "Appointment marked as cancelled"
    }