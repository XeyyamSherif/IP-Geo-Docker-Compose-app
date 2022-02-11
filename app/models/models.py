from peewee import *
from .base import BaseModel


class UserModel(BaseModel):
    first_name = CharField(max_length=30)
    password = CharField(max_length=30)

    class Meta:
        db_table = 'user'


class TaskModel(BaseModel):
    city = CharField(max_length=60)

    class Meta:
        db_table = 'task'
