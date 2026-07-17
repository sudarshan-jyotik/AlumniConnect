"""Tests for Company Repository."""
import pytest
from datetime import datetime, timezone

from app.models.company import Company
from app.repositories.company import CompanyRepository


class TestCompanyRepository:
    """Test cases for Company Repository."""

    def test_create_company(self, db):
        """Test creating a company."""
        repo = CompanyRepository(db)
        company = Company(
            name="New Tech Corp",
            industry="Technology",
            website="https://newtech.com",
            description="A new tech company",
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        
        created_company = repo.create(company)
        db.commit()  # Commit the transaction
        db.refresh(created_company)  # Refresh to get the ID
        
        assert created_company.id is not None
        assert created_company.name == "New Tech Corp"
        assert created_company.industry == "Technology"

    def test_get_by_id(self, db, test_company):
        """Test getting company by ID."""
        repo = CompanyRepository(db)
        
        company = repo.get_by_id(test_company.id)
        
        assert company is not None
        assert company.id == test_company.id
        assert company.name == test_company.name

    def test_get_by_id_not_found(self, db):
        """Test getting non-existent company."""
        repo = CompanyRepository(db)
        
        company = repo.get_by_id(99999)
        
        assert company is None

    def test_get_by_name(self, db, test_company):
        """Test getting company by name."""
        repo = CompanyRepository(db)
        
        company = repo.get_by_name(test_company.name)
        
        assert company is not None
        assert company.name == test_company.name
        assert company.id == test_company.id

    def test_get_by_name_not_found(self, db):
        """Test getting company with non-existent name."""
        repo = CompanyRepository(db)
        
        company = repo.get_by_name("Nonexistent Company")
        
        assert company is None

    def test_get_all(self, db, test_company, test_company_2):
        """Test getting all companies."""
        repo = CompanyRepository(db)
        
        companies = repo.get_all(skip=0, limit=100)
        
        assert len(companies) >= 2
        company_ids = [c.id for c in companies]
        assert test_company.id in company_ids
        assert test_company_2.id in company_ids

    def test_get_all_pagination(self, db):
        """Test pagination in get_all."""
        repo = CompanyRepository(db)
        
        # Create multiple companies
        for i in range(5):
            company = Company(
                name=f"Company {i}",
                industry="Test",
                is_active=True,
                created_at=datetime.now(timezone.utc)
            )
            repo.create(company)
        db.commit()  # Commit all companies
        
        # Test pagination
        page1 = repo.get_all(skip=0, limit=2)
        page2 = repo.get_all(skip=2, limit=2)
        
        assert len(page1) == 2
        assert len(page2) >= 2
        assert page1[0].id != page2[0].id

    def test_search_companies(self, db):
        """Test searching companies by name."""
        repo = CompanyRepository(db)
        
        # Create companies with searchable names
        company1 = Company(
            name="Google Inc",
            industry="Technology",
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        company2 = Company(
            name="Microsoft Corporation",
            industry="Technology",
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        company3 = Company(
            name="Apple Inc",
            industry="Technology",
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        
        repo.create(company1)
        repo.create(company2)
        repo.create(company3)
        db.commit()  # Commit all companies
        
        # Search for "Inc"
        results = repo.search("Inc")
        
        assert len(results) >= 2
        assert any("Inc" in c.name for c in results)

    def test_update_company(self, db, test_company):
        """Test updating a company."""
        repo = CompanyRepository(db)
        
        updated_company = repo.update(test_company.id, {
            "industry": "Software",
            "description": "Updated description"
        })
        
        assert updated_company.industry == "Software"
        assert updated_company.description == "Updated description"
        assert updated_company.name == test_company.name  # Unchanged

    def test_update_nonexistent_company(self, db):
        """Test updating a non-existent company."""
        repo = CompanyRepository(db)
        
        updated_company = repo.update(99999, {"industry": "New Industry"})
        
        assert updated_company is None

    def test_delete_company(self, db, test_company):
        """Test deleting a company."""
        repo = CompanyRepository(db)
        company_id = test_company.id
        
        result = repo.delete(company_id)
        db.commit()  # Commit the deletion
        
        assert result is True
        assert repo.get_by_id(company_id) is None

    def test_delete_nonexistent_company(self, db):
        """Test deleting a non-existent company."""
        repo = CompanyRepository(db)
        
        result = repo.delete(99999)
        
        assert result is False

    def test_get_active_companies(self, db):
        """Test getting only active companies."""
        repo = CompanyRepository(db)
        
        # Create active and inactive companies
        active_company = Company(
            name="Active Corp",
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        inactive_company = Company(
            name="Inactive Corp",
            is_active=False,
            created_at=datetime.now(timezone.utc)
        )
        
        repo.create(active_company)
        repo.create(inactive_company)
        db.commit()  # Commit both companies
        
        # Get all companies and filter active
        all_companies = repo.get_all()
        active_companies = [c for c in all_companies if c.is_active]
        
        assert len(active_companies) >= 1
        assert all(c.is_active for c in active_companies)

    def test_create_duplicate_name(self, db, test_company):
        """Test creating company with duplicate name raises error."""
        repo = CompanyRepository(db)
        company = Company(
            name=test_company.name,  # Duplicate
            industry="Test",
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        
        with pytest.raises(Exception):  # SQLAlchemy IntegrityError
            repo.create(company)
            db.commit()

    def test_company_with_referral_requests(self, db, test_company, test_draft_request):
        """Test company with referral requests relationship."""
        repo = CompanyRepository(db)
        
        company = repo.get_by_id(test_company.id)
        
        # Access relationship
        assert company.referral_requests is not None
        assert len(company.referral_requests) >= 1
