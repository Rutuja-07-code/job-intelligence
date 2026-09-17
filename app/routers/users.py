from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from ..services.user_service import (
    register_user,
    authenticate_user
)

from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user(db, user_data)

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return authenticate_user(
        db,
        form_data.username,
        form_data.password
    )