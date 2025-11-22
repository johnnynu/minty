"""FastAPI application entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import accounts, transactions, categories, budget

# Create FastAPI
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Envelope budgeting application API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.env == "development" else [""],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(accounts.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(budget.router, prefix="/api")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Minty API is running",
        "version": "0.1.0",
        "environment": settings.env
    }


@app.get("/health")
async def health_check():
    """Health check for monitoring"""
    return {"status": "healthy"}
