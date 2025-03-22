# 🚀 Weather Monitoring System — Docker Setup Guide

Цей документ допоможе запустити систему моніторингу погоди за допомогою Docker.

---

## 📦 Вимоги перед запуском

Перед запуском переконайся, що на твоїй машині встановлено:

-

> ⚠️ Якщо використовуєш Windows, рекомендовано запускати в PowerShell або WSL

---

## 🧱 Docker-компоненти

- `web`: Django-бекенд (порт `8000`)
- `db`: SQLite/volume (або PostgreSQL, якщо потрібно)
- `celery`: для асинхронних задач (обробка API-запитів)
- `celery-beat`: періодичне оновлення погоди

---

## ⚙️ Запуск у Docker

### 1. Клонувати репозиторій:

```bash
git clone https://github.com/your-name/weather_monitoring_system.git
cd weather_monitoring_system/backend
```

### 2. Побудувати образи

```bash
docker compose build
```

### 3. Запустити сервіс

```bash
docker compose up
```

## 🧪 Перевірка

- Перейди в браузері на `http://localhost:8000/admin/`
- Увійди з суперкористувачем
- Перевір доступність API: `http://localhost:8000/weather/`

---

## 🛠 Команди розробника

### Перевірка коду (тільки локально, не в Docker):

```bash
# лінтинг
.\lint.bat

# юніт-тести
pytest
```

---

## 📁 Структура проекту

```
weather_monitoring_system/
├── backend/
│   ├── app/                # Django settings
│   ├── weather/            # Основна логіка додатку
│   ├── tests/              # Юніт-тести
│   ├── Dockerfile          # Docker-образ
│   ├── docker-compose.yml  # Сервіси
│   └── manage.py
```

---

## ❓ Поширені проблеми

- **"Address already in use"**: порт 8000 вже зайнятий — зупини процес або зміни порт у `docker-compose.yml`
- **Celery не запускається**: перевір `.env`, налаштування брокера та залежності
- **Немає прав**: якщо WSL — запускай команду з `sudo`

---

## ✉️ Зв'язок

Проєкт створено для демонстрації навичок Python-розробника. Усі пропозиції чи питання — в issues або напряму 🙂

