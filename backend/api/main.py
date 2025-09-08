import logging
import os
from datetime import datetime

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.auth import get_current_user
from backend.api.config import settings

# Import routers
from backend.api.routers import (
    applications,
    auth,
    companies,
    job_deduplication,
    job_sources,
    jobs,
    resumes,
    search,
    skill_banks,
    stats,
    timeline,
    users,
)

# Setup logging with both file and console handlers
# Create logs directory if it doesn't exist
logs_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs"
)
os.makedirs(logs_dir, exist_ok=True)

# Create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create file handler for all levels
file_handler = logging.FileHandler(
    os.path.join(logs_dir, f"{datetime.now().strftime('%Y%m%d')}-backend.log")
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Create console handler for INFO and above
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Configure root logger
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])

logger = logging.getLogger(__name__)

# Log authentication setting for debugging
logger.info(
    f"REQUIRE_AUTHENTICATION setting: {getattr(settings, 'REQUIRE_AUTHENTICATION', 'Not found')}"
)

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


# Add custom middleware for logging
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


# Include routers
app.include_router(jobs.router)
app.include_router(users.router)
app.include_router(companies.router)
app.include_router(applications.router)
app.include_router(resumes.router)
app.include_router(skill_banks.router)
app.include_router(auth.router)
app.include_router(timeline.router)
app.include_router(job_sources.router)
app.include_router(search.router)
app.include_router(job_deduplication.router)
app.include_router(stats.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the JobPilot API"}


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Test endpoint to check authentication setting
@app.get("/test-auth-setting")
async def test_auth_setting():
    from backend.api.config import settings

    return {
        "REQUIRE_AUTHENTICATION": getattr(
            settings, "REQUIRE_AUTHENTICATION", "Not found"
        ),
        "all_settings": settings.dict(),
    }


# Test endpoint to validate a token
@app.get("/test-token")
async def test_token(current_user=Depends(get_current_user)):
    return {"message": "Token is valid", "user_id": current_user}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
