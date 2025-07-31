# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # app config
    APP_DOMAIN = os.getenv("APP_DOMAIN", "minb.in")

    # redis connection
    DB_HOST = str(os.getenv("DB_HOST", "dragonfly"))
    DB_PORT = int(os.getenv("DB_PORT", 6379))
    DB_USER = os.getenv("DB_USER", None)
    DB_PASS = os.getenv("DB_PASS", None)

    # cache expiry
    DEFAULT_EXPIRY = int(os.getenv("DEFAULT_EXPIRY", 60))  # default 1 minute
