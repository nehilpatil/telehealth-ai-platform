from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class PatientCase(Base):
    __tablename__ = "patient_cases"

    id = Column(Integer, primary_key=True, index=True)

    patient_name = Column(String)
    age = Column(Integer)

    symptoms = Column(String)
    duration = Column(String)

    risk_level = Column(String)
    specialty = Column(String)

    assigned_clinician = Column(String)
    
    user_id = Column(Integer, nullable=True)
    
class Clinician(Base):
    __tablename__ = "clinicians"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    specialty = Column(String, nullable=False)
    
    user_id = Column(Integer, nullable=True)
     
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_name = Column(String, nullable=False)

    clinician_id = Column(
        Integer,
        ForeignKey("clinicians.id")
    )

    start_time = Column(DateTime)

    end_time = Column(DateTime)

    status = Column(
        String,
        default="scheduled"
    )

    clinician = relationship(
        "Clinician"
    )
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    role = Column(String, nullable=False)
    
    name = Column(String, nullable=False)
    
