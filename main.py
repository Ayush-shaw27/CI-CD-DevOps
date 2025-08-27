from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.patients import router as patients_router
from api.auth import router as auth_router
from database.seed_data import seed_database
import uvicorn

# Create FastAPI application
app = FastAPI(
    title="Medical Records API",
    description="Secure medical records management system with DevSecOps integration",
    version="1.0.0"
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(patients_router)

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Medical Records API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "medical-records-api"}

@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    seed_database()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
