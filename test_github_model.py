from llm import llm
from schemas.patient import PatientInfo

structured_llm = llm.with_structured_output(PatientInfo)

result = structured_llm.invoke("""
Name: John Doe
Age: 45
Symptoms: Chest pain
Duration: 2 days
""")

print(result)