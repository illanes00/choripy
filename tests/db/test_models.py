# tests/db/test_models.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import Base, User, Page
import datetime

@pytest.fixture(scope="function")
def db_session(tmp_path, monkeypatch):
    """
    Crea una BD SQLite temporal en memoria y la sesión para cada test.
    """
    engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_user(db_session):
    u = User(
        email="test@ejemplo.com",
        name="Tester",
        is_admin=True,
        created_at=datetime.datetime.utcnow()
    )
    db_session.add(u)
    db_session.commit()
    q = db_session.query(User).filter_by(email="test@ejemplo.com").first()
    assert q is not None
    assert q.name == "Tester"

def test_create_page(db_session):
    # Primero crear user
    user = User(
        email="owner@ejemplo.com",
        name="Owner",
        is_admin=False,
        created_at=datetime.datetime.utcnow()
    )
    db_session.add(user)
    db_session.commit()

    page = Page(
        slug="hola-mundo",
        title="Hola Mundo",
        content="**Markdown** de prueba",
        created_by=user.id,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )
    db_session.add(page)
    db_session.commit()

    q = db_session.query(Page).filter_by(slug="hola-mundo").first()
    assert q is not None
    assert q.owner.email == "owner@ejemplo.com"
