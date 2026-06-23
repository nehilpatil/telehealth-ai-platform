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

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173"
        ).split(",")
        if origin.strip()
    ]

    CORS_ALLOW_ORIGIN_REGEX = os.getenv(
        "CORS_ALLOW_ORIGIN_REGEX",
        r"https?://.*"
    )

settings = Settings()