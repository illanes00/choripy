#!/usr/bin/env python
from pathlib import Path
import webbrowser
import subprocess
import typer
import uvicorn
from rich.console import Console
from rich.progress import Progress
from dotenv import load_dotenv
import subprocess, sys, venv, shutil, os


console = Console()
app = typer.Typer(help="Entry-point CLI for Seguridad-ETL")

load_dotenv()

@app.command()
def init():
    """Crea .venv, instala requirements y compila assets."""
    if not Path(".venv").exists():
        venv.EnvBuilder(with_pip=True).create(".venv")
    pip = Path(".venv/bin/pip")
    subprocess.run([pip, "install", "-r", "requirements-dev.txt"], check=True)
    console.print("[green]Deps instaladas[/]")

    # compilar SCSS + JS (npm not required, usamos sass CLI)
    subprocess.run(["npm", "install"], check=False)
    subprocess.run(["npm", "run", "build:css"], check=False)

    console.print("[cyan]Assets listos. Ejecuta './run.py up'[/]")

@app.command()
def up():
    """Levanta todo el stack dockerizado + API en caliente."""
    subprocess.run(["docker", "compose", "up", "-d"], check=True)
    serve_api()

@app.callback()
def main(ctx: typer.Context):
    """Seguridad-ETL multipurpose runner."""
    if ctx.invoked_subcommand is None:
        console.print("[bold green]Use --help to see subcommands.[/]")


@app.command()
def serve_api(host: str = "127.0.0.1", port: int = 8000):
    """Launch FastAPI."""
    uvicorn.run("src.api.main:app", host=host, port=port, reload=True)


@app.command()
def flask_demo(host: str = "127.0.0.1", port: int = 5000):
    """Launch tiny Flask demo."""
    from src.api.flask_app import flask_app
    flask_app.run(host=host, port=port, debug=True)


@app.command()
def report():
    """Render all Quarto docs → HTML/PDF."""
    docs_path = Path("docs")
    with Progress() as progress:
        task = progress.add_task("Rendering docs…", total=None)
        subprocess.run(["quarto", "render", str(docs_path)], check=True)
        progress.update(task, completed=True)
    console.print("[bold cyan]Docs built in docs/_site[/]")


@app.command()
def open_docs():
    """Open docs home in browser."""
    index = Path("docs/_site/index.html")
    if not index.exists():
        console.print("[yellow]Docs not built yet — running report()[/]")
        report()
    webbrowser.open(index.as_uri())


if __name__ == "__main__":
    app()
