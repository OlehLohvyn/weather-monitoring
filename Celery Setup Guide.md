# 🚀 Інструкція із запуску Celery 

## **4️⃣ Перезапускаємо проект**
Щоб зміни набули сили, виконай:
```bash
docker-compose down -v
docker-compose up -d --build
```
✅ **Тепер Celery Beat повністю вимкнено, але Celery Worker продовжує працювати!**  

---

## **5️⃣ Перевіряємо, чи Celery все ще працює**
📌 **Запускаємо Django shell і тестуємо Celery вручну:**
```bash
docker-compose exec web-app python manage.py shell
```
```python
from weather.tasks import ask_weather_question
ask_weather_question.delay()
```
✅ **Якщо Celery працює, ти побачиш в `docker-compose logs -f celery-worker`:**
```
[2025-03-09 03:40:00] Яка зараз температура повітря?
```

ює, але без автоматичних тасок. Якщо потрібно – можна налаштувати `crontab` або API для виклику тасок!**