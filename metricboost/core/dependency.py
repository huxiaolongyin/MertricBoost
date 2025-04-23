from typing import Any

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from metricboost.config import SETTINGS
from metricboost.core.ctx import CTX_USER_ID
from metricboost.core.exceptions import HTTPException
from metricboost.models.system import User

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/token")


def check_token(token: str) -> tuple[bool, int, Any]:
    try:
        options = {"verify_signature": True, "verify_aud": False, "exp": True}
        decode_data = jwt.decode(
            token,
            SETTINGS.SECRET_KEY,
            algorithms=[SETTINGS.JWT_ALGORITHM],
            options=options,
        )
        return True, 0, decode_data
    except jwt.DecodeError:
        return False, 4010, "无效的Token"
    except jwt.ExpiredSignatureError:
        return False, 4010, "登录已过期"
    except Exception as e:
        return False, 5000, f"{repr(e)}"


class AuthControl:
    @classmethod
    async def is_authed(cls, token: str = Depends(oauth2_schema)) -> User | None:
        user_id = CTX_USER_ID.get()
        if user_id == 0:
            status, code, decode_data = check_token(token)
            if not status:
                raise HTTPException(code=code, msg=decode_data)

            if decode_data["data"]["tokenType"] != "accessToken":
                raise HTTPException(code="4010", msg="The token is not an access token")

            user_id = decode_data["data"]["userId"]

        user = await User.filter(id=user_id).first()
        if not user:
            raise HTTPException(
                code="4040",
                msg=f"Authentication failed, the user_id: {user_id} does not exists in the system.",
            )
        CTX_USER_ID.set(int(user_id))
        return user


DependAuth = Depends(AuthControl.is_authed)
