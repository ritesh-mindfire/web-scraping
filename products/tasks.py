import time
from celery import shared_task
# from demoapp.models import Widget


@shared_task
def test_concurrency(num):
    print(num)
    time.sleep(60)

@shared_task
def add(x, y):
    return x + y

