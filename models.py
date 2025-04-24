from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True,generated=True)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)