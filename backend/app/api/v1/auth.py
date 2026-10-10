# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.database.database import get_db
# from app.schemas.auth import (
#     LoginRequest,
#     Token,
# )
# from app.services.auth_service import AuthService

# router = APIRouter(
#     prefix="/auth",
#     tags=["Authentication"]
# )


# @router.post(
#     "/login",
#     response_model=Token
# )
# def login(
#     login_data: LoginRequest,
#     db: Session = Depends(get_db),
# ):
#     try:
#         return AuthService.login(
#             db,
#             login_data.username,
#             login_data.password,
#         )

#     except ValueError as e:
#         raise HTTPException(
#             status_code=401,
#             detail=str(e)
#         )






from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.auth import Token
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        return AuthService.login(
            db,
            form_data.username,
            form_data.password,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )