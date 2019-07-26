import pickle
import time
import json
from settings import MESSAGE_CHANNEL, DATA_PROCESSORS
from core.tasks import app, start_process
from queues.redisqueue import RedisQueue

__all__ = ["main_loop"]

def main_loop(batch_size=10):
    """主要循环， 从消息队列中获取数据，分发给执行进程执行
    args:
        batch_size: 当同一标志的数据积累到batch_size个的时候，开始处理
    """
    data_bag = {}
    for data_type in DATA_PROCESSORS:
        data_bag[data_type] = []
    message_queue = RedisQueue()
    sub = message_queue.channel(MESSAGE_CHANNEL, 's')
    try:
        while True:
            try:
                data_origin = sub()
            except ConnectionError as e:
                print("connect error, retry after 1 seconds")
                time.sleep(1)
                sub = message_queue.channel(MESSAGE_CHANNEL, 's')
                continue
            except TimeoutError as e:
                print("connect time out, retry after 1 seconds")
                time.sleep(1)
                sub = message_queue.channel(MESSAGE_CHANNEL, 's')
                continue

            try:
                data = json.loads(data_origin[-1].decode())
            except Exception as e:
                print("json loads failed")

            if "_meta" not in data['_meta']:
                print("_meta is necessary for data dispatch")

            data_type = data['_meta']['data_type']
            data_bag[data_type] = data_bag.get(data_type, []) + [data]
            if len(data_bag[data_type]) >= batch_size:
                start_process.delay(data_bag[data_type], data_type)
                data_bag[data_type] = []

    finally:
        print("shutting down")
