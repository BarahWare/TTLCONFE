from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import User
from app.modules.auth.schemas import RegisterRequest
from app.shared.exceptions import Conflict, Unauthorized
from app.shared.utils import (
    create_access_token as _create_access_token,
    create_refresh_token as _create_refresh_token,
    hash_password,
    verify_password,
)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def create_access_token(user_id: int) -> str:
        return _create_access_token(user_id)

    @staticmethod
    def create_refresh_token(user_id: int) -> str:
        return _create_refresh_token(user_id)

    async def register(self, data: RegisterRequest) -> User:
        result = await self.db.execute(select(User).where(User.email == data.email))
        if result.scalar_one_or_none():
            raise Conflict("Email already registered")

        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            full_name=data.full_name,
            phone=data.phone,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def login(self, email: str, password: str) -> tuple[str, str, User]:
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.password_hash):
            raise Unauthorized("Invalid email or password")
        if not user.is_active:
            raise Unauthorized("User is inactive")

        access_token = _create_access_token(user.id)
        refresh_token = _create_refresh_token(user.id)
        return access_token, refresh_token, user

    async def refresh_token(self, token: str) -> tuple[str, str]:
        from jose import JWTError, jwt

        from app.config import settings

        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
            if payload.get("type") != "refresh":
                raise Unauthorized("Invalid refresh token")
            user_id: int = payload.get("sub")
        except JWTError:
            raise Unauthorized("Invalid refresh token")

        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            raise Unauthorized("User not found or inactive")

        return _create_access_token(user.id), _create_refresh_token(user.id)

    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def update_user(self, user_id: int, data: dict) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(user, key, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user
