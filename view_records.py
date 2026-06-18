from database.db import SessionLocal
from database.models import PatientCase

db = SessionLocal()

cases = db.query(PatientCase).all()

for case in cases:
    print("-" * 50)
    print(f"ID: {case.id}")
    print(f"Patient: {case.patient_name}")
    print(f"Age: {case.age}")
    print(f"Symptoms: {case.symptoms}")
    print(f"Risk: {case.risk_level}")
    print(f"Specialty: {case.specialty}")
    print(f"Clinician: {case.assigned_clinician}")

db.close()