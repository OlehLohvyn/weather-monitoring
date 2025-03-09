from celery import shared_task
import datetime

@shared_task
def ask_weather_question():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Яка зараз температура повітря?")
