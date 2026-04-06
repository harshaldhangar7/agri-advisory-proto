import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy.exc import OperationalError

# Default connection string; override with DATABASE_URL env var
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://agriuser:your_password@localhost:3306/agri?charset=utf8mb4"
)

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

def init_db():
    try:
        SQLModel.metadata.create_all(engine)
    except OperationalError as e:
        print("Database connection error:", e)
        raise

def get_engine():
    return engine