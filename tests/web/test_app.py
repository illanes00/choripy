# tests/web/test_app.py
import pytest
from flask import url_for
from src.web.app import app as flask_app
from src.db.models import Base, User, Page
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

@pytest.fixture
def client(monkeypatch, tmp_path):
    """
    Crea app de Flask en testing, con BD SQLite en memoria.
    """
    # BD en memoria
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["WTF_CSRF_ENABLED"] = False  # si usas formularios WTForms
    # Overwrite el db.session de la app
    flask_app.db = Session()
    with flask_app.test_client() as client:
        yield client

def test_healthz_flask(client):
    res = client.get("/healthz")
    assert res.status_code == 200
    data = res.get_json()
    assert data["flask"] == "ok"
    # FastAPI no corre en tests, debería decir "down"
    assert data["fastapi"] == "down"

def test_metrics_proxy_error(monkeypatch, client):
    # Simular que FastAPI no está arriba
    def fake_get(*args, **kwargs):
        raise Exception("no levantar FastAPI")
    monkeypatch.setattr("src.web.app.requests.get", fake_get)
    res = client.get("/metrics")
    assert res.status_code == 500
    assert b"Error proxy métricas" in res.data

def test_page_not_found(client):
    res = client.get("/page/no-existe")
    assert res.status_code == 404

def test_create_user_and_page(client):
    # Insertar directamente en la DB
    session = flask_app.db
    user = User(
        email="u@ejemplo.com",
        name="UserTest",
        is_admin=True,
        created_at=datetime.datetime.utcnow()
    )
    session.add(user)
    session.commit()
    page = Page(
        slug="test-slug",
        title="Título de Prueba",
        content="Contenido",
        created_by=user.id,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )
    session.add(page)
    session.commit()

    # Ahora pedir la ruta /page/<slug>
    res = client.get("/page/test-slug")
    assert res.status_code == 200
    assert b"Título de Prueba" in res.data
