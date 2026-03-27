from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging
from contextlib import asynccontextmanager

from config.settings import settings
from src.routes import router

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    logger.info("Starting Cybersecurity & Fraud Detection System")
    yield
    logger.info("Shutting down Cybersecurity & Fraud Detection System")


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Real-time cybersecurity and fraud detection system",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])

# Include routers
app.include_router(router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "running",
        "docs_url": "/docs",
        "features": {
            "anomaly_detection": settings.ENABLE_ANOMALY_DETECTION,
            "phishing_detection": settings.ENABLE_PHISHING_DETECTION,
            "fraud_detection": settings.ENABLE_FRAUD_DETECTION,
            "behavioral_analysis": settings.ENABLE_BEHAVIORAL_ANALYSIS,
        },
    }


@app.get("/api/v1/info")
async def api_info():
    """Get API information."""
    return {
        "api_title": settings.API_TITLE,
        "api_version": settings.API_VERSION,
        "endpoints": {
            "health": "/api/v1/health",
            "analyze_transaction": "/api/v1/transactions/analyze",
            "detect_phishing": "/api/v1/phishing/detect",
            "analyze_behavior": "/api/v1/behavior/analyze",
            "models_status": "/api/v1/models/status",
            "risk_summary": "/api/v1/alerts/risk-summary",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host=settings.API_HOST, port=settings.API_PORT, debug=settings.DEBUG
    )

{
  "framework": "vite",
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": { "distDir": "dist" }
    }
  ],
  "routes": [{ "src": "/(.*)", "dest": "/index.html" }]
}
