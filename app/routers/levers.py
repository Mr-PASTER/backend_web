from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import Lever, LeverCreate, LeverUpdate
from app.database import db

router = APIRouter(prefix="/levers", tags=["levers"])


@router.post("/", response_model=Lever, status_code=status.HTTP_201_CREATED)
async def create_lever(lever: LeverCreate):
    """Создать новый рычаг"""
    # Валидация позиции
    if lever.position < 0.0 or lever.position > 100.0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Позиция рычага должна быть в диапазоне от 0.0 до 100.0"
        )
    return db.create_lever(lever)


@router.get("/", response_model=List[Lever])
async def get_all_levers():
    """Получить все рычаги"""
    return db.get_all_levers()


@router.get("/{lever_id}", response_model=Lever)
async def get_lever(lever_id: int):
    """Получить рычаг по ID"""
    lever = db.get_lever(lever_id)
    if not lever:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Рычаг с ID {lever_id} не найден"
        )
    return lever


@router.put("/{lever_id}", response_model=Lever)
async def update_lever(lever_id: int, lever_update: LeverUpdate):
    """Обновить рычаг"""
    if lever_update.position is not None:
        if lever_update.position < 0.0 or lever_update.position > 100.0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Позиция рычага должна быть в диапазоне от 0.0 до 100.0"
            )
    
    lever = db.update_lever(lever_id, lever_update)
    if not lever:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Рычаг с ID {lever_id} не найден"
        )
    return lever


@router.patch("/{lever_id}/position", response_model=Lever)
async def set_lever_position(lever_id: int, position: float):
    """Установить позицию рычага"""
    if position < 0.0 or position > 100.0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Позиция рычага должна быть в диапазоне от 0.0 до 100.0"
        )
    
    lever_update = LeverUpdate(position=position)
    lever = db.update_lever(lever_id, lever_update)
    if not lever:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Рычаг с ID {lever_id} не найден"
        )
    return lever


@router.patch("/{lever_id}/toggle", response_model=Lever)
async def toggle_lever(lever_id: int):
    """Переключить состояние рычага (активен/неактивен)"""
    lever = db.get_lever(lever_id)
    if not lever:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Рычаг с ID {lever_id} не найден"
        )
    
    lever_update = LeverUpdate(is_active=not lever.is_active)
    return db.update_lever(lever_id, lever_update)


@router.delete("/{lever_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lever(lever_id: int):
    """Удалить рычаг"""
    success = db.delete_lever(lever_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Рычаг с ID {lever_id} не найден"
        )

