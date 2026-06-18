from database.db import SessionLocal
from database.models import Clinician

db = SessionLocal()

clinicians = [
    Clinician(
        name="Dr Sarah Johnson",
        specialty="Cardiology"
    ),
    Clinician(
        name="Dr James Wilson",
        specialty="Cardiology"
    ),
    Clinician(
        name="Dr Emily Davis",
        specialty="Neurology"
    ),
    Clinician(
        name="Dr Michael Lee",
        specialty="Dermatology"
    )
]

for clinician in clinicians:
    db.add(clinician)

db.commit()
db.close()

print("Clinicians seeded successfully!")

