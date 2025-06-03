# src/api/auth.py
import os
from fastapi import Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from jose import JWTError, jwt
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.datastructures import URL

# Carga variables de entorno
config = Config(".env")
SECRET_KEY = config("SECRET_KEY", cast=str, default="changeme")
GOOGLE_CLIENT_ID = config("OAUTH_CLIENT_ID", cast=str, default=None)
GOOGLE_CLIENT_SECRET = config("OAUTH_CLIENT_SECRET", cast=str, default=None)

# Instancia OAuth
oauth = OAuth(config)
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


def add_oauth_middleware(app):
    """
    Añade SessionMiddleware necesario para manejar sesiones (cookies) en FastAPI.
    Llama esto desde main.py antes de incluir routers.
    """
    app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, session_cookie="session")


async def login(request: Request):
    """
    Redirige a Google para autenticación.
    """
    # after login, Google llamará a /auth
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


async def auth_callback(request: Request):
    """
    Callback de Google que guarda datos de usuario en sesión.
    """
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        raise HTTPException(status_code=400, detail=f"OAuth Error: {error.error}")

    user_info = token.get("userinfo") or await oauth.google.parse_id_token(request, token)
    # Almacena en sesión: name, email, picture
    request.session["user"] = {
        "name": user_info["name"],
        "email": user_info["email"],
        "picture": user_info.get("picture", ""),
    }
    # Luego rediriges a front (p. ej. dashboard principal)
    return RedirectResponse(url="/")


def get_current_user(request: Request):
    """
    Dependencia para proteger endpoints: debe haber usuario en sesión.
    """
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


async def logout(request: Request):
    """
    Limpia la sesión y redirige a home.
    """
    request.session.pop("user", None)
    return RedirectResponse(url="/")
