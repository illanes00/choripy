PY := python -m

.PHONY: setup precommit lint test migrate serve serve-all etl figs paper tables

###############################################################################
# 1. Crear venv e instalar dependencias + pre-commit
###############################################################################
setup:
	@python -m venv .venv && . .venv/bin/activate && pip install -r requirements-dev.txt
	pre-commit install

precommit:
	pre-commit install

###############################################################################
# 2. Linter y tests
###############################################################################
lint:         ## black + ruff
	black --check .
	ruff check .

test:
	pytest -q

###############################################################################
# 3. Migraciones Alembic
###############################################################################
migrate:
	alembic upgrade head

###############################################################################
# 4. Levantar servicios sin Docker
###############################################################################
serve:           ## FastAPI hot-reload
	python run.py serve_api

serve-all:       ## Backend + Frontend en paralelo
	python run.py serve_all

###############################################################################
# 5. ETL / Plots / Reportes (igual que antes)
###############################################################################
etl:
	$(PY) src.etl.run

figs:            ## Genera figuras reproducibles
	python -m tools.plots.generate

paper: figs tables
	quarto render docs/report.qmd --to pdf

tables:
	python -m tools.tables.make_tables
