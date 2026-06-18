from database.repository import (
    get_earliest_available_clinician
)

doctor = get_earliest_available_clinician(
    "Cardiology"
)

print(doctor.name)