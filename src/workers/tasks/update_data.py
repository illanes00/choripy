from .celery_app import celery
@celery.task
def update_data():
    # Aquí va tu pipeline ETL
    from src.etl.clean import run as clean_run
    from src.etl.aggregate import run as agg_run
    clean_run(src="data/raw/raw.csv", dst="data/interim/clean.parquet")
    agg_run(src="data/interim/clean.parquet", dst="data/processed/features.parquet")
    return "ETL OK"
