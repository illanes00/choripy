PY := python -m

setup:
	@python -m venv .venv && . .venv/bin/activate && pip install -r requirements-dev.txt
precommit:
	pre-commit install
lint: ## black + ruff
	black --check .
	ruff check .
test:
	pytest -q
run-api:
	uvicorn src.api.main:app --reload
etl:
	$(PY) src.etl.run
docs:
	quarto render docs/ --to html

setup:           ## crea venv e instala deps + pre-commit
	python -m pip install -r requirements-dev.txt
	pre-commit install

etl:             ## ejemplo dummy
	python -m src.etl.run

lint:            ## black + ruff
	black --check .
	ruff check .

test:
	pytest -q

serve:           ## FastAPI hot-reload
	./run.py serve-api

# data pipeline reproducible
data/raw/.stamp:
	curl -L -o data/raw/raw.csv https://ejemplo/dataset.csv
	touch $@

data/interim/.stamp: data/raw/.stamp
	python -m src.etl.clean --src data/raw/raw.csv --dst data/interim/clean.parquet
	touch $@

data/processed/.stamp: data/interim/.stamp
	python -m src.etl.aggregate --src data/interim/clean.parquet --dst data/processed/features.parquet
	touch $@

etl: data/processed/.stamp   ## orquesta todo

figs: ## genera figuras reproducibles
	python -m tools.plots.generate

paper: figs tables
	quarto render docs/report.qmd --to pdf

tables:
	python -m tools.tables.make_tables
