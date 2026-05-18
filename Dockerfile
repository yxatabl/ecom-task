FROM python:3.13-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS test
COPY . .

FROM base AS production
COPY ./src ./src
COPY ./migrations ./migrations
COPY alembic.ini .