import os

import pytest

from httpx import ASGITransport, AsyncClient

if not os.getenv("DB_URL") or "localhost" in os.getenv("DB_URL", ""):
    TEST_DB_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/grades_test"
    os.environ["DB_URL"] = TEST_DB_URL.replace("postgresql+asyncpg://", "postgresql://")
else:
    os.environ["DB_URL"] = os.getenv("DB_URL").replace("postgresql+asyncpg://", "postgresql://")

from src.commons.postgres import database
from src.main import app

@pytest.fixture(scope="function", autouse=True)
async def setup_test_database():
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture(scope="function", autouse=True)
async def clean_database(setup_test_database):
    yield
    
    async with database.connection() as conn:
        await conn.execute("TRUNCATE TABLE grades, students RESTART IDENTITY CASCADE;")


@pytest.fixture(scope="function")
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac