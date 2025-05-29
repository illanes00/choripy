from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()
broker = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery = Celery("choripy_demo", broker=broker)
celery.autodiscover_tasks(["src.workers.tasks"])
