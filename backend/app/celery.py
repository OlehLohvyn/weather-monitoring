import os
from celery import Celery

# Встановлюємо змінну середовища для Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

# Завантажуємо налаштування з Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматично шукаємо таски у всіх додатках
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
