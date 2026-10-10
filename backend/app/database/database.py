"""
Database configuration and session management.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


# Create SQLAlchemy Engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)


# Create Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Creates a new database session for each request.

    The session is automatically closed after the request
    completes, whether it succeeds or fails.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()