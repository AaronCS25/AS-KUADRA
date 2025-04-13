from fastapi import HTTPException, status

from .models import *
from .schemas import *
from .repositories import (create_user as repository_create_user)
from .repositories import (get_user as repository_get_user)

def signup(user_schema: SignupRequest) -> SignupResponse:
    """Register a new user."""
    user: User = User(**user_schema.model_dump())
    if repository_get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    repository_create_user(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User creation failed",
        )
    return SignupResponse.model_validate(user)

def login(user_schema: LoginRequest) -> LoginResponse:
    """Login a user."""
    user: User | None = repository_get_user(user_schema.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    return LoginResponse.model_validate(user)