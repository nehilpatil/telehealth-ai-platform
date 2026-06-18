import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///telehealth.db"
    )

    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "gpt-4o-mini"
    )

    GITHUB_MODELS_ENDPOINT = os.getenv(
        "GITHUB_MODELS_ENDPOINT",
        "https://models.inference.ai.azure.com"
    )

settings = Settings()