# Setup rápido (sin Docker)

```bash
# 1. Clona el repo
git clone <repo>
cd <repo>

# 2. Copia y edita variables de entorno
cp .env.example .env
# Modifica en .env: DATABASE_URL, REDIS_URL, SECRET_KEY, OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET...

# 3. Crea y activa el virtualenv, luego instala dependencias
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

# 4. Aplica migraciones Alembic para crear tablas
make migrate

# 5. Arranca FastAPI + Flask
make serve-all
```