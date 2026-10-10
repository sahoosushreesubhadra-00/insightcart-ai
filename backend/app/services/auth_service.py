from sqlalchemy.orm import Session

from app.core.security import (
    verify_password,
    create_access_token,
)
from app.repositories.user_repository import UserRepository


class AuthService:

    @staticmethod
    def login(
        db: Session,
        username: str,
        password: str,
    ):

        user = UserRepository.get_by_username(
            db,
            username
        )

        if not user:
            raise ValueError("Invalid username or password.")

        if not verify_password(
            password,
            user.hashed_password
        ):
            raise ValueError("Invalid username or password.")

        token = create_access_token(
            {
                "sub": str(user.id)
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }