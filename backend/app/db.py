import os
from pathlib import Path
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
from sqlalchemy.exc import OperationalError

# Load .env from project root (parent of backend folder)
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# Connection string from environment variable
if not os.getenv("DATABASE_URL"):
    raise ValueError(
        "DATABASE_URL environment variable not set. "
        "Copy .env.example to .env and update with your database credentials."
    )

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

def init_db():
    try:
        SQLModel.metadata.create_all(engine)
    except OperationalError as e:
        print("Database connection error:", e)
        raise

def get_engine():
    return engine