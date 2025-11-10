from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    title: str = Field(..., description="Название проекта")
    short_description: str = Field(..., description="Краткое описание проекта")
    full_description: str = Field(..., description="Полное описание проекта")


class ProjectCreate(ProjectBase):
    images: List[str] = Field(default_factory=list, description="Список URL изображений проекта")


class ProjectUpdate(ProjectBase):
    images: Optional[List[str]] = Field(
        default=None,
        description="Новый список URL изображений проекта (полностью заменяет предыдущий)",
    )


class ProjectRead(ProjectBase):
    id: int
    images: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

