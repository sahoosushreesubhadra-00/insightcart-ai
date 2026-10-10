from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """
    Common fields shared across multiple user schemas.
    """

    username: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Unique username"
    )

    email: EmailStr


class UserCreate(UserBase):
    """
    Schema used while creating a user.
    """

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Plain text password"
    )


class UserUpdate(BaseModel):
    """
    Schema used while updating a user.
    """

    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    email: EmailStr | None = None

    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=100
    )

    is_active: bool | None = None


class UserResponse(UserBase):
    """
    Schema returned by the API.
    """

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    """
    Schema returned when listing users.
    """

    total: int
    users: list[UserResponse]