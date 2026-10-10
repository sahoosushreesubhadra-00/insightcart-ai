from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    """
    pass


# Import all models here so Alembic can discover them
# from app.models.user import User  # noqa: E402,F401

# __all__ = [
#     "Base",
#     "User",
# ]