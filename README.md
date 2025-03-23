# Weather Monitoring System — Docker Setup Guide

This document explains how to run the Weather Monitoring System using Docker.

---

## Requirements Before Starting

Make sure the following tools are installed on your machine:

- Docker
- Docker Compose
- Git
- Python 3.10+ (for local development)

> If you're using Windows, it's recommended to run commands in PowerShell or WSL.

---

## Required Environment Variables

Create a `.env` file in the **root of the repository** (next to `docker-compose.yml`) with the following variables:

```env
# Django
SECRET_KEY=your_secret_key
DJANGO_SETTINGS_MODULE=app.settings

# Weather API
WEATHER_API_KEY=your_api_key
DEFAULT_CITY=Boryspil

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Database (PostgreSQL or other)
DB_HOST=db
DB_NAME=app_db
DB_USER=app_user
DB_PASS=your_password
DB_PORT=5432

# Django superuser (auto-creation)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=adminpassword
```

This file is ignored by Git, so you must create it manually on each machine or CI/CD environment.

---

## Docker Components

- `web`: Django backend (port `8000`)
- `db`: SQLite with volume (or PostgreSQL if configured)
- `celery`: handles async tasks (e.g., API calls)
- `celery-beat`: runs scheduled weather updates

---

## How to Run the Project in Docker

### 1. Clone the Repository

```bash
git clone git@github.com:OlehLohvyn/weather-monitoring.git
cd weather_monitoring_system/backend
```

### 2. Build Docker Images

```bash
docker compose build
```

### 3. Start Services

```bash
docker compose up
```

---

## Testing the System

- Open `http://localhost:8000/admin/` in your browser
- Log in with the superuser credentials
- Check the weather API at: `http://localhost:8000/weather/`

---

## Developer Commands (Local Only)

These commands should be run outside Docker, in your virtual environment.

```bash
# Code linting
.\lint.bat

# Run tests
pytest
```

---

## Project Structure

```
weather_monitoring_system/
├── backend/
│   ├── app/                # Django settings
│   ├── weather/            # Core business logic
│   ├── tests/              # Unit tests
│   ├── Dockerfile          # Docker image definition
│   ├── docker-compose.yml  # Docker services configuration
│   └── manage.py
```

---

## Common Issues

- **"Address already in use"**: Port 8000 is busy — stop the running service or change the port in `docker-compose.yml`
- **Celery won't start**: Check the `.env` file, broker settings, and dependencies
- **Permission denied**: If using WSL, try running with `sudo`

---

## Contact

This project was created to demonstrate Python backend development skills.  
For suggestions or issues, open an issue or contact the author directly.

