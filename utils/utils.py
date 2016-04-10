import time
import datetime


class Utils(object):
    def __init__(self):
        pass

    def get_date_time(self):
        # return time.strftime("%Y-%m-%d %H:%M:%S")
        return datetime.datetime.strptime(
            time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
