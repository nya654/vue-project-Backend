from fastapi import APIRouter, HTTPException, Depends, Request,Query
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
    id: int
    content: str
    is_finish: bool = False


@router.post("/addthing")
async def addthing(
        request: ThingCreate,
        current_user: User = Depends(get_current_user)  # 正确使用依赖注入
):
    """创建待办事项"""
    # 现在current_user已经是验证后的用户对象
    new_thing = await Thing.create(
        content=request.content,
        author_id=current_user.id,  # 确保Thing模型有user_id字段
        is_finish= request.is_finish
    )

    return {
        "code": 200,
        "message": "创建成功",
        "data": {
            "id": new_thing.id,
            "content": new_thing.content,
            "is_finish": new_thing.is_finish,
        }
    }

@router.get("/getthings/{date}")
async def getthing(date: str , current_user: User = Depends(get_current_user)):
    target_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = target_date.replace(hour=0, minute=0, second=0)
    end_date = target_date.replace(hour=23, minute=59, second=59)


    contents = await Thing.filter(
            create_at__gte=start_date,create_at__lte=end_date
        ).filter(author_id=current_user.id).values_list("content","is_finish","id")
    return {
        "code": 200,
        "message": "获取成功",
        "data": {
            "items": contents
        }
    }

@router.put("/updatethings/{thing_id}")
async def updatethings(thing_id: int,
                       request: ThingCreate
                       ):

    update_data = {
        "content": request.content,
        "is_finish": request.is_finish
    }

    await Thing.filter(id=thing_id).update(**update_data)
    return {
        "code": 200,
        "message": "更新成功"
    }

@router.delete("/deletethings/{thing_id}")
async def deletethings(thing_id: int):
    await Thing.filter(id=thing_id).delete()
    return {
        "code": 200,
        "message": "删除成功"
    }