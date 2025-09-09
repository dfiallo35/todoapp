from fastapi import APIRouter
from fastapi import Response
from fastapi import status
from datetime import timedelta

from app.settings import settings
from app.domain.models import TokenResponse
from app.domain.models import User
from app.domain.models import UserSignup
from app.domain.models import UserLogin
from app.presentation.security import get_password_hash
from app.presentation.security import create_access_token
from app.presentation.security import verify_password
from app.application.services import UserCreateService
from app.application.services import UserListService
from app.domain.filters import UserFilter


auth_router = APIRouter(prefix="/auth")


@auth_router.post("/signup", response_model=TokenResponse)
async def signup(user_in: UserSignup, response: Response):
    user_list_service = UserListService()
    user_create_service = UserCreateService()

    users = await user_list_service(UserFilter(username_eq=user_in.username))
    if users:
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise ValueError(f"Username {user_in.username} already exists")

    hashed_password = get_password_hash(user_in.password)
    user = User(
        username=user_in.username,
        hashed_password=hashed_password,
    )
    user = await user_create_service(user)

    token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    response.status_code = status.HTTP_200_OK
    return TokenResponse(access_token=token, token_type="bearer")


@auth_router.post("/login", response_model=TokenResponse)
async def login(user_in: UserLogin, response: Response):
    user_list_service = UserListService()
    users = await user_list_service(UserFilter(username_eq=user_in.username))
    if not users:
        raise ValueError(f"Username {user_in.username} not found")

    user = users[0]
    if not verify_password(user_in.password, user.hashed_password):
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise ValueError("Incorrect username or password")

    token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    response.status_code = status.HTTP_200_OK
    return TokenResponse(access_token=token, token_type="bearer")
