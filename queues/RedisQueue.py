import redis as pyredis
import threading
from settings import REDIS_PORT, REDIS_HOST
"""This model is a impelmention of redis message queue"""


class RedisQueue:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        self.pool = pyredis.ConnectionPool(host=host, port=port)

    def get_value(self, key):
        redis = pyredis.StrictRedis(connection_pool=self.pool)
        return redis.get(key)

    def set_value(self, key, value, time=0):
        redis = pyredis.StrictRedis(connection_pool=self.pool)
        if time != 0:
            redis.set(name=key, value=value, ex=time)
        else:
            redis.set(name=key, value=value)

    def channel(self, topic, action='p'):
        """Public or subscribe a channel

        This function create a topic in redis, and return a
        publish function or subscribe function according to
        the input paragm
        Args:
            topic (str): The channel name
            action (str): p for create channel, s for subscribe channel

        Returns:
            func: the publish function or subscribe function

        Samples:
            create a topic:
            publish = channel('topic')
            for i in range(100):
                publish(i)

        """

        redis = pyredis.StrictRedis(connection_pool=self.pool)

        def publish(msg):
            redis.publish(topic, msg)
            return True

        def subscribe():
            msg = pub.parse_response()
            return msg

        if action == 'p':
            return publish
        elif action == 's':
            pub = redis.pubsub()
            pub.subscribe(topic)
            msg = pub.parse_response()
            print(msg)
            return subscribe
