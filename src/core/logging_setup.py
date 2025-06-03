# src/core/logging_setup.py

import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_filename: str = "logs/app.log"):
    """
    Configura el logger raíz para usar:
    - salida a consola via Rich (si se desea)
    - archivo rotativo con tamaño máximo y backups
    """
    # 1. Asegurar que exista la carpeta logs/
    log_dir = os.path.dirname(log_filename)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # 2. Logger raíz
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 3. Handler rotativo (archivo)
    file_handler = RotatingFileHandler(
        log_filename,
        maxBytes=5_000_000,      # 5 MB
        backupCount=3,           # Mantener hasta 3 archivos de respaldo
        encoding="utf-8"
    )
    file_fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_fmt)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    # 4. (Opcional) RichHandler para consola si tienes rich instalado
    try:
        from rich.logging import RichHandler
        rich_handler = RichHandler(show_time=False, show_path=False)
        rich_fmt = logging.Formatter("%(message)s")
        rich_handler.setFormatter(rich_fmt)
        rich_handler.setLevel(logging.INFO)
        logger.addHandler(rich_handler)
    except ImportError:
        # Si no está rich, simplemente seguimos con el rotativo
        pass

    # 5. Descarta handlers duplicados (ej.: si setup_logging se llama dos veces)
    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.error").handlers.clear()
    logging.getLogger("uvicorn").handlers.clear()
    logging.getLogger("fastapi").handlers.clear()
