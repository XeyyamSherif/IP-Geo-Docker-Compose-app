import time
from celery import Celery
from celery.utils.log import get_task_logger
from models.models import TaskModel
from requests import get
from ipdata import ipdata


ipdata = ipdata.IPData(
    '7cf8f3f50e643b268994e1ae1e0eab54e87f2b04055498cbf044222d')

logger = get_task_logger(__name__)

celery_app = Celery('tasks',
                    broker='amqp://admin:mypass@rabbit:5672',
                    backend='rpc://', include=['tasks'])


@celery_app.task()
def longtime_add(id):
    ip = get('https://api.ipify.org').text
    response = ipdata.lookup(ip)
    task_city = TaskModel(id=id)
    task_city.city = response['city']
    task_city.save()
    return {'city': task_city.city}
