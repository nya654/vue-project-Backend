from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from datetime import datetime
from models import User, Session, Thing  # 确保导入了Thing模型
from fastapi.security import HTTPBearer
from fastapi import Cookie

security = HTTPBearer()
router = APIRouter(prefix="/api")


async def get_current_user(
        session_id: str = Cookie(None, alias="session_id")  # 👈 从 Cookie 获取
) -> User:
    if not session_id:
        raise HTTPException(status_code=401, detail="未提供会话ID")

    session = await Session.get_or_none(
        session_id=session_id,
        expires_at__gt=datetime.now()
    ).prefetch_related("user")
    if not session or not session.user:
        raise HTTPException(status_code=401, detail="会话无效或已过期")

    return session.user


class ThingCreate(BaseModel):  # 改个更准确的名字
    content: str


@router.post("/addthing")
async def addthing(
        request: ThingCreate,
        current_user: User = Depends(get_current_user)  # 正确使用依赖注入
):
    """创建待办事项"""
    # 现在current_user已经是验证后的用户对象
    new_thing = await Thing.create(
        content=request.content,
        author_id=current_user.id  # 确保Thing模型有user_id字段
    )

    return {
        "code": 200,
        "message": "创建成功",
        "data": {
            "id": new_thing.id,
            "content": new_thing.content
        }
    }