from io import BytesIO
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
async def test_upload_grades_valid_csv(setup_database, client_app):
    csv_content = "Дата;Номер группы;ФИО;Оценка\n11.03.2025;101Б;Иванов Иван;4\n12.03.2025;101Б;Петров Петр;5"
    file = BytesIO(csv_content.encode('utf-8'))
    
    response = await client_app.post(
        "/upload-grades",
        files={"file": ("test.csv", file, "text/csv")}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "ok"
    assert data["records_loaded"] == 2
    assert data["students"] == 2


@pytest.mark.asyncio
async def test_upload_grades_invalid_extension(setup_database, client_app):
    file = BytesIO(b"test data")
    
    response = await client_app.post(
        "/upload-grades",
        files={"file": ("test.txt", file, "text/plain")}
    )
    
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_upload_grades_empty_csv(setup_database, client_app):
    csv_content = "Дата;Номер группы;ФИО;Оценка\n"
    file = BytesIO(csv_content.encode('utf-8'))
    
    response = await client_app.post(
        "/upload-grades",
        files={"file": ("test.csv", file, "text/csv")}
    )
    
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_upload_grades_invalid_date(setup_database, client_app):
    csv_content = "Дата;Номер группы;ФИО;Оценка\n32.13.2025;101Б;Иванов Иван;4"
    file = BytesIO(csv_content.encode('utf-8'))
    
    response = await client_app.post(
        "/upload-grades",
        files={"file": ("test.csv", file, "text/csv")}
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_upload_grades_invalid_grade(setup_database, client_app):
    csv_content = "Дата;Номер группы;ФИО;Оценка\n11.03.2025;101Б;Иванов Иван;6"
    file = BytesIO(csv_content.encode('utf-8'))
    
    response = await client_app.post(
        "/upload-grades",
        files={"file": ("test.csv", file, "text/csv")}
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_more_than_three_twos_empty(setup_database, client_app):
    response = await client_app.get("/students/more-than-3-twos")
    
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_less_than_five_twos_empty(setup_database, client_app):
    response = await client_app.get("/students/less-than-5-twos")
    
    assert response.status_code == 200
    assert response.json() == []