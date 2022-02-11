from peewee import *


db = MySQLDatabase(
    'db', user='user',
    password='password',
    host='db'
)


class BaseModel(Model):
    class Meta:
        database = db
