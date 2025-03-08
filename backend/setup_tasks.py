from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

print("🔄 Очищення старих задач та інтервалів...")

# Видаляємо всі старі задачі та інтервали
PeriodicTask.objects.all().delete()
IntervalSchedule.objects.all().delete()

print("✅ Видалено старі задачі!")

# Створюємо інтервал 1 година
schedule, created = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.HOURS,
)

# Створюємо нову задачу
task, created = PeriodicTask.objects.get_or_create(
    interval=schedule,
    name="Отримання та збереження погоди",
    task="weather.tasks.fetch_and_store_weather",
    defaults={"args": json.dumps([])}
)

if created:
    print("✅ Нова періодична таска створена!")
else:
    print("✅ Таска вже існує!")

print("🚀 Celery Beat оновлений!")
