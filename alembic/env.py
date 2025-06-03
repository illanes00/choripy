# alembic/env.py
from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from alembic import context

# 1. Cargar variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv()

# 2. Importar Base para metadata
from src.db.models import Base

# Alembic Config object
config = context.config

# 3. Sobrescribir sqlalchemy.url desde la env var
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Logging config (igual que antes)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 4. Aquí asignamos la metadata de nuestros modelos
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations en modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations en modo online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
