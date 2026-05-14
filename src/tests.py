import pytest
from src.commons.postgres import database
from src.commons import migrate
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.fixture()
async def setup_database():
    await database.connect()
    
    async with database.pool.acquire() as conn:
        await conn.execute("CREATE SCHEMA IF NOT EXISTS public")
    
    await migrate.apply_pending_migrations()

    yield

    async with database.pool.acquire() as conn:
        await conn.execute("DROP SCHEMA IF EXISTS public CASCADE")
    
    await database.disconnect()

@pytest.fixture
async def client_app():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_upload_csv(setup_database, client_app):
    response = await client_app.post("/upload-grades")
    assert response.status_code == 200