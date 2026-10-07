"""
AlumniConnect - Main Application Entry Point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.database import Base, engine
from app.core.exceptions import AppException
from app.core.rate_limit import limiter
from app.middleware.error_handler import app_exception_handler, general_exception_handler
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.routers import (
    admin,
    alumni,
    auth,
    companies,
    endorsements,
    notifications,
    referral_requests,
    referral_submissions,
    users,
)

# API version prefix
API_PREFIX = "/api/v1"

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Platform connecting students with alumni for job referrals",
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"https://.*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(auth.router, prefix=API_PREFIX, tags=["Authentication"])
app.include_router(users.router, prefix=API_PREFIX, tags=["Users"])
app.include_router(companies.router, prefix=API_PREFIX, tags=["Companies"])
app.include_router(
    referral_requests.router, prefix=API_PREFIX, tags=["Referral Requests"]
)
app.include_router(
    referral_submissions.router, prefix=API_PREFIX, tags=["Referral Submissions"]
)
app.include_router(alumni.router, prefix=API_PREFIX, tags=["Alumni"])
app.include_router(endorsements.router, prefix=API_PREFIX, tags=["Endorsements"])
app.include_router(notifications.router, prefix=API_PREFIX, tags=["Notifications"])
app.include_router(admin.router, prefix=API_PREFIX, tags=["Admin"])


@app.get("/", tags=["Root"])
def root():
    """Root endpoint - API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "message": "Welcome to AlumniConnect - Placement Referral Platform",
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
        "version": settings.APP_VERSION,
    }


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting...")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"🔧 Debug Mode: {settings.DEBUG}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    print(f"👋 {settings.APP_NAME} shutting down...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
