# 🚀 Інструкція із запуску Celery та Celery Beat

Цей документ містить покрокову інструкцію щодо запуску та використання Celery у проєкті.

---

## 📌 1. Встановлення необхідних пакетів

Переконайтеся, що у вас встановлені всі необхідні пакети:

```sh
pip install celery redis django-celery-beat
```

Якщо Redis працює в контейнері, запустіть його:

```sh
docker start redis
```

Якщо контейнер не створений, виконайте:

```sh
docker run -d --name redis -p 6379:6379 redis
```

---

## 📌 2. Налаштування змінних середовища

Перед запуском переконайтеся, що у файлі `.env` вказані правильні параметри для підключення Celery до Redis:

```env
CELERY_BROKER_URL=redis://host.docker.internal:6379/0
CELERY_RESULT_BACKEND=redis://host.docker.internal:6379/0
```

---

## 📌 3. Запуск Celery Worker

Щоб Celery міг виконувати задачі, запустіть Worker у **першому терміналі**:

```sh
celery -A app worker --loglevel=info --pool=solo
```

---

## 📌 4. Запуск Celery Beat

Celery Beat використовується для періодичних задач. Запустіть його у **другому терміналі**:

```sh
celery -A app beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

---

## 📌 5. Перевірка роботи Celery Beat

Щоб переконатися, що Celery Beat передає задачі у Worker, виконайте команду у **третьому терміналі**:

```sh
celery -A app inspect scheduled
```

Якщо все працює правильно, ви маєте бачити заплановані задачі.

---

## 📌 6. Оновлення списку періодичних задач

Щоб очистити старі задачі та додати нові, виконайте **один із варіантів**:

### ВАРІАНТ 1: Окремий скрипт

```sh
python backend/setup_tasks.py
```

### ВАРІАНТ 2: Django management команда

```sh
python manage.py setup_celery_tasks
```

Після цього **перезапустіть Celery Beat**.

---

## 📌 7. Дебаг і перевірка задач

Якщо щось не працює, можна вручну запустити таску у Django shell:

```sh
python manage.py shell
```

Потім виконайте у консолі:

```python
from weather.tasks import send_greeting
send_greeting.delay()
```

Якщо Celery Worker працює, він має обробити цю задачу.

---

## ✅ Висновок

Ця інструкція допоможе швидко запустити Celery та Celery Beat у проєкті, перевірити їхню роботу та оновлювати список періодичних задач. Якщо виникають проблеми, перевіряйте логи Celery Worker і Celery Beat! 🚀

