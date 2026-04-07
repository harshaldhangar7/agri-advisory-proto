from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from .db import init_db
from .routers import farmers, advisory, auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agri Advisory Prototype")

# Allow local frontend origin (Vite default)
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(farmers.router)
app.include_router(advisory.router)

@app.on_event("startup")
def on_startup():
    logger.info("Starting Agri Advisory API...")
    init_db()
    logger.info("Database initialized")

@app.get("/health")
def health_check():
    logger.debug("Health check requested")
    return {"status": "ok"}