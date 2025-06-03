# src/api/main.py
import os
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# --- Importar setup_logging si aún no lo has hecho (paso 5) ---
from src.core.logging_setup import setup_logging

# Iniciar logging rotativo antes de crear la app
setup_logging(log_filename="logs/app.log")
logger = logging.getLogger(__name__)
logger.info("Init FastAPI con métricas y health")

# Importar helpers de Auth (asume que están en src/api/auth.py)
from .auth import add_oauth_middleware, login, auth_callback, logout, get_current_user

app = FastAPI(title="ChoriPy API")

# Montar estáticos, si los necesitas
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- SessionMiddleware para manejar sesiones (Auth) ---
add_oauth_middleware(app)

# ------------------ Métricas Prometheus ------------------
REQUEST_COUNT = Counter(
    "app_requests_total", "Total HTTP requests", ["method", "endpoint", "http_status"]
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        http_status=response.status_code,
    ).inc()
    return response

@app.get("/metrics")
async def metrics():
    """
    Devuelve las métricas en formato Prometheus.
    """
    data = generate_latest()
    return PlainTextResponse(data, media_type=CONTENT_TYPE_LATEST)

# ------------------ Health endpoint ------------------
@app.get("/healthz")
async def healthz():
    """
    Endpoint de health que solo devuelve {"status":"ok"}.
    """
    return JSONResponse({"status": "ok"})


# ------------------ Rutas de autenticación ------------------
@app.get("/login")
async def route_login(request: Request):
    return await login(request)

@app.get("/auth")
async def route_auth(request: Request):
    return await auth_callback(request)

@app.get("/logout")
async def route_logout(request: Request):
    return await logout(request)


# ------------------ Endpoint raíz ------------------
@app.get("/")
async def root():
    logger.info("Acceso a /")
    return {"msg": "Hola FastAPI 🚀"}


# ------------------ Ejemplo de endpoint protegido ------------------
@app.get("/dashboard")
async def dashboard(user: dict = Depends(get_current_user)):
    logger.info(f"Usuario autenticado: {user['email']}")
    return {"msg": f"Bienvenido, {user['name']}!", "email": user["email"]}
