from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:

    @staticmethod
    def create_user(db, user: UserCreate):

        existing_email = UserRepository.get_by_email(
            db,
            user.email
        )

        if existing_email:
            raise ValueError("Email already exists.")

        existing_username = UserRepository.get_by_username(
            db,
            user.username
        )

        if existing_username:
            raise ValueError("Username already exists.")

        # Hash password before saving
        # user.password = hash_password(user.password)
        hashed_user = user.model_copy(
            update={
                "password": hash_password(user.password)
            }
        )

        # return UserRepository.create(db, user)
        return UserRepository.create(db, hashed_user)

    @staticmethod
    def get_user(db, user_id: int):

        user = UserRepository.get_by_id(
            db,
            user_id
        )

        if not user:
            raise ValueError("User not found.")

        return user

    @staticmethod
    def get_all_users(db):

        return UserRepository.get_all(db)

    @staticmethod
    def update_user(
        db,
        user_id: int,
        user_data: UserUpdate
    ):

        db_user = UserRepository.get_by_id(
            db,
            user_id
        )

        if not db_user:
            raise ValueError("User not found.")

        return UserRepository.update(
            db,
            db_user,
            user_data
        )

    @staticmethod
    def delete_user(db, user_id: int):

        db_user = UserRepository.get_by_id(
            db,
            user_id
        )

        if not db_user:
            raise ValueError("User not found.")

        UserRepository.delete(
            db,
            db_user
        )

        return {
            "message": "User deleted successfully."
        }