from fastapi import FastAPI
from rich.logging import RichHandler
import logging

logging.basicConfig(handlers=[RichHandler()], level=logging.INFO)
app = FastAPI(title="ChoriPy API")


@app.get("/")
def root():
    return {"msg": "Hola FastAPI 🚀"}
