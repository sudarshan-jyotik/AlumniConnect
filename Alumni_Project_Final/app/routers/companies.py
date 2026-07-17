"""Companies endpoints."""
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.dependencies.roles import require_admin
from app.models.user import User
from app.repositories.company import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyOut, CompanyUpdate
from app.schemas.response import ApiResponse
from app.services.company import CompanyService

router = APIRouter(prefix="/companies")


def get_service(db: Session = Depends(get_db)) -> CompanyService:
    """Get company service."""
    repository = CompanyRepository(db)
    return CompanyService(repository, db)


@router.get("/", response_model=ApiResponse[list[CompanyOut]])
@limiter.limit("60/minute")
def get_companies(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    service: CompanyService = Depends(get_service),
):
    """Get all companies."""
    companies = service.get_all_companies(skip, limit)
    return ApiResponse(
        message="Companies fetched successfully",
        data=companies,
    )


@router.get("/search", response_model=ApiResponse[list[CompanyOut]])
@limiter.limit("60/minute")
def search_companies(
    request: Request,
    q: str,
    skip: int = 0,
    limit: int = 100,
    service: CompanyService = Depends(get_service),
):
    """Search companies by name."""
    companies = service.search_companies(q, skip, limit)
    return ApiResponse(
        message="Companies found",
        data=companies,
    )


@router.get("/{company_id}", response_model=ApiResponse[CompanyOut])
@limiter.limit("60/minute")
def get_company(
    request: Request,
    company_id: int,
    service: CompanyService = Depends(get_service),
):
    """Get a specific company."""
    company = service.get_company(company_id)
    return ApiResponse(
        message="Company fetched successfully",
        data=company,
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[CompanyOut])
@limiter.limit("5/minute")
def create_company(
    request: Request,
    company: CompanyCreate,
    current_user: User = Depends(require_admin),
    service: CompanyService = Depends(get_service),
):
    """Create a new company (admin only)."""
    created_company = service.create_company(company)
    return ApiResponse(
        message="Company created successfully",
        data=created_company,
    )


@router.put("/{company_id}", response_model=ApiResponse[CompanyOut])
@limiter.limit("10/minute")
def update_company(
    request: Request,
    company_id: int,
    company_data: CompanyUpdate,
    current_user: User = Depends(require_admin),
    service: CompanyService = Depends(get_service),
):
    """Update a company (admin only)."""
    updated_company = service.update_company(company_id, company_data.model_dump(exclude_unset=True))
    return ApiResponse(
        message="Company updated successfully",
        data=updated_company,
    )


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
def delete_company(
    request: Request,
    company_id: int,
    current_user: User = Depends(require_admin),
    service: CompanyService = Depends(get_service),
):
    """Delete a company (admin only)."""
    service.delete_company(company_id)
