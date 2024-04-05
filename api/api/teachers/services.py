from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext

from .models import Teacher
from .exceptions import TeacherNotFoundException, AuthenticationException
from .repositories import BaseTeacherRepository


class ITokenService(ABC):
    @abstractmethod
    def decode(self, token) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    def encode(self, payload: dict) -> str:
        raise NotImplementedError


class JoseJWTService(ITokenService):
    def __init__(self, secret_key: str, algorithm: str) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def decode(self, token) -> dict | None:
        try:
            return jwt.decode(token, self.secret_key, self.algorithm)
        except JWTError:
            return None

    def encode(self, payload: dict) -> str:
        data = payload.copy()
        return jwt.encode(data, self.secret_key, self.algorithm)


class IPasswordService(ABC):
    """interface of service for hashing and verifying passwords"""

    @abstractmethod
    def hash_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError


class BcryptPasswordService:
    """implementation of service for hashing and verifying passwords uses bcrypt algorithm"""

    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.context.verify(plain_password, hashed_password)


class TeacherService:
    def __init__(
        self,
        repo: BaseTeacherRepository,
        pwd_service: IPasswordService,
        jwt_service: ITokenService,
        access_token_expires_minutes: int,
    ):
        self.repo = repo
        self.pwd_service = pwd_service
        self.jwt_service = jwt_service
        self.access_token_expires_minutes = access_token_expires_minutes

    async def get_teacher(self, teacher_id: int):
        teacher = await self.repo.get_by_id(teacher_id)
        if teacher is None:
            raise TeacherNotFoundException(id=teacher_id)
        return teacher

    async def register_teacher(
        self, email: str, password: str, firstname: str, lastname: str
    ):
        teacher = Teacher(
            email=email,
            hashed_password=self.pwd_service.hash_password(password),
            firstname=firstname,
            lastname=lastname,
        )
        await self.repo.add(teacher)
        return teacher

    async def authenticate_teacher(self, email: str, password: str):
        teacher = await self.repo.get_by_email(email)
        if teacher is None or not self.pwd_service.verify_password(
            password, teacher.hashed_password
        ):
            raise AuthenticationException
        return teacher

    async def update_teacher(
        self,
        teacher: Teacher,
        email: str | None = None,
        password: str | None = None,
        firstname: str | None = None,
        lastname: str | None = None,
    ):
        data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": (
                self.password_service.hash_password(password)
                if password is not None
                else None
            ),
        }

        for key, value in data.items():
            if value is not None:
                setattr(teacher, key, value)

        await self.repo.add(teacher)

    def create_access_token(self, teacher: Teacher) -> str:
        payload = {
            "sub": str(teacher.id),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=self.access_token_expires_minutes),
        }
        return self.jwt_service.encode(payload)

    async def get_teacher_by_access_token(self, token: str) -> Teacher:
        payload = self.jwt_service.decode(token)
        if payload is None:
            raise AuthenticationException("token decode error")
        if payload["exp"] < int(datetime.now(timezone.utc).timestamp()):
            raise AuthenticationException("token expired")
        teacher = await self.repo.get_by_id(int(payload["sub"]))
        if teacher is None:
            raise AuthenticationException("token decode error")
        return teacher
