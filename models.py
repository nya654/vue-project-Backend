from tortoise.models import Model
from tortoise import fields
from datetime import datetime, timedelta
import secrets


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    things: fields.ReverseRelation["Thing"]

    class Meta:
        table = "users"  # 显式指定表名


class Thing(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    create_at = fields.DatetimeField(auto_now_add=True)
    is_finish = fields.BooleanField(default=False)
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        related_name="things",
        on_delete=fields.CASCADE  # 级联删除
    )

    class Meta:
        table = "things"


class Session(Model):
    id = fields.IntField(pk=True)
    session_id = fields.CharField(max_length=255, unique=True)  # 唯一约束
    user = fields.ForeignKeyField(  # 👈 正确写法
        "models.User",
        related_name="sessions",
        on_delete=fields.CASCADE
    )
    expires_at = fields.DatetimeField()  # 必须的过期时间
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "sessions"
        indexes = [
            ("session_id", "expires_at"),  # 组合索引
            ("user_id",)  # 单字段索引
        ]