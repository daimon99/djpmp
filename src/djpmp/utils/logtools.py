# coding: utf-8
import time


class TimeIt(object):
    """计时器。

    用法::

        with httplog.TimeIt() as timeit:
            res = requests.post(url, json=payload)
        httplog.http_log_from_response('upload_case', res, timeit.duration)

    """

    def __init__(self):
        self.start = 0
        self.end = 0

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()

    @property
    def duration(self):
        return int((self.end - self.start) * 1000)
