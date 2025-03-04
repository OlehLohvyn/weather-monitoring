from celery import shared_task
from datetime import datetime


@shared_task
def send_greeting():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Привіт! Celery працює кожні 10 секунд 🚀")
