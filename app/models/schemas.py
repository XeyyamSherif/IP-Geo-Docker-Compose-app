from peewee import *
import peewee
from typing import Any
from pydantic import BaseModel
from pydantic.utils import GetterDict
from fastapi_jwt_auth import AuthJWT


class Settings(BaseModel):
    authjwt_secret_key: str = '2bb4ce7878a0b00b0fe30951f649a23bcf253745f0285260bc1269d14eaa443b'


@AuthJWT.load_config
def get_config():
    return Settings()


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class User(BaseModel):
    id: int
    first_name: str
    password: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class StatusSchema(BaseModel):
    id: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
