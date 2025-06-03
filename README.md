
# ChoriPy

[![PyPI version](https://img.shields.io/pypi/v/choripy)](https://pypi.org/project/choripy) [![CI](https://github.com/your-org/choripy/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/choripy/actions) [![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

> **ChoriPy** is a **pure-Python** DataOps starter stack: reproducible ETL → FastAPI → background tasks → Quarto reporting → monitoring, all wired up and ready to clone-and-go.

---

## 📋 Table of Contents

- [ChoriPy](#choripy)
  - [📋 Table of Contents](#-table-of-contents)
  - [🔍 Overview](#-overview)
  - [⚙️ Features](#️-features)
  - [🛠 Prerequisites](#-prerequisites)
  - [🚀 Installation](#-installation)
  - [🎉 Quick Start](#-quick-start)
  - [📂 Directory Structure](#-directory-structure)
  - [🔧 Configuration](#-configuration)
  - [🛣 Next Steps](#-next-steps)
  - [🤝 Contributing](#-contributing)
  - [📄 License](#-license)

---

## 🔍 Overview

ChoriPy gives you a **ready-to-use** Python template for data-driven apps:

1. **ETL** with “one step = one output” caching via stamp files.  
2. **FastAPI** REST endpoints + tiny Flask demo.  
3. **Celery** workers (broker = Redis) & optional Flower UI.  
4. **Quarto** reports with built-in bibliography support.  
5. **Rich/Typer** CLI (`run.py init`, `run.py up`, `run.py report`).  
6. **Monitoring** via `/metrics` (Prometheus) and `/monitor` HTML.  
7. **Dev tooling**: pre-commit, Black, Ruff, Flake8, isort, pytest, coverage.  
8. **SCSS pipeline** using Python’s `libsass`, no Node.js required.  
9. **Configs** managed by Hydra + `.env` + `.envrc`.  

Clone, type two commands, and you’ll have a full ETL→API→report→monitor flow.

---

## ⚙️ Features

- **ETL**: `src/etl/clean.py` & `aggregate.py`, stamp-file caching in `Makefile`.  
- **API**: FastAPI endpoints (`/`, `/monitor`, `/metrics`) + Swagger UI.  
- **Dashboard**: Jinja2 templates in `templates/`, CSS in `static/css/`.  
- **Background Tasks**: Celery tasks in `src/workers/tasks/`.  
- **Monitoring**:  
  - `/metrics` for Prometheus  
  - `/monitor` HTML status page  
  - *Optional* Flower UI: `celery -A src.workers.celery_app flower --port 5555`  
- **Reporting**: Quarto QMDs in `docs/` → HTML/PDF → hidden in `.quarto_output/`.  
- **CLI**: `run.py init`, `run.py up`, `run.py serve-api`, `run.py report`, `run.py open-docs`.  
- **Config**: Hydra YAML + environment variables.  
- **Dev-ops**: GitHub Actions (CI), coverage, code style.  

---

## 🛠 Prerequisites

- **Python ≥ 3.10**  
- **Redis** & **PostgreSQL** installed locally (e.g. `apt install redis-server postgresql`)  
- **Quarto CLI** (for docs): [install guide](https://quarto.org/docs/get-started/)  
- **Make**  
- *(optional)* **Flower** (`pip install flower`) for task UI  

---

## 🚀 Installation

```bash
git clone https://github.com/your-org/choripy.git
cd choripy

# 1. Copy env template & configure
cp .env.example .env
#    edit DATABASE_URL, REDIS_URL, SECRET_KEY in .env

# 2. Bootstrap Python env, install deps, compile SCSS
./run.py init

# 3. Ensure Redis & Postgres are running, then start the API
./run.py up
````

---

## 🎉 Quick Start

* **API docs**:      [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Health page**:   [http://127.0.0.1:8000/monitor](http://127.0.0.1:8000/monitor)
* **Prom metrics**:  [http://127.0.0.1:8000/metrics](http://127.0.0.1:8000/metrics)
* **Flower UI** (opt): `http://127.0.0.1:5555`
* **Quarto report**:

  ```bash
  run.py report       # renders docs/*.qmd → .quarto_output/
  open .quarto_output/index.html
  ```

Run the demo ETL and plots:

```bash
make etl             # raw → interim → processed
make figs            # plots → reports/figures
```

---

## 📂 Directory Structure

```text
.
├── .env.example          ← template env vars
├── Makefile              ← etl, figs, paper, lint, test
├── run.py                ← CLI: init, up, serve-api, report, open-docs
├── config/               ← Hydra & logging configs
├── src/
│   ├── api/              ← FastAPI & Flask demo
│   ├── etl/              ← clean.py & aggregate.py
│   ├── workers/          ← celery_app + tasks/
│   ├── db/               ← models + migrations/
│   └── viz/              ← plot helpers
├── static/               ← CSS/SCSS, JS, images
├── templates/            ← Jinja2 templates
├── docs/                 ← Quarto QMDs & setup guide
├── .quarto_output/       ← Quarto-generated HTML/PDF (hidden)
├── reports/              ← generated figures & tables
├── references/           ← bibliography.bib
├── tests/                ← pytest tests
├── tools/                ← helper scripts
└── .github/              ← CI workflows
```

> Folders like `src/analysis/`, `tools/tables/`, and `alembic/` are scaffolds—drop in your own code.

---

## 🔧 Configuration

* **Env vars**: `.env` (see `.env.example`)
* **Hydra**: `config/default.yml` + `config/conf/hydra/config.yaml`
* **Logging**: `config/logging.yml` uses Rich + rotating files
* **SCSS**: edit `static/css/_variables.scss` to customize Bootstrap

---

## 🛣 Next Steps

1. Implement your ETL logic in `src/etl/…`.
2. Add Celery tasks under `src/workers/tasks/`.
3. Write DB migrations in `alembic/versions/`.
4. Customize Jinja templates & JS in `static/`.
5. Add more tests in `tests/`.
6. Publish to PyPI (`choripy`) and enable GitHub Pages for docs.

---

## 🤝 Contributing

Please see [CODE\_OF\_CONDUCT.md](CODE_OF_CONDUCT.md) and [CONTRIBUTING.md](CONTRIBUTING.md) before submitting issues or PRs.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).


