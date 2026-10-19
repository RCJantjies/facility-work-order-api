from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables when the application starts."""
    create_db_and_tables()
    yield


app = FastAPI(
    title="Facility Work Order Management API",
    description=(
        "REST API for managing facility assets, maintenance work orders, "
        "SLA deadlines, status transitions, and operational metrics."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "name": "Facility Work Order Management API",
        "version": "0.1.0",
        "status": "operational",
    }