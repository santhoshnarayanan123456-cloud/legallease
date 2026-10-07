import os
from functools import lru_cache

from dotenv import load_dotenv


load_dotenv()


class Settings:

    def __init__(self):

        self.gemini_api_key = os.getenv(
            "GEMINI_API_KEY",
            ""
        ).strip()

        self.gemini_model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        ).strip()

        self.backend_url = os.getenv(
            "BACKEND_URL",
            "http://127.0.0.1:8000"
        ).rstrip("/")


@lru_cache
def get_settings():

    return Settings()