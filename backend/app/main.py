from fastapi import FastAPI
from sqlalchemy import text

import app.models
from app.api.v1.users import router as user_router
from app.api.v1.auth import router as auth_router
from app.api.v1.customers import router as customer_router
from app.api.v1.purchases import router as purchase_router
from app.api.v1.predictions import router as prediction_router

from app.database.database import engine

app = FastAPI(
    title="InsightCart AI",
    description="Customer Purchase Prediction & Recommendation System",
    version="1.0.0",
)

# Register API Routes
app.include_router(
    user_router,
    prefix="/api/v1"
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    customer_router,
    prefix="/api/v1"
)

app.include_router(
    purchase_router,
    prefix="/api/v1"
)

app.include_router(prediction_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Welcome to InsightCart AI Backend"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/db-check")
def db_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "status": "success",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }