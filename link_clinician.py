from database.db import SessionLocal
from database.models import Clinician

db = SessionLocal()

sarah = (
    db.query(Clinician)
    .filter(
        Clinician.name == "Dr Sarah Johnson"
    )
    .first()
)

sarah.user_id = 4

db.commit()

print(
    sarah.name,
    sarah.user_id
)

db.close()
# from database.db import SessionLocal
# from database.models import Clinician

# db = SessionLocal()

# for c in db.query(Clinician).all():
#     print(
#         c.id,
#         c.name,
#         c.user_id
#     )

# db.close()

