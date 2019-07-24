from core.Singleton import Singleton
from core.Tasks import BaseTask

class Status(metaclass=Singleton):
    """
    在一个字典中，存储整个系统的状态信息
    """

    def __init__(self):
        self.data = {}

    def __setitem__(self, key, value):
        return self.data.__setitem__(key, value)

    def __getitem__(self, obj):
        return self.data.__getitem__(obj)

    def __delitem__(self, key):
        return self.data.__delitem__(key)

    def __len__(self):
        return self.data.__len__()

    def add_task(self, task_name, task=None):
        if task_name in self.data.keys():
            raise ValueError("task already exists")
        else:
            self.data[task_name] = BaseTask()
            return True

    def get_task(self, task_name):
        if task_name not in self.data.keys():
            raise ValueError("task not exists")
        else:
            task = self.data[task_name]
            if not isinstance(task, BaseTask):
                raise ValueError("{0} is not a task".format(task_name))
            else:
                return self.data[task_name]
