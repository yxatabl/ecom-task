# REST-сервис на FastAPI для загрузки и анализа успеваемости студентов

[![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-316192?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-✓-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/yxatabl/ecom-task/tests.yml)](https://github.com/yxatabl/ecom-task/actions)

## Функционал
- Принимает csv-файл и сохраняет данные в PostgreSQL
- Выполняет валидацию данных
- Предоставляет аналитические функции (создан простой механизм для фильтрации по оценкам, по заданию добавлено две конкретные ручки)
- Работает без ORM
- Реализованы тесты (запускаются с помощью GitHub Actions)
- Испозьзует собственный механизм миграций (миграции добавляются в `/src/migrations`)
- Swagger

## Запуск
```bash
git clone https://github.com/yxatabl/ecom-task
cd ecom-task
docker compose up -d
```
Swagger - `http://localhost:8000/docs`

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
