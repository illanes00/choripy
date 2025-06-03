# src/web/app.py
import os
from flask import Flask, session, redirect, url_for, render_template, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babel import Babel
from authlib.integrations.flask_client import OAuth
from flask import Response, jsonify
import markdown
import requests

# 1. Importar setup_logging
from src.core.logging_setup import setup_logging

# 2. Inicializar logging para Flask
setup_logging(log_filename="logs/app.log")

import logging
logger = logging.getLogger(__name__)
logger.info("📣 Plataforma Flask arrancando con logging rotativo…")

# 3. Crear la app Flask
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "changeme")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///./db.sqlite3"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ---------- Babel (i18n) ----------
babel = Babel(app)
app.config["BABEL_DEFAULT_LOCALE"] = "es"
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(["es", "en"])

# ---------- OAuth (Google) ----------
oauth = OAuth(app)
CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth.register(
    name="google",
    client_id=os.getenv("OAUTH_CLIENT_ID"),
    client_secret=os.getenv("OAUTH_CLIENT_SECRET"),
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
)

# ---------- Inicializar DB ----------
db = SQLAlchemy(app)

# ---------- Modelos ----------
from src.db.models import User as UserModel, Page as PageModel
User = UserModel
Page = PageModel

# ---------- Vistas protegidas (igual que antes) ----------
class SecureModelView(ModelView):
    def is_accessible(self):
        user = session.get("user")
        # Solo correos de tu dominio (ajusta si es necesario)
        return bool(user and user.get("email", "").endswith("@tudominio.cl"))

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))

admin = Admin(app, name="AdminPanel", template_mode="bootstrap4")
admin.add_view(SecureModelView(User, db.session, category="Usuarios"))
admin.add_view(SecureModelView(Page, db.session, category="Páginas"))

# ---------- Rutas login/logout, páginas, métricas, health (idéntico a paso 3) ----------
@app.route("/login")
def login():
    redirect_uri = url_for("auth_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route("/auth")
def auth_callback():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)
    session["user"] = {
        "name": user_info["name"],
        "email": user_info["email"],
        "picture": user_info.get("picture", ""),
    }
    return redirect(url_for("admin.index"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/page/<slug>")
def render_page(slug):
    page = Page.query.filter_by(slug=slug).first_or_404()
    html = markdown.markdown(page.content or "")
    return render_template("page.html", title=page.title, content=html)


@app.route("/metrics")
def proxy_metrics():
    """
    Proxy a FastAPI /metrics.
    Llama internamente a http://localhost:8000/metrics y reenvía el contenido.
    """
    try:
        r = requests.get("http://localhost:8000/metrics", timeout=2)
        return Response(
            r.content,
            status=r.status_code,
            mimetype=r.headers.get("Content-Type", "text/plain")
        )
    except Exception as e:
        app.logger.error(f"Error proxy /metrics: {e}")
        return Response(f"Error proxy metrics: {e}", status=500)

@app.route("/healthz")
def flask_healthz():
    """
    Health integrado: verifica FastAPI y reporta estado de Flask.
    """
    try:
        resp = requests.get("http://localhost:8000/healthz", timeout=2)
        fastapi_status = resp.json().get("status", "down")
    except Exception:
        fastapi_status = "down"

    flask_status = "ok"
    return jsonify({"flask": flask_status, "fastapi": fastapi_status})


# ---------- run (solo para debug local) ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
