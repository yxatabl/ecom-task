from httpx import AsyncClient


async def test_upload_csv_endpoint(client: AsyncClient):
    csv_content = (
        "Дата;Номер группы;ФИО;Оценка\n"
        "11.03.2025;101Б;Курочкин Антон Владимирович;4\n"
        "18.09.2024;102Б;Москвичев Андрей;3\n"
        "26.09.2024;103М;Фомин Глеб Александрович;4\n"
        "20.05.2025;103М;Леонова Виктория;5\n"
        "01.02.2025;103М;Третьяков Максим;2"
    )

    files = {
        "file": ("journal.csv", csv_content, "text/csv")
    }

    response = await client.post("/upload-grades", files=files)

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "ok"
    assert data["records_loaded"] == 5
    assert data["students"] == 5

async def test_upload_invalid_file_extension(client: AsyncClient):
    files = {"file": ("document.txt", "text", "text/plain")}
    response = await client.post("/upload-grades", files=files)

    assert response.status_code == 400
    assert response.json()["detail"] == "Разрешены только csv файлы"