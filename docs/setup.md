# Setup rápido

```bash
# 1. clona y crea venv
git clone <repo>; cd <repo>
python -m venv .venv && source .venv/bin/activate
make setup        # instala deps + pre-commit

# 2. arranca Postgres
docker compose up -d db

# 3. carga datos dummy y levanta API
make etl
./run.py serve-api
