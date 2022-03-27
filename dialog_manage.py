import re
from taskbot import birth, memo, tarot

class DialoStatus(object):
    def __init__(self):
        self.intent = None # 意图
        self.cache = [] # 缓存记录
        self.mode = None # 模式: 检索｜任务｜生成
        self.memo = [] # 备忘录
        self.output = []

    def update_intent(self, input):
        if re.search(r"塔罗|占卜", input):
            self.intent = 'tarot start'
            self.mode = 'task'
        elif re.search(r"八字|生辰|五行", input):
            self.intent = 'bazi start'
            self.mode = 'task'
        elif re.search(r"记录|记下|备忘", input):
            self.intent = 'memo'
            self.mode = 'task'