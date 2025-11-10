from typing import Dict, List
from datetime import datetime
from app.models import Lever, LeverCreate, LeverUpdate


# In-memory хранилище для демонстрации
# В реальном проекте здесь будет подключение к БД
class Database:
    def __init__(self):
        self.levers: Dict[int, Lever] = {}
        self._next_id = 1

    def create_lever(self, lever: LeverCreate) -> Lever:
        now = datetime.now()
        new_lever = Lever(
            id=self._next_id,
            name=lever.name,
            description=lever.description,
            position=lever.position,
            is_active=lever.is_active,
            created_at=now,
            updated_at=now
        )
        self.levers[self._next_id] = new_lever
        self._next_id += 1
        return new_lever

    def get_lever(self, lever_id: int) -> Lever | None:
        return self.levers.get(lever_id)

    def get_all_levers(self) -> List[Lever]:
        return list(self.levers.values())

    def update_lever(self, lever_id: int, lever_update: LeverUpdate) -> Lever | None:
        if lever_id not in self.levers:
            return None
        
        existing_lever = self.levers[lever_id]
        update_data = lever_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(existing_lever, field, value)
        
        existing_lever.updated_at = datetime.now()
        return existing_lever

    def delete_lever(self, lever_id: int) -> bool:
        if lever_id in self.levers:
            del self.levers[lever_id]
            return True
        return False


# Глобальный экземпляр базы данных
db = Database()

