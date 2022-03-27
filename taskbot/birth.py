import re
import ganzhi
import math
import numpy as np

tiangans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
dizhis = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
wuxings = ["金", "木", "水", "火", "土"]

char2num = {
    "零": "0",
    "一": "1",
    "二": "2",
    "三": "3",
    "四": "4",
    "五": "5",
    "六": "6",
    "七": "7",
    "八": "8",
    "九": "9",
    "十": "10",
    "十一": "11",
    "十二": "12",
    "十三": "13",
    "十四": "14",
    "十五": "15",
    "十六": "16",
    "十七": "17",
    "十八": "18",
    "十九": "19",
    "二十": "20",
    "二十一": "21",
    "二十二": "22",
    "二十三": "23",
    "二十四": "24",
    "二十五": "25",
    "二十六": "26",
    "二十七": "27",
    "二十八": "28",
    "二十九": "29",
    "三十": "30",
    "三十一": "31"
}

wuxingDicForTiangan = {
    "甲": "木",
    "乙": "木",
    "丙": "火",
    "丁": "火",
    "戊": "土",
    "己": "土",
    "庚": "金",
    "辛": "金",
    "壬": "水",
    "癸": "水"
}
wuxingDicForDizhi = {
    "子": "水",
    "丑": "土",
    "寅": "木",
    "卯": "木",
    "辰": "土",
    "巳": "火",
    "午": "火",
    "未": "土",
    "申": "金",
    "酉": "金",
    "戌": "土",
    "亥": "水"
}

num2char = {
    '0': '零',
    '1': '一',
    '2': '二',
    '3': '三',
    '4': '四',
    '5': '五',
    '6': '六',
    '7': '七',
    '8': '八',
    '9': '九',
    '10': '十',
    '11': '十一',
    '12': '十二',
    '13': '十三',
    '14': '十四',
    '15': '十五',
    '16': '十六',
    '17': '十七',
    '18': '十八',
    '19': '十九',
    '20': '二十',
    '21': '二十一',
    '22': '二十二',
    '23': '二十三',
    '24': '二十四'
}

def getTime(tiangan, time):
    idx = (2 * tiangan - 1) % 10
    if time == 23 or time == 0 or time == 24:
        dizhi = dizhis[0]
        dizhiIdx = 0
    else:
        dizhiIdx = time / 2
        if dizhiIdx >= 0.5:
            dizhiIdx = math.ceil(dizhiIdx)
        else:
            dizhiIdx = round(dizhiIdx)
        dizhi = dizhis[dizhiIdx]
    return tiangans[(idx + dizhiIdx - 1) % 10] + dizhi
        

def getBazi(cache):
    year = int(cache[0])
    month = int(cache[1])
    day = int(cache[2])
    time = int(cache[3])

    data = ganzhi.day(year, month, day)
    tiangan = data[2]
    tiangan_symbol = tiangans.index(tiangan) + 1
    ganzhi_time = getTime(tiangan_symbol, time)

    return data[0] + '-' + ganzhi_time

def getWuxing(cache):
    bazi_list = str(cache[0]).split('-')
    wuxing_list = []
    cnt = np.zeros(5) # 金｜木｜水｜火｜土
    score = np.zeros(5)

    for b in bazi_list:
        wuxing_list.append(wuxingDicForTiangan[b[0]])
        wuxing_list.append(wuxingDicForDizhi[b[1]])
    for w in wuxing_list:
        if w == '金':
            cnt[0] += 1
        elif w == '木':
            cnt[1] += 1
        elif w == '水':
            cnt[2] += 1
        elif w == '火':
            cnt[3] += 1
        else:
            cnt[4] += 1
    
    for i in range(5):
        score[i] = str(round(cnt[i] / 8, 2))
    return score


def birth(input, cache, dialog_status):
    # input format: 一九九四/年/五月三十/日
    if dialog_status.intent == "bazi start":
        dialog_status.intent = "year"
        return ("请说出你出生的年份")
    if dialog_status.intent == "year":
        num = []
        for i in range(4):
            num.append(char2num[input[i]])
            ind = ""
        year = ind.join(num)
        cache.append(year)
        dialog_status.intent = "month"
        return ("请说出你出生的月份")
    elif dialog_status.intent == "month":
        month = char2num[input]
        cache.append(month)

        dialog_status.intent = "day"
        return ("请说出你出生的日期")
    elif dialog_status.intent == "day":
        day = char2num[input]
        cache.append(day)
        dialog_status.intent = "time"
        return ("说出出生的时间")
    elif dialog_status.intent == "time":
        time = char2num[input]
        cache.append(time)
        dialog_status.intent = 'calculate bazi'

        bazi = getBazi(cache) 
        cache = []
        cache.append(bazi)  

        wuxing = getWuxing(cache) 

        re_bazi = "你的八字是%s" % bazi

        score_str = []
        for i in range(5):
            nn = str(wuxing[i]).split('.')[1]
            # print(nn)
            # print(type(nn))
            # print(nn[0])
            a = num2char[nn[0]]
            if len(nn) == 1:
                b = '零'
            else:
                b = num2char[nn[1]]
            score_str.append(a+b)

        re_wuxing = "你的八字五行指数为金零点%s木零点%s水零点%s火零点%s土零点%s" % (score_str[0], score_str[1], score_str[2], score_str[3], score_str[4])  
        dialog_status.intent = 'end'  

        return re_bazi + re_wuxing

class DialoStatus(object):
    def __init__(self):
        self.intent = None

dialog_status = DialoStatus()
dialog_status.intent = 'bazi start'
cache = []
while dialog_status.intent != 'end':
    intext = input('input: ')
    print(birth(intext, cache, dialog_status))