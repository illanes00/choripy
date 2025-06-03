#!/usr/bin/env python3
import os
import sys
import subprocess
import venv
import json
import socket
import secrets
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt

# Paths
ROOT = Path(__file__).parent
VENV = ROOT / ".venv"
PY = VENV / "bin" / "python"
PIP = VENV / "bin" / "pip"

console = Console()

def bootstrap():
    # Si ya estamos dentro de la venv, no hacemos nada
    if sys.executable == str(PY):
        return

    console.print(":package:  [cyan]Creando virtualenv…[/]")
    venv.EnvBuilder(with_pip=True).create(VENV)

    console.print(":arrow_down:  [cyan]Instalando dependencias…[/]")
    # pip install requierements, silenciando la salida
    subprocess.run([str(PIP), "install", "--quiet", "-r", "requirements.txt"], check=True)
    subprocess.run([str(PIP), "install", "--quiet", "-r", "requirements-dev.txt"], check=True)

    # Relanzar dentro de la venv
    os.execv(str(PY), [str(PY)] + sys.argv)

def free_port(start: int = 8000) -> int:
    for p in range(start, start + 100):
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", p)) != 0:
                return p
    raise RuntimeError("No hay puertos libres en rango")

def main():
    console.print("[bold green]⚙️  Instalador de ChoriPy[/]\n")

    project = Prompt.ask("Slug del proyecto", default="choripy_demo")
    port    = Prompt.ask("Puerto para la API", default=str(free_port()))
    db_url  = Prompt.ask(
        "DATABASE_URL",
        default=f"postgresql+asyncpg://postgres:postgres@localhost:5432/{project}",
    )
    redis   = Prompt.ask("REDIS_URL", default="redis://localhost:6379/0")
    secret  = secrets.token_hex(16)

    # Generar .env
    env_text = (
        f"DATABASE_URL={db_url}\n"
        f"REDIS_URL={redis}\n"
        f"SECRET_KEY={secret}\n"
    )
    (ROOT / ".env").write_text(env_text)
    console.print("[green]✔[/] .env creado")

    # Generar config/local.yml
    cfg = {"project": {"name": project}, "api": {"port": int(port)}}
    (ROOT / "config" / "local.yml").write_text(json.dumps(cfg, indent=2))
    console.print("[green]✔[/] config/local.yml creado\n")

    console.print(":tada:  [bold green]Instalación completa![/]")
    console.print("Ahora ejecuta  [bold]./run.py up[/]  para levantar todo.")

if __name__ == "__main__":
    bootstrap()
    main()
