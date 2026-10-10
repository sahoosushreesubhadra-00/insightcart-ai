from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:

    @staticmethod
    def create(db: Session, user: UserCreate) -> User:
        """
        Create a new user.
        """

        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=user.password,  # Already hashed in UserService
            is_active=True,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User | None:
        """
        Get a user by ID.
        """

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        """
        Get a user by email.
        """

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def get_by_username(db: Session, username: str) -> User | None:
        """
        Get a user by username.
        """

        return (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

    @staticmethod
    def get_all(db: Session) -> list[User]:
        """
        Get all users.
        """

        return (
            db.query(User)
            .order_by(User.id)
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        db_user: User,
        user: UserUpdate,
    ) -> User:
        """
        Update a user.
        """

        update_data = user.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if key == "password":
                db_user.hashed_password = hash_password(value)
            else:
                setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def delete(db: Session, db_user: User) -> None:
        """
        Delete a user.
        """

        db.delete(db_user)
        db.commit()