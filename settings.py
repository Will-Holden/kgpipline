import os
from logging import WARN, ERROR, FATAL, CRITICAL, DEBUG, INFO

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PROCESSORS = ['news']

MESSAGE_CHANNEL = "scrapy"
BROKER_TRANSPORT_OPTION = {'visibility_timeout': 3600}
CELERY_NAME = "pipline"

REDIS_HOST = "rembern.com"
REDIS_PORT = 32379

MYSQL_HOST = "rembern.com"
MYSQL_PORT = 32306
MYSQL_USER = "xiaolong"
MYSQL_PASSWORD = '123456'
MYSQL_DB = "kb_demo"

MONGO_HOST = "rembern.com"
MONGO_PORT = 32317
MONGO_DB = "kb_demo"
