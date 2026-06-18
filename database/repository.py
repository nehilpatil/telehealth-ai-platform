from database.db import SessionLocal
from database.models import PatientCase
from database.models import Clinician, Appointment
from database.models import Appointment
from database.models import User


def save_patient_case(state, user_id):
    db = SessionLocal()

    try:
        patient_case = PatientCase(
            patient_name=state.get("patient_name"),
            age=state.get("age"),
            symptoms=state.get("symptoms"),
            duration=state.get("duration"),
            risk_level=state.get("risk_level"),
            specialty=state.get("specialty"),
            assigned_clinician=state.get("assigned_clinician"),
            user_id=user_id,
        )

        db.add(patient_case)
        db.commit()

    finally:
        db.close()
        
def get_patient_history(patient_name: str):
    db = SessionLocal()

    try:
        return (
            db.query(PatientCase)
            .filter(PatientCase.patient_name == patient_name)
            .all()
        )
    finally:
        db.close()
        
        
def get_available_clinician(specialty: str):
    db = SessionLocal()

    try:
        clinicians = (
            db.query(Clinician)
            .filter(Clinician.specialty == specialty)
            .all()
        )

        best_clinician = None
        minimum_appointments = float("inf")

        for clinician in clinicians:

            appointment_count = (
                db.query(Appointment)
                .filter(
                    Appointment.clinician_id == clinician.id,
                    Appointment.status == "scheduled"
                )
                .count()
            )

            if appointment_count < minimum_appointments:
                minimum_appointments = appointment_count
                best_clinician = clinician

        return best_clinician

    finally:
        db.close()
        
from datetime import datetime, timedelta
from database.models import Appointment



def create_appointment(
    patient_name: str,
    clinician_id: int
):
    db = SessionLocal()

    try:
        next_available_time = get_next_available_time(
            clinician_id
        )

        appointment = Appointment(
            patient_name=patient_name,
            clinician_id=clinician_id,
            start_time=next_available_time,
            end_time=next_available_time + timedelta(minutes=30),
            status="scheduled"
        )

        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        
        return appointment

    finally:
        db.close()
        

def get_earliest_available_clinician(specialty: str):
    db = SessionLocal()

    try:
        clinicians = (
            db.query(Clinician)
            .filter(
                Clinician.specialty == specialty
            )
            .all()
        )

        best_clinician = None
        earliest_end_time = None

        for clinician in clinicians:

            latest_appointment = (
                db.query(Appointment)
                .filter(
                    Appointment.clinician_id == clinician.id,
                    Appointment.status == "scheduled"
                )
                .order_by(
                    Appointment.end_time.desc()
                )
                .first()
            )

            if latest_appointment is None:
                return clinician

            if (
                earliest_end_time is None
                or latest_appointment.end_time < earliest_end_time
            ):
                earliest_end_time = (
                    latest_appointment.end_time
                )

                best_clinician = clinician

        return best_clinician

    finally:
        db.close()
        
def get_next_available_time(clinician_id: int):
    db = SessionLocal()

    try:
        latest_appointment = (
            db.query(Appointment)
            .filter(
                Appointment.clinician_id == clinician_id,
                Appointment.status == "scheduled"
            )
            .order_by(
                Appointment.end_time.desc()
            )
            .first()
        )

        if latest_appointment:
            return latest_appointment.end_time

        return datetime.now()

    finally:
        db.close()


def update_appointment_status(appointment_id: int, status: str):
    valid_statuses = {"scheduled", "completed", "cancelled"}
    if status not in valid_statuses:
        raise ValueError(f"Invalid status '{status}'. Must be one of {valid_statuses}")

    db = SessionLocal()
    try:
        appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if not appointment:
            return None
        appointment.status = status
        db.commit()
        db.refresh(appointment)
        return appointment
    finally:
        db.close()


def get_all_patient_cases():
    db = SessionLocal()
    try:
        cases = db.query(PatientCase).order_by(PatientCase.id.desc()).all()
        return [
            {
                "id": c.id,
                "patient_name": c.patient_name,
                "age": c.age,
                "symptoms": c.symptoms,
                "duration": c.duration,
                "risk_level": c.risk_level,
                "specialty": c.specialty,
                "assigned_clinician": c.assigned_clinician,
            }
            for c in cases
        ]
    finally:
        db.close()
        
from database.models import User


def create_user(
    email: str,
    hashed_password: str,
    role: str,
    name: str = ""
):
    db = SessionLocal()

    try:
        user = User(
            name=name,
            email=email,
            hashed_password=hashed_password,
            role=role
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    finally:
        db.close()
        
from database.models import User


def get_user_by_email(email: str):
    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        return user

    finally:
        db.close()
        
def get_all_users():
    db = SessionLocal()

    try:
        return db.query(User).all()

    finally:
        db.close()
        
def get_all_appointments():
    db = SessionLocal()

    try:
        return db.query(Appointment).all()

    finally:
        db.close()
        
def get_appointments_by_clinician(
    clinician_id: int
):
    db = SessionLocal()

    try:
        return (
            db.query(Appointment)
            .filter(
                Appointment.clinician_id == clinician_id
            )
            .all()
        )

    finally:
        db.close()
        
def get_clinician_by_user_id(
    user_id: int
):
    db = SessionLocal()

    try:
        return (
            db.query(Clinician)
            .filter(
                Clinician.user_id == user_id
            )
            .first()
        )

    finally:
        db.close()
        
def get_user_by_id(user_id: int):
    db = SessionLocal()

    try:
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    finally:
        db.close()
        
def get_patient_cases_by_user_id(
    user_id: int
):
    db = SessionLocal()

    try:
        return (
            db.query(PatientCase)
            .filter(
                PatientCase.user_id == user_id
            )
            .all()
        )

    finally:
        db.close()
        
#create clinician
def create_clinician_record(
    name: str,
    specialty: str,
    user_id: int
):
    db = SessionLocal()

    try:
        clinician = Clinician(
            name=name,
            specialty=specialty,
            user_id=user_id
        )

        db.add(clinician)
        db.commit()
        db.refresh(clinician)

        return clinician

    finally:
        db.close()
        
def update_appointment_status(
    appointment_id: int,
    status: str
):
    db = SessionLocal()

    try:
        appointment = (
            db.query(Appointment)
            .filter(
                Appointment.id == appointment_id
            )
            .first()
        )

        if not appointment:
            return None

        appointment.status = status

        db.commit()
        db.refresh(appointment)

        return appointment

    finally:
        db.close()
        