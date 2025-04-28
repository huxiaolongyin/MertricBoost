# from controllers.system.user import user_controller
# from models.system.user import User
# from core.jwt import create_access_token, JWTPayload
# from core.response import Success
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter

from metricboost.config import SETTINGS
from metricboost.controllers.user import user_controller
from metricboost.core.ctx import CTX_USER_ID
from metricboost.core.dependency import DependAuth, check_token
from metricboost.core.exceptions import HTTPException
from metricboost.core.response import Error, Success
from metricboost.core.security import create_access_token
from metricboost.logger import insert_log, logger
from metricboost.models.enums import StatusType
from metricboost.models.system import Button, LogDetailType, LogType, Role, User
from metricboost.schemas.login import CredentialsSchema, JWTOut, JWTPayload

router = APIRouter()


@router.post("/login", summary="登录")
async def _(credentials: CredentialsSchema):
    try:
        # 账号验证, 失败则触发异常返回请求错误)
        user_obj: User | None = await user_controller.authenticate(credentials)
    except HTTPException as e:
        return Error(code="4000", msg="认证失败")
    await user_controller.update_last_login(user_obj.id)

    payload = JWTPayload(
        data={
            "userId": user_obj.id,
            "userName": user_obj.user_name,
            "tokenType": "accessToken",
        },
        iat=datetime.now(timezone.utc),
        exp=datetime.now(timezone.utc),
    )
    access_token_payload = payload.model_copy(deep=True)
    access_token_payload.exp += timedelta(
        minutes=SETTINGS.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token_payload = payload.model_copy(deep=True)
    refresh_token_payload.data["tokenType"] = "refreshToken"
    refresh_token_payload.exp += timedelta(
        minutes=SETTINGS.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
    )
    data = JWTOut(
        access_token=create_access_token(data=access_token_payload),
        refresh_token=create_access_token(data=refresh_token_payload),
    )
    await insert_log(
        log_type=LogType.UserLog,
        log_detail_type=LogDetailType.UserLoginSuccess,
        log_detail="用户登录成功",
        by_user_id=user_obj.id,
    )
    return Success(data=data.model_dump(by_alias=True))


@router.post("/refreshToken", summary="刷新认证")
async def _(jwt_token: JWTOut):
    if not jwt_token.refresh_token:
        return Error(code="4000", msg="The refreshToken is not valid.")
    status, code, data = check_token(jwt_token.refresh_token)
    if not status:
        return Error(code=code, msg=data)
    user_id = data["data"]["userId"]
    user_obj = await user_controller.get(user_id)

    if data["data"]["tokenType"] != "refreshToken":
        return Error(code="4000", msg="The token is not an refresh token.")

    if user_obj.status == StatusType.disable:
        await insert_log(
            log_type=LogType.UserLog,
            log_detail_type=LogDetailType.UserLoginForbid,
            log_detail="用户被禁用",
            by_user_id=user_id,
        )
        return Error(code="4030", msg="This user has been disabled.")

    await user_controller.update_last_login(user_id)
    payload = JWTPayload(
        data={
            "userId": user_obj.id,
            "userName": user_obj.user_name,
            "tokenType": "accessToken",
        },
        iat=datetime.now(timezone.utc),
        exp=datetime.now(timezone.utc),
    )
    access_token_payload = payload.model_copy()
    access_token_payload.exp += timedelta(
        minutes=SETTINGS.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token_payload = payload.model_copy()
    refresh_token_payload.data["tokenType"] = "refreshToken"
    refresh_token_payload.exp += timedelta(
        minutes=SETTINGS.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
    )
    data = JWTOut(
        access_token=create_access_token(data=access_token_payload),
        refresh_token=create_access_token(data=refresh_token_payload),
    )
    await insert_log(
        log_type=LogType.UserLog,
        log_detail_type=LogDetailType.UserAuthRefreshTokenSuccess,
        log_detail="用户刷新token成功",
        by_user_id=user_obj.id,
    )
    return Success(data=data.model_dump(by_alias=True))


@router.get("/getUserInfo", summary="查看用户信息", dependencies=[DependAuth])
async def _():
    try:
        user_id = CTX_USER_ID.get()
        user_obj: User = await user_controller.get(id=user_id)
        data = await user_obj.to_dict(exclude_fields=["password"])

        user_roles: list[Role] = await user_obj.roles
        user_role_codes = [user_role.role_code for user_role in user_roles]

        user_role_button_codes = (
            [b.button_code for b in await Button.all()]
            if "R_SUPER" in user_role_codes
            else [
                b.button_code
                for user_role in user_roles
                for b in await user_role.buttons
            ]
        )

        user_role_button_codes = list(set(user_role_button_codes))

        data.update(
            {
                "user_id": user_id,
                "roles": user_role_codes,
                "buttons": user_role_button_codes,
            }
        )
        await insert_log(
            log_type=LogType.UserLog,
            log_detail_type=LogDetailType.UserLoginGetUserInfo,
            log_detail="用户获取用户信息",
            by_user_id=user_obj.id,
        )
        return Success(data=data)
    except Exception as e:
        return Error(code="5000", msg=f"获取用户信息失败, error: {e}")


@router.get("/error", summary="自定义后端错误")  # todo 使用限流器, 每秒最多一次
async def _(code: str, msg: str):
    if code == "9999":
        return Success(code="4030", msg="accessToken已过期")

    return Error(code=code, msg=f"未知错误, code: {code} msg: {msg}")
