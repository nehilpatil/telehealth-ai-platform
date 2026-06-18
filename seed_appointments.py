from datetime import datetime, timedelta

from database.db import SessionLocal
from database.models import Appointment

db = SessionLocal()

appointments = [
    Appointment(
        patient_name="Existing Patient 1",
        clinician_id=1,
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(minutes=30),
        status="scheduled"
    ),
    Appointment(
        patient_name="Existing Patient 2",
        clinician_id=1,
        start_time=datetime.now() + timedelta(minutes=30),
        end_time=datetime.now() + timedelta(minutes=60),
        status="scheduled"
    ),
    Appointment(
        patient_name="Existing Patient 3",
        clinician_id=2,
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(minutes=30),
        status="scheduled"
    )
]

for appointment in appointments:
    db.add(appointment)

db.commit()
db.close()

print("Appointments seeded successfully!")