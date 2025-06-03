# src/db/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")

# Para PostgreSQL asyncpg podrías usar: 
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://...")

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
