import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import auth, projects, deployments, users

# Create tables on startup (For production, use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CloudDeploy API",
    description="API Gateway for Cloud Deployment Platform",
    version="1.0.0"
)

# CORS Configuration
origins = ["*"] # Configure this properly for production

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(deployments.router)
app.include_router(users.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "api-gateway"}

@app.get("/", tags=["Info"])
def root():
    return {
        "message": "Welcome to CloudDeploy API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
