import re

class DialoStatus(object):
    def __init__(self):
        self.intent = None
        self.cache = [] # 缓存记录
        self.mode = None # 模式: 检索｜任务｜生成
        self.memo = [] # 备忘录

    def update_intent(self, input):

        pass