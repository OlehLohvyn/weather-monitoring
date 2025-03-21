import json

from django_celery_beat.models import IntervalSchedule, PeriodicTask


def setup_periodic_tasks():
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )

    task, created = PeriodicTask.objects.get_or_create(
        name="Запит погоди щохвилини",
        defaults={
            "interval": schedule,
            "task": "weather.tasks.ask_weather_question",
            "args": json.dumps([]),
            "enabled": True,
        }
    )

    if not created:
        task.enabled = True
        task.save()

    print("✅ Periodic task added or updated!")
