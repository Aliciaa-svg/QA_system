# -*- coding: utf-8 -*-
# @Time    : 2019/4/3 16:48
# @Author  : Alan
# @Email   : xiezhengwen2013@163.com
# @File    : tmodel.py
# @Software: PyCharm

import pandas as pd
import matplotlib as mpl
import numpy as np
from nltk.probability import FreqDist
import time

from QA_base.jiebaSegment import *
from QA_base.sentenceSimilarity import SentenceSimilarity

mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # enable chinese

def read_corpus():
    qList = []
    # 问题的关键词列表
    # qList_kw = []
    # aList = []
    # data = pd.read_csv('data/data.csv', header=None)
    # data_ls = np.array(data).tolist()
    # for t in data_ls:
    #     qList.append(t[0])
    #     # qList_kw.append(seg.cut(t[0]))
    #     aList.append(t[1])
    # np.save('./QA_base/qList', np.array(qList))
    # np.save('./QA_base/aList', np.array(aList))
    qList = np.load('./QA_base/qList.npy')
    aList = np.load('./QA_base/aList.npy')
    return None, qList, aList


def plot_words(wordList):
    fDist = FreqDist(wordList)
    #print(fDist.most_common())
    print("单词总数: ",fDist.N())
    print("不同单词数: ",fDist.B())
    fDist.plot(10)


def main(question):
    # 设置外部词
    seg = Seg()
    seg.load_userdict('./QA_base/userdict/userdict.txt')
    # 读取数据
    List_kw, questionList, answerList = read_corpus()
    # 初始化模型
    ss = SentenceSimilarity(seg)
    ss.set_sentences(questionList)
    # ss.TfidfModel()         # tfidf模型
    # ss.LsiModel()         # lsi模型
    # ss.LdaModel()         # lda模型
    ss.Bm25Model()

    while True:
        # question = input("请输入问题(q退出): ")
        if question == 'q':
            break
        time1 = time.time()
        question_k = ss.similarity_k(question, 5)
        f = "output.txt"
        # print("亲，我们给您找到的答案是： {}".format(answerList[question_k[0][0]]))
        # with open(f, "w") as file:  # ”w"代表着每次运行都覆盖内容
        #     file.write(answerList[question_k[0][0]])
        # for idx, score in zip(*question_k):
        #     print("same questions： {},                score： {}".format(questionList[idx], score))
        time2 = time.time()
        cost = time2 - time1
        # print('Time cost: {} s'.format(cost))
        return questionList[0], answerList[question_k[0][0]]








