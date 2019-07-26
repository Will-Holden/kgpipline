"""
任务分发模块，负责将任务分配给执行节点执行
依赖于 celery
"""

import pandas as pd
from piplinecelery.celery import app
from core.status import Status
import logging


@app.task
def start_process(data, task_name):
    """数据处理流程入口"""
    data = pd.DataFrame(data)
    task = Status().get_task(task_name)
    try:
        task.process(data)
    except Exception as e:
        logging.info("error occured when executing task {0}".format(task_name))

from abc import ABCMeta, abstractmethod
import time


class BaseTask:
    """
    基础的任务模块
    """
    steps = []

    def __len__(self):
        return len(self.steps)

    def add_step(self, step, priority):
        """添加执行步骤
        args:
        priority:优先级，数值越大，越早被执行"""

        if not isinstance(step, BaseStep):
            raise ValueError("step provided not a Step")
        else:
            self.steps.append((step, priority))
            self.steps = sorted(self.steps, key=lambda x: x[1], reverse=True)

    def process(self, datas):
        """逐步执行任务
        """
        logging.info("there is {0} steps to be executed".format(self.__len__()))
        for index, step in enumerate(self.steps):
            logging.info("executing the {0} step, step name is {1}".format(index, step))
            start_time = time.time()
            datas = step[0].fit(datas)
            end_time = time.time()
            logging.info("step {0} cost time {1}".format(index, end_time - start_time))
            logging.info("data processed {0}".format(datas))
            return datas


class BaseStep:
    """
    一步处理
    """

    def fit(self, data):
        # 处理逻辑
        return data
