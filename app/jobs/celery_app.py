from celery import Celery
from celery.schedules import crontab

from app.config import settings as s
from app.jobs.tasks import do_something

celery = Celery("schedule", broker=s.REDIS_URL)
celery.conf.beat_schedule = {
    "some_scheduled_task": {
        "task": "app.jobs.celery_app.some_celery_task",
        "schedule": crontab(minute="*/15"),
    },
}


@celery.task
def some_celery_task() -> None:
    do_something()
    return None
