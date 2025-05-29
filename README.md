# ChoriPy

```bash
git clone <repo> && cd <repo>
make setup  # crea venv e instala deps
cp .env.example .env  # configura URL_DB, etc.
make etl     # corre pipeline completo
make run-api # levanta FastAPI en http://127.0.0.1:8000
make test    # corre tests
```
