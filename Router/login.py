import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Response, Cookie
from pydantic import BaseModel

from models import User,Session
from fastapi.security import HTTPBearer
from fastapi import Depends

class LoginRequest(BaseModel):
    username: str
    password: str
router = APIRouter(prefix="/api")

@router.get("/init")
async def get_user_by_session(
        session_id: str = Cookie(None,alias="session_id")
):
    if not session_id:
        raise HTTPException(status_code=401, detail="未提供会话ID")
    session = await Session.get_or_none(
        session_id=session_id,
        expires_at__gt=datetime.now()
    ).prefetch_related("user")
    if not session or not session.user:
        raise HTTPException(status_code=401, detail="会话无效或已过期")
    return {
        "code":200,
        "message": "获取成功",
        "data": {
            "id": session.user.id,
            "name": session.user.username,
            "email": session.user.email
        }
    }
#创建/api/login的登陆接口
@router.post("/login")
#用loginRequest来接受POST请求的数据
async def login(request: LoginRequest,response: Response):
    #从数据库中查询用户名是否存在
    user = await User.get_or_none(username=request.username)

    #如果不存在 或者说密码不正确 则返回错误信息
    if not user or user.password != request.password:
        raise HTTPException(
            #状态码401
            status_code=401,
            #错误信息
            detail={
                "code": 401,
                "message": "用户名或密码错误"  # 结构化数据
            }
        )
    #给他SessionID
    session_id = secrets.token_urlsafe(32)
    await Session.create(
        session_id=session_id,
        user=user,
        expires_at=datetime.now() + timedelta(days=1),
    )

    #给他cookies
    response.set_cookie(
        key="session_id",
        value=session_id,
        max_age=3600*24,
        httponly=False,
        secure=False,
        samesite="lax"
    )

    return {"code": 200, "message": "Login successful"}


#从数据库获取用户信息
async def get_user_by_username(username: str):
    return await User.get_or_none(username=username)

security = HTTPBearer()
async def get_current_user(session_id: str = Depends(security)) -> User:
    # 1. 验证 Session 是否存在
    session = await Session.get_or_none(
        session_id=session_id,
        expires_at__gt=datetime.now()
    )
    if not session:
        raise HTTPException(status_code=401, detail="无效会话")

    # 2. 返回关联的用户对象
    return await User.get(id=session.user.id)
async def get_session_id_from_cookie(session_id: str = Depends(security)):
    return session_id