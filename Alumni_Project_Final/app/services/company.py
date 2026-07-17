"""Company service."""
from sqlalchemy.orm import Session
from app.core.exceptions import ConflictException, NotFoundException
from app.models.company import Company
from app.repositories.company import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyUpdate

class CompanyService:
    def __init__(self, repository: CompanyRepository, db: Session):
        self.repository = repository
        self.db = db

    def create_company(self, company_data: CompanyCreate) -> Company:
        """Create a new company."""
        existing = self.repository.get_by_name(company_data.name)
        if existing:
            raise ConflictException("Company already exists")

        new_company = Company(
            name=company_data.name,
            industry=company_data.industry,
            website=str(company_data.website) if company_data.website else None,
            description=company_data.description,
            headquarters=company_data.headquarters,
        )

        self.repository.create(new_company)
        self.db.commit()
        self.db.refresh(new_company)

        return new_company

    def get_company(self, company_id: int) -> Company:
        """Get company by ID."""
        company = self.repository.get_by_id(company_id)
        if not company:
            raise NotFoundException("Company not found")
        return company

    def get_all_companies(self, skip: int = 0, limit: int = 100) -> list[Company]:
        """Get all active companies."""
        return self.repository.get_active(skip, limit)

    def search_companies(self, query: str, skip: int = 0, limit: int = 100) -> list[Company]:
        """Search companies by name."""
        return self.repository.search(query, skip, limit)
    
    def update_company(self, company_id: int, data: dict) -> Company:
        """Update a company."""
        company = self.get_company(company_id)  # Raises NotFoundException if not found
        
        updated_company = self.repository.update(company_id, data)
        self.db.commit()
        self.db.refresh(updated_company)
        
        return updated_company
    
    def delete_company(self, company_id: int) -> None:
        """Delete a company."""
        company = self.get_company(company_id)  # Raises NotFoundException if not found
        
        self.repository.delete(company_id)
        self.db.commit()
