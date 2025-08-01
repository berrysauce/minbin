# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration class. Loads environment variables and provides default values."""

    # app config
    APP_DOMAIN = os.getenv("APP_DOMAIN", "minb.in")

    # redis connection
    DB_HOST = str(os.getenv("DB_HOST", "dragonfly"))
    DB_PORT = int(os.getenv("DB_PORT", "6379"))
    DB_USER = os.getenv("DB_USER", None)
    DB_PASS = os.getenv("DB_PASS", None)

    # paste settings
    PASTE_EXPIRY = int(os.getenv("PASTE_EXPIRY", "60"))  # default 1 minute
    MAX_PASTE_SIZE = int(
        os.getenv("MAX_PASTE_SIZE", str(1024 * 1024 * 25))
    )  # default 25 MB
