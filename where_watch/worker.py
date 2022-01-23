import asyncio
import os

from celery import Celery

from socket_handler import scrap_sites

worker = Celery(__name__)
worker.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
worker.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")


@worker.task(name="scrap")
def scrap_task(title):
    asyncio.run(scrap_sites(title))