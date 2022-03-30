# 成晓雪
# 创建时间：2022/3/24 21:28
# from util import word_tokenize
import search_QA.util
from search_QA.search.star import get_star_sign
from search_QA.search.weather import weathers


def predict(query):
    # 对输入文本分词
    query = search_QA.util.word_tokenize(query)
    for word in query:
        if word in ['天气', '气温', '今天天气', '今日天气']:
            return weathers('天津')
        if word in ['星座','星座运势','运势']:
            return get_star_sign('白羊座')


# if __name__ == '__main__':
def main(question):
    while True:
        # question = input("请输入(q退出): ")
        if question == 'q':
            break
        message = predict(question)

        # time1 = time.time()
        # question_k = predict(sif_model, question)
        # f = "output.txt"
        # print("输出： {}".format(message))
        return message
        # with open(f, "w") as file:  # ”w"代表着每次运行都覆盖内容
        #     file.write(answers[question_k[0]])
        # for idx in question_k:
        #     print("same questions： {}".format(questions_src[idx]))
        # time2 = time.time()
        # cost = time2 - time1
        # print('Time cost: {} s'.format(cost))