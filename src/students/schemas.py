from pydantic import BaseModel, Field


class StudentStatsResponse(BaseModel):
    full_name: str = Field(..., description="ФИО студента")
    count_twos: int = Field(..., description="Кол-во оценок")