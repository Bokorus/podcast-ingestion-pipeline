import os
from dotenv import load_dotenv
from pathlib import Path
import mysql.connector

# go to the project root and load the '.env' file
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )