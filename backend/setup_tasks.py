import os
import django

# Ініціалізуємо Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

print("🔄 Очищення старих задач та інтервалів...")

# Видаляємо всі старі задачі та інтервали
PeriodicTask.objects.all().delete()
IntervalSchedule.objects.all().delete()

print("✅ Видалено старі задачі!")

# Створюємо інтервал 10 секунд
schedule, created = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.SECONDS,
)

# Створюємо нову задачу
task, created = PeriodicTask.objects.get_or_create(
    interval=schedule,
    name="Повторюване привітання",
    task="weather.tasks.send_greeting",
    defaults={"args": json.dumps([])}
)

if created:
    print("✅ Нова періодична таска створена!")
else:
    print("✅ Таска вже існує!")

print("🚀 Celery Beat оновлений!")
