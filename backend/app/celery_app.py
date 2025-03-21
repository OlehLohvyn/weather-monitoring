import os

from celery import Celery

# Вказуємо Django settings як конфігурацію Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

# Створюємо Celery додаток
app = Celery("app")

# Завантажуємо налаштування з Django settings (ті, що починаються з CELERY_)
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматично шукає та реєструє таски в усіх встановлених додатках Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
