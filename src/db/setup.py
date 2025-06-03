# src/db/setup.py
from src.db.database import engine
from src.db.models import Base

def create_all():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_all()
    print("Tablas creadas.")
