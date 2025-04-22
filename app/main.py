from fastapi import FastAPI
from .routes import router
from .database import engine
from .models import Base

app = FastAPI(title="Task Management System")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include API routes
app.include_router(router)


