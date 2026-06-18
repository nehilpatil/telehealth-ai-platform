from typing import TypedDict, Optional


class PatientState(TypedDict):
    intake_form: str

    # Extracted fields
    patient_name: Optional[str]
    age: Optional[int]
    symptoms: Optional[str]
    duration: Optional[str]
    insurance: Optional[str]
    preferred_location: Optional[str]
    # patient_email: Optional[str]
    patient_history: Optional[str]
    estimated_wait_minutes: Optional[int]

    # Validation
    validation_status: Optional[str]
    missing_fields: Optional[list[str]]
    
    # Follow-up
    followup_message: Optional[str]

    # Risk assessment
    risk_level: Optional[str]
    risk_reasoning: Optional[str]

    # Routing
    specialty: Optional[str]
    assigned_clinician: Optional[str]
    specialty_reasoning: Optional[str]
    assigned_clinician_id: Optional[int]
    appointment_id: Optional[int]
    appointment_time: Optional[str]

    # Notifications
    notification_sent: Optional[bool]
    
    
    