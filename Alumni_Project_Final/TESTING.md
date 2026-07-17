# Testing Documentation

## Test Coverage

This project includes comprehensive test coverage across all layers:

- **Repositories**: Complete CRUD operations and query methods
- **Services**: Business logic and error handling
- **Endpoints**: API integration tests with authentication
- **Utilities**: Helper functions and normalization
- **Dependencies**: Authentication and authorization

**Target Coverage**: 80-85%

## Test Structure

```
tests/
├── conftest.py                  # Shared fixtures and test configuration
├── pytest.ini                   # Pytest configuration
├── unit/                        # Unit tests
│   ├── test_repositories/       # Repository layer tests
│   │   ├── test_user_repository.py
│   │   ├── test_company_repository.py
│   │   └── test_referral_request_repository.py
│   ├── test_services/           # Service layer tests
│   │   ├── test_auth_service.py
│   │   └── test_referral_request_service.py
│   ├── test_utils/              # Utility function tests
│   │   ├── test_normalize_enums.py
│   │   └── test_security.py
│   └── test_dependencies/       # Dependency tests
│       └── test_auth_dependencies.py
└── integration/                 # Integration tests
    ├── test_auth_endpoints.py
    ├── test_referral_request_endpoints.py
    └── test_company_endpoints.py
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run With Coverage Report
```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

### Run Specific Test Categories

**Unit Tests Only:**
```bash
pytest tests/unit/
```

**Integration Tests Only:**
```bash
pytest tests/integration/
```

**Specific Test File:**
```bash
pytest tests/unit/test_repositories/test_user_repository.py
```

**Specific Test Class:**
```bash
pytest tests/unit/test_services/test_auth_service.py::TestAuthService
```

**Specific Test Function:**
```bash
pytest tests/unit/test_services/test_auth_service.py::TestAuthService::test_register_new_user
```

### Run Tests by Markers

```bash
# Authentication tests
pytest -m auth

# Repository tests
pytest -m repositories

# Service tests
pytest -m services

# Integration tests
pytest -m integration
```

### Parallel Test Execution

For faster test runs, install pytest-xdist and run:
```bash
pip install pytest-xdist
pytest -n auto
```

## Coverage Report

After running tests with coverage, open the HTML report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Test Fixtures

### User Fixtures
- `test_student` - Active student user
- `test_alumni` - Active alumni user
- `test_admin` - Admin user
- `test_pending_user` - Pending verification user

### Authentication Fixtures
- `student_token` - JWT token for student
- `alumni_token` - JWT token for alumni
- `admin_token` - JWT token for admin
- `auth_headers_student` - Authorization headers for student
- `auth_headers_alumni` - Authorization headers for alumni
- `auth_headers_admin` - Authorization headers for admin

### Data Fixtures
- `test_company` - Test company
- `test_company_2` - Second test company
- `test_alumni_profile` - Alumni profile with company
- `test_draft_request` - Draft referral request
- `test_pending_request` - Pending referral request
- `test_approved_request` - Approved referral request
- `test_submission` - Referral submission
- `test_approved_submission` - Approved submission
- `test_endorsement` - Endorsement on request

### Database Fixtures
- `db` - Fresh database session for each test
- `client` - TestClient with database override

## Writing New Tests

### Example Unit Test

```python
"""Tests for MyService."""
import pytest

from app.services.my_service import MyService

class TestMyService:
    """Test cases for MyService."""

    @pytest.fixture
    def my_service(self, db):
        """Create service instance."""
        return MyService(db)

    def test_my_function(self, my_service):
        """Test my function does something."""
        result = my_service.my_function()
        
        assert result is not None
        assert result.value == "expected"
```

### Example Integration Test

```python
"""Tests for my endpoints."""
import pytest

class TestMyEndpoints:
    """Test cases for my API endpoints."""

    def test_get_endpoint(self, client, auth_headers_student):
        """Test GET endpoint."""
        response = client.get(
            "/api/v1/my-endpoint/",
            headers=auth_headers_student
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
```

## Testing Best Practices

1. **Test Isolation**: Each test should be independent
2. **Clear Names**: Test names should describe what they test
3. **Arrange-Act-Assert**: Follow AAA pattern
4. **One Assertion Focus**: Each test should have a clear focus
5. **Use Fixtures**: Reuse test data through fixtures
6. **Mock External Dependencies**: Don't make real API calls
7. **Test Edge Cases**: Include error conditions
8. **Keep Tests Fast**: Unit tests should run quickly

## Continuous Integration

Tests run automatically on:
- Pull requests
- Commits to main branch
- Scheduled nightly builds

CI Configuration: `.github/workflows/tests.yml`

## Test Coverage Thresholds

Minimum coverage requirements by module:
- Repositories: 90%
- Services: 85%
- Routers/Endpoints: 80%
- Models: 70%
- Utilities: 90%
- Overall: 80%

## Troubleshooting

### Tests Hanging
- Check for database connections not being closed
- Look for infinite loops
- Use `pytest --timeout=60` to set a timeout

### Database Errors
- Ensure test database is clean
- Check migration status
- Verify fixture dependencies

### Import Errors
- Verify PYTHONPATH includes project root
- Check for circular imports
- Ensure all `__init__.py` files exist

### Fixture Not Found
- Check fixture is defined in conftest.py
- Verify fixture scope (function/class/module/session)
- Check for typos in fixture names

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)

## Test Maintenance

- Review and update tests when changing business logic
- Keep test data fixtures up to date
- Remove obsolete tests
- Refactor duplicated test code
- Update expected values when API responses change

## Contact

For questions about testing:
- Review existing tests for examples
- Check documentation
- Ask in team chat
