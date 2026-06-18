from graph.workflow import graph
from database.db import engine
from database.repository import save_patient_case

result = graph.invoke(
    {
        "intake_form": """
        Name: Deboo Patil
        Age: 23
        Symptoms: Chest pain
        Duration: 2 days
        """
    }
)

save_patient_case(result)

print(result)