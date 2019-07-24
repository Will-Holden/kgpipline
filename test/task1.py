from celery import Celery


app = Celery('tasks',
             broker="redis://{0}:{1}/0".format("rembern.com", 32379))


def add(x,y):
    print("add 2 : %s %s" %(x,y))
    return x + y
