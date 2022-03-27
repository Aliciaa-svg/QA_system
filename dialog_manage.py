import re

class DialoStatus(object):
    def __init__(self):
        self.intent = None
        self.cache = [] # 缓存记录