import re
import search_QA.main
from search_QA import demo
from taskbot import birth, memo, tarot
from QA_STS import main
from GPT2 import interact
from QA_base import tmodel1


class DialoStatus(object):
    def __init__(self):
        self.intent = 'end' # 意图
        self.cache = [] # 缓存记录
        self.mode = None # 模式: 任务|解梦|其他
        self.memo = [] # 备忘录
        self.memo_process = None
        self.bazi = None
        self.dream_process = None
        self.output = []

    def update_intent(self, input):
        if self.intent != 'end':
            pass
        else: 
            if re.search(r"塔罗|占卜", input): # 任务：塔罗占卜
                self.intent = 'tarot start'
                self.mode = 'task'
            elif re.search(r"八字|生辰|五行", input): # 任务：计算八字与五行得分
                self.intent = 'bazi start'
                self.bazi = 'start'
                self.mode = 'task'
            elif re.search(r"打开备忘", input): # 任务：备忘录记录
                self.intent = 'memo'
                self.memo_process = 'start'
                self.mode = 'task'
            elif re.search(r"查询备忘|查备忘|查看备忘", input): # 任务：备忘录查询
                self.intent = 'memo check'
                self.memo_process = 'start'
                self.mode = 'task'
            elif re.search(r"清空备忘|删除备忘", input): # 任务：备忘录清空
                self.intent = 'memo delete'
                self.memo_process = 'start'
                self.mode = 'task'
            elif re.search(r"天气|气温|温度|气候", input): # 任务：气候查询
                self.intent = 'weather'
                self.mode = 'task'
            elif re.search(r"日期|日子|多少号", input): # 任务：气候查询
                self.intent = 'date'
                self.mode = 'task'
            elif re.search(r"星座|运势|运气|白羊|金牛|双子|巨蟹|狮子|处女|天秤|天蝎|射手|摩羯|水瓶座|双鱼", input): # 任务：星座运势
                self.intent = 'star'
                self.mode = 'task'
            elif re.search(r"梦到|梦见|做梦|解梦|梦境", input): # 其他：解梦
                self.intent = 'dream'
                self.dream_process = 'start'
                self.mode = 'others'
            else: # 其他：闲聊
                self.intent = 'chat'
                self.mode = 'others'

    def process_dialog(self, input):
        if self.mode == 'task':
            """
            任务型对话：优先级最高
            """
            if self.intent == 'tarot start': # 塔罗
                self.output = tarot.tarot(input, self)
            elif self.intent == 'memo': # 备忘-记录
                self.output = memo.memo(input, self)
            elif self.intent == 'memo check': # 备忘-查询
                self.output = memo.memo_check(input, self)
            elif self.intent == 'memo delete': # 备忘-查询
                self.output = memo.memo_delete(input, self)
            elif self.intent == 'bazi start': # 八字五行
                self.output = birth.birth(input, self.cache, self)
            elif self.intent == 'weather' or self.intent == 'star' or self.intent == 'date': # 查询天气&星座
                self.output = demo.main(input)
                self.intent = 'end'
        else: 
            """
            其他类型：检索&生成
            """
            if self.intent == 'dream': # (a)解梦 
                # (NOTE: Tianyi) 
                # 检索型options: BERT+CoSENT | BM25 | SIF 
                if self.dream_process == 'start':
                    self.output = '你梦见了什么呢'
                    self.dream_process = 'end'
                else:
                    # re_ques, self.output = search_QA.main.main(input) # SIF
                    re_ques, self.output = tmodel1.main(input) # BM25
                    self.intent = 'end'
                    
                    # if score >= 0.75: # (检索得分 > p)则采用检索得到的回答，否则采用生成式得到的回答
                    #     self.output = retrieve_ans
                    # else:
                    #     # 生成式暂时使用GPT2
                    #     self.output = interact.main(self.intent, input)
            else: # (b)闲聊
                mode = self.intent
                # print(mode)
                self.output = interact.main(mode, input)


if __name__ == '__main__':
    dialog_status = DialoStatus()
    
    while True:

        query = input('user:')
        
        dialog_status.update_intent(query)
        dialog_status.process_dialog(query)
        # if type(dialog_status.output) == list:
        #     ans = ''
        #     for i in range(2):
        #         ans += dialog_status.output[i]
        #     print('bot:', ans)
        #     ans = ''
        #     for i in range(2,4):
        #         ans += dialog_status.output[i]
        #     print('bot:你抽到了', ans)
        #     ans = ''
        #     for i in range(4, 6):
        #         ans += dialog_status.output[i]
        #     print('bot:', ans)
        #     ans = ''
        #     for i in range(6,8):
        #         ans += dialog_status.output[i]
        #     print('bot:你抽到了', ans)
        #     ans = ''
        #     for i in range(8,10):
        #         ans += dialog_status.output[i]
        #     print('bot:', ans)
        #     ans = ''
        #     for i in range(10,12):
        #         ans += dialog_status.output[i]
        #     print('bot:你抽到了', ans)
        #     ans = ''
        #     for i in range(12,14):
        #         ans += dialog_status.output[i]
        #     print('bot:', ans)
        #     ans = ''
        #     for i in range(14,16):
        #         ans += dialog_status.output[i]
        #     print('bot:你抽到了', ans)
        # else:
        print('bot:', dialog_status.output)
            

            