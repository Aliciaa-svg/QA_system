# 成晓雪
# 创建时间：2022/3/22 19:23

import argparse
import time
from util import get_corpus, word_tokenize, build_word_embedding
from model_zoo.sif_model import SIFRetrievalModel

# 配置参数
parser = argparse.ArgumentParser(description='Information retrieval model hyper-parameter setting.')
parser.add_argument('--input_file_path', type=str, default='./dream.xls', help='Training data location.')
# default='bm25'or'sif'or'tfidf'
parser.add_argument('--model_type', type=str, default='sif', help='Different information retrieval models.')

# gensim模型路径
parser.add_argument('--gensim_model_path', type=str, default='./cached/gensim_model.pkl')
parser.add_argument('--pretrained_gensim_embddings_file', type=str, default='./cached/gensim_word_embddings.txt')
parser.add_argument('--cached_gensim_embedding_file', type=str, default='./cached/embeddings_gensim.pkl')

# 编码维度
parser.add_argument('--embedding_dim', type=int, default=100)

# 最大序列长度
parser.add_argument('--max_seq_len', type=int, default=30)
# pooling策略
parser.add_argument('--pooling_strategy', type=int, default=0)
# pool层数
parser.add_argument('--pooling_layer', type=str, default='-2')

# 属性给与args实例:把parser中设置的所有"add_argument"给返回到args子类实例当中，
# 那么parser中增加的属性内容都会在args实例中，使用即可。
args = parser.parse_args()

# 读取 问题-答案
questions_src, answers = get_corpus(args.input_file_path)

# 分词，返回多个列表组成的列表
questions = [word_tokenize(line) for line in questions_src]
answers_corpus = [word_tokenize(line) for line in answers]

# 第一次运行，需要训练词向量
print('\nBuild gensim model and word vectors...')
corpus = questions + answers_corpus
build_word_embedding(corpus, args.gensim_model_path, args.pretrained_gensim_embddings_file)


def predict(model, query):
    """
    预测
    :param model: 模型
    :param query: 输入文本
    :return: topK
    """
    # 对输入文本分词
    query = word_tokenize(query)
    # 返回最相似两个问题的索引
    idx = model.get_top_similarities(query, topk=2)
    # top_1, top_2 = model.get_top_similarities(query, topk=2)
    # return questions_src[top_1], answers[top_1], questions_src[top_2], answers[top_2]
    return idx

if __name__ == '__main__':

    # 输入文本
    # query = '心脏病'
    # # 模型选择
    # # BM25
    # if args.model_type == 'bm25':
    #     bm25_model = BM25RetrievalModel(questions)
    #     res = predict(bm25_model, query)
    # # TFIDF
    # elif args.model_type == 'tfidf':
    #     tfidf_model = TFIDFRetrievalModel(questions)
    #     res = predict(tfidf_model, query)
    # # SIF
    # elif args.model_type == 'sif':
    #     # sif模型
    #     sif_model = SIFRetrievalModel(questions, args.pretrained_gensim_embddings_file,
    #                                   args.cached_gensim_embedding_file, args.embedding_dim)
    #     # 预测
    #     res = predict(sif_model, query)
    # else:
    #     raise ValueError('Invalid model type!')
    # sif模型
    sif_model = SIFRetrievalModel(questions, './cached/gensim_word_embddings.txt',args.cached_gensim_embedding_file, args.embedding_dim)
    # 预测
    # res = predict(sif_model, query)
    # # 打印
    # print('Query: ', query)
    # print('\nQuestion 1: ', questions_src[res[0]])
    # print('Answer 1: ', answers[res[0]])
    # print('\nQuestion 2: ', questions_src[res[1]])
    # print('Answer 2: ', answers[res[1]])
    while True:
        question = input("请输入梦境(q退出): ")
        if question == 'q':
            break
        time1 = time.time()
        question_k = predict(sif_model, question)
        f = "output.txt"
        print("解梦： {}".format(answers[question_k[0]]))
        with open(f, "w") as file:  # ”w"代表着每次运行都覆盖内容
            file.write(answers[question_k[0]])
        for idx in question_k:
            print("same questions： {}".format(questions_src[idx]))
        time2 = time.time()
        cost = time2 - time1
        print('Time cost: {} s'.format(cost))
