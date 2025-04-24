from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import User

class LoginRequest(BaseModel):
    username: str
    password: str
router = APIRouter(prefix="/api")


#创建/api/login的登陆接口
@router.post("/login")
#用loginRequest来接受POST请求的数据
async def login(request: LoginRequest):
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

    return {"code": 200, "message": "Login successful"}


#从数据库获取用户信息
async def get_user_by_username(username: str):
    return await User.get_or_none(username=username)