"""Company repository."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.company import Company
from app.repositories.base import BaseRepository

class CompanyRepository(BaseRepository[Company]):
    def __init__(self, db: Session):
        super().__init__(Company, db)

    def get_by_name(self, name: str) -> Optional[Company]:
        """Get company by name."""
        return self.db.query(Company).filter(Company.name == name).first()

    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Company]:
        """Search companies by name."""
        search = f"%{query}%"
        return self.db.query(Company).filter(Company.name.ilike(search)).offset(skip).limit(limit).all()

    def get_active(self, skip: int = 0, limit: int = 100) -> List[Company]:
        """Get active companies."""
        return self.db.query(Company).filter(Company.is_active == True).offset(skip).limit(limit).all()
