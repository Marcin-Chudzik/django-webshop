# making sure that the celery will be imported at the projects start.
from .celery import app as celery_app
