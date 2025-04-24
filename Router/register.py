from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import User

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str

register_router = APIRouter(prefix="/api")

@register_router.post("/register")
async def register(request: RegisterRequest):
    user = await User.get_or_none(username=request.username)
    email = await User.get_or_none(email=request.email)

    if email:
        raise HTTPException(
            status_code=401,
            detail={
                "code":401,
                "message": "该邮箱已经被人注册过了"
            }
        )
    #如果User存在 抛出401错误
    if user:
        raise HTTPException(
            status_code=401,
            detail={
                "code":401,
                "message": "该用户已经存在"
            }
        )
    #如果User不存在的话 直接创建
    await User.create(
        username=request.username,
        password=request.password,
        email=request.email
    )
    return {"code": 200, "message": "register successful"}
