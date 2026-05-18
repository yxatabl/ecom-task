# REST-сервис на FastAPI для загрузки и анализа успеваемости студентов

[![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-316192?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-✓-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/yxatabl/ecom-task/tests.yml)](https://github.com/yxatabl/ecom-task/actions)

## Функционал
- Принимает csv-файл и сохраняет данные в PostgreSQL
- Валидация данных
- Предоставляет аналитические функции (создан простой механизм для фильтрации по оценкам, по заданию добавлено две конкретные ручки)
- Работает без ORM
- Реализованы тесты (запускаются с помощью GitHub Actions + доступен ручной запуск на тестовой бд)
- Для миграций используется alembic
- Swagger

## Запуск

### Запуск через докер
```bash
git clone https://github.com/yxatabl/ecom-task
cd ecom-task
docker compose up -d
```
Swagger - `http://localhost:8000/docs`

### Запуск локально
```bash
git clone https://github.com/yxatabl/ecom-task
cd ecom-task
uvicorn src.main:app --host 0.0.0.0 --port 8000
```
Важно: нужно активировать виртуальное окружение, поднять базу данных (и добавить строку для подключения в пременную окружения DB_URL в формате postgresql://<user>:<password>@address:port/<db_name>) и установить все зависимости из requirements.txt!

## Запуск тестов
### Запуск через докер
```bash
git clone https://github.com/yxatabl/ecom-task
cd ecom-task
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

### Запуск локально
```bash
git clone https://github.com/yxatabl/ecom-task
cd ecom-task
pytest -v
```
Важно: нужно активировать виртуальное окружение, поднять базу данных (и добавить строку для подключения в пременную окружения DB_URL в формате postgresql://<user>:<password>@address:port/<db_name>) и установить все зависимости из requirements.txt!


## Схема БД
```sql
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    fullname TEXT NOT NULL,
    "group" TEXT NOT NULL,
    CONSTRAINT uq_name_group UNIQUE (fullname, "group")
);

CREATE TABLE IF NOT EXISTS grades (
    id SERIAL PRIMARY KEY,
    student_id INTEGER,
    "date" DATE,
    grade INTEGER NOT NULL,

    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);
```
