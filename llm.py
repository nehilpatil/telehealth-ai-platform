from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from config.settings import settings

load_dotenv()

llm = ChatOpenAI(
    model=settings.MODEL_NAME,
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url=settings.GITHUB_MODELS_ENDPOINT,
    temperature=0
)