import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.config import settings

# Import routers
from backend.api.routers import (
    applications,
    auth,
    companies,
    jobs,
    resumes,
    skill_banks,
    users,
    timeline,
    job_sources,
    search,
    job_deduplication,
    stats,
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
