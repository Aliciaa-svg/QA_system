# 成晓雪
# 创建时间：2022/3/22 19:24
from gensim.summarization import bm25


class BM25RetrievalModel:
    """BM25 definition: https://en.wikipedia.org/wiki/Okapi_BM25"""
    def __init__(self, corpus):
        self.model = bm25.BM25(corpus)

    def get_top_similarities(self, query, topk=10):
        """query: [word1, word2, ..., wordn]"""
        # 得到query与每个文档的分数
        scores = self.model.get_scores(query)
        # 基于score进行排序
        rtn = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:topk]
        # 得到文档索引与分数
        return rtn[0][0], rtn[1][0]
