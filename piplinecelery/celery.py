from __future__ import absolute_import
from celery import Celery
from settings import REDIS_HOST, REDIS_PORT

app = Celery('piplinecelery',
             broker="redis://{0}:{1}".format(REDIS_HOST, REDIS_PORT),
             backend="redis://{0}:{1}".format(REDIS_HOST, REDIS_PORT),
             include=['core.Tasks'])

app.conf.update(
    result_expires=3600,
)


if __name__ == '__main__':
    app.start()
