# Використовуємо офіційний Python-образ
FROM python:3.10

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файл залежностей
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install -r requirements.txt

# Копіюємо весь проєкт у контейнер
COPY . /app

# Встановлюємо змінну середовища для Django
ENV PYTHONPATH="/app"

# Відкриваємо порт 8000
EXPOSE 8000

# Запускаємо Gunicorn з правильним шляхом до wsgi.py
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
