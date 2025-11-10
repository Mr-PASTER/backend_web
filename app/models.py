from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LeverBase(BaseModel):
    name: str
    description: Optional[str] = None
    position: float = 0.0  # Позиция рычага (0.0 - 100.0)
    is_active: bool = True


class LeverCreate(LeverBase):
    pass


class LeverUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    position: Optional[float] = None
    is_active: Optional[bool] = None


class Lever(LeverBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

