import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

class Config:
    PORT = os.getenv("PORT", 5001)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "salud_integral")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=6400)
    SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_TLS = os.getenv("SMTP_TLS", "False").lower() in ("true", "1")
    SMTP_SSL = os.getenv("SMTP_SSL", "False").lower() in ("true", "1")
    EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE", "Salud Integral <no-reply@saludintegral.com>")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5001")
