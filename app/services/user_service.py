from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import User
from ..schemas import UserCreate, UserLogin
from ..utils.security import (
    hash_password,
    verify_password,
    create_access_token
)
from ..repositories.user_repository import (
    get_user_by_email,
    create_user
)


def register_user(db: Session, user_data: UserCreate):
    existing_user = get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        user_data.password
    )

    new_user = User(
        email=user_data.email,
        password_hash=hashed_password
    )

    return create_user(db, new_user)

def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    user = get_user_by_email(db, email)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }