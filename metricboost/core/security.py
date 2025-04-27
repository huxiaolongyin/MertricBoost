import jwt
from passlib.context import CryptContext

from metricboost.config import SETTINGS
from metricboost.schemas.login import JWTPayload

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def create_access_token(*, data: JWTPayload):
    payload = data.model_dump().copy()
    encoded_jwt = jwt.encode(
        payload, SETTINGS.SECRET_KEY, algorithm=SETTINGS.JWT_ALGORITHM
    )
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False
