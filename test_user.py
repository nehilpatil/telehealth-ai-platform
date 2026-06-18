# from database.repository import get_appointments_by_clinician

# appointments = get_appointments_by_clinician(2)

# for appointment in appointments:
#     print(
#         appointment.patient_name,
#         appointment.status
#     )

# from database.db import SessionLocal
# from database.models import User

# db = SessionLocal()

# for user in db.query(User).all():
#     print(user.id, user.email, user.role)

# db.close()

# from database.db import SessionLocal
# from database.models import Appointment

# db = SessionLocal()

# appointments = db.query(Appointment).all()

# for a in appointments:
#     print(
#         a.patient_name,
#         a.clinician_id
#     )

# db.close()

from database.db import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(
        text(
            "ALTER TABLE patient_cases ADD COLUMN user_id INTEGER"
        )
    )
    conn.commit()

print("user_id column added to patient_cases")