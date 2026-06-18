from database.repository import get_patient_history

history = get_patient_history("John Doe")

for visit in history:
    print(
        visit.id,
        visit.patient_name,
        visit.symptoms,
        visit.specialty
    )