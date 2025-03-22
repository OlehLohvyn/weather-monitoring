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

## Docker Components

- `web`: Django backend (port `8000`)
- `db`: SQLite with volume (or PostgreSQL if configured)
- `celery`: handles async tasks (e.g., API calls)
- `celery-beat`: runs scheduled weather updates

---

## How to Run the Project in Docker

### 1. Clone the Repository

```bash
git clone https://github.com/your-name/weather_monitoring_system.git
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



