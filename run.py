#!/usr/bin/env python
from pathlib import Path
import subprocess
import typer
import uvicorn
import signal
from rich.console import Console
from rich.progress import Progress
from dotenv import load_dotenv
import sys
import os
import signal
from pathlib import Path

console = Console()
app = typer.Typer(help="Entry-point CLI para el stack (FastAPI + Flask)")

load_dotenv()


@app.command()
def init():
    """
    Crea .venv, instala requirements y (opcional) compila assets.
    """
    if not Path(".venv").exists():
        console.print(":package: Creando virtualenv…")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)

    pip = Path(".venv/bin/pip")
    console.print(":arrow_down: Instalando dependencias…")
    subprocess.run([str(pip), "install", "-r", "requirements-dev.txt"], check=True)
    console.print(":white_check_mark: Dependencias instaladas")
    console.print("[cyan]Ahora puedes usar 'run.py serve_full' para levantar TODO el stack[/]")



@app.command()
def serve_all():
    """
    Lanza en paralelo:
    - Backend FastAPI con Uvicorn en el puerto 8000
    - Frontend Flask-Admin con Gunicorn en el puerto 5000
    """
    console.print("[green]▶️  Arrancando backend (FastAPI)…[/]")
    backend_proc = subprocess.Popen(
        ["uvicorn", "src.api.main:app", "--reload", "--port", "8000"]
    )

    console.print("[green]▶️  Arrancando frontend (Flask)…[/]")
    frontend_proc = subprocess.Popen(
        ["gunicorn", "src.web.app:app", "--reload", "--bind", "127.0.0.1:5000"]
    )

    def _shutdown(signum, frame):
        console.print("\n[red]🛑  Deteniendo servicios…[/]")
        backend_proc.terminate()
        frontend_proc.terminate()
        sys.exit(0)

    # Capturamos Ctrl+C
    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    # Esperamos a que terminen (normalmente no lo hacen hasta Ctrl+C)
    backend_proc.wait()
    frontend_proc.wait()


@app.command()
def serve_api(host: str = "127.0.0.1", port: int = 8000):
    """
    Lanza sólo el backend FastAPI.
    """
    uvicorn.run("src.api.main:app", host=host, port=port, reload=True)


@app.command()
def flask_demo(host: str = "127.0.0.1", port: int = 5000):
    """
    Lanza sólo el frontend Flask en modo desarrollo.
    """
    from src.web.app import app as flask_app

    flask_app.run(host=host, port=port, debug=True)


@app.command()
def report():
    """
    Renderiza todos los docs de Quarto → HTML/PDF.
    """
    docs_path = Path("docs")
    with Progress() as progress:
        task = progress.add_task("Rendering docs…", total=None)
        subprocess.run(["quarto", "render", str(docs_path)], check=True)
        progress.update(task, completed=True)
    console.print("[bold cyan]Docs construidos en docs/_site[/]")


@app.command()
def open_docs():
    """
    Abre la home de los docs en el navegador.
    """
    index = Path("docs/_site/index.html")
    if not index.exists():
        console.print("[yellow]Docs no están construidos — ejecutando 'report()'...[/]")
        report()
    typer.launch(index.as_uri())


if __name__ == "__main__":
    app()
