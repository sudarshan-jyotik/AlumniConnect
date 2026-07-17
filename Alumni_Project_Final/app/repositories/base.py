"""
Base repository with common CRUD operations.
"""

from typing import Generic, List, Optional, Type, TypeVar
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get record by ID."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records with pagination."""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj: ModelType) -> ModelType:
        """Create a new record. Does NOT commit."""
        self.db.add(obj)
        return obj

    def update(self, id: int, data: dict) -> Optional[ModelType]:
        """Update a record. Does NOT commit."""
        obj = self.get_by_id(id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
        return obj

    def delete(self, id: int) -> bool:
        """Delete a record. Does NOT commit."""
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            return True
        return False
