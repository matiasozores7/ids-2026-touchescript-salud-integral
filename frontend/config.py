import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    API_BASE_URL = os.environ.get("API_BASE_URL","http://127.0.0.1:5000/api")
    PORT = int(os.environ.get("FRONTEND_PORT", 5001))
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() == "true"