from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.exceptions import HTTPException
from models.schemas import User, UserLogin, StatusSchema
from models.models import UserModel, TaskModel
from models.base import db
from fastapi_jwt_auth import AuthJWT
from requests import get
from celery import Celery
from tasks import longtime_add, celery_app
from celery.result import AsyncResult


app = FastAPI()


@app.on_event("startup")
def startup():
    db.connect()
    db.create_tables([UserModel, TaskModel])
    db.close()
    print("Connected, and created")


@app.post('/sign_up')
def create(user_created: User):
    new_user = UserModel(
        first_name=user_created.first_name,
        password=user_created.password
    )
    new_user.save()

    return user_created


@app.post('/login')
def sign_in(signed_user: UserLogin, Authorize: AuthJWT = Depends()):
    for item in UserModel:
        if (item.first_name == signed_user.username and item.password == signed_user.password):
            acces_token = Authorize.create_access_token(
                subject=signed_user.username)
            refresh_token = Authorize.create_refresh_token(
                subject=signed_user.username)
            return {'access_token': acces_token, 'refresh_toke': refresh_token}
        raise HTTPException(status_code='401',
                            detail='invalid username or password')


@app.get('/user')
def user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token')

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


@app.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token')

    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}


@app.get('/refresh')
def new_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token')

    current_user = Authorize.get_jwt_subject()
    acces_token = Authorize.create_access_token(subject=current_user)

    return {'new acces token': acces_token}


@app.get('/task')
def task():
    '''
    Burda task tam olaraq dəqiq qeyd olunayıb, ona görə app userin ip-sini avtomatik götürüb işlədəcək.
    Amma üstündə istənilən dəyişiklik asanlıqla edə bilərəm, istəyə görə

    '''

    new_task = TaskModel(
        city=''
    )
    new_task.save()
    r = longtime_add.delay(new_task.__data__['id'])
    return {"task id": r.id}


@app.get('/status')
def task(task: StatusSchema):
    try:
        taskResult = celery_app.AsyncResult(task.id)
        return taskResult.get()
    except:
        return {'message': 'invalid task id'}
