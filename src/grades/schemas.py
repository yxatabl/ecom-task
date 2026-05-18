from pydantic import BaseModel, Field


class UploadStatusResponse(BaseModel):
    ok: str = Field(default="ok", description="Статус загрузки")
    records_loaded: int = Field(..., description="Кол-во загруженных записей")
    students: int = Field(..., description="Кол-во уникальных студентов")