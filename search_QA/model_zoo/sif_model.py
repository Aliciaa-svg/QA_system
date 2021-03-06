# 成晓雪
# 创建时间：2022/3/22 19:25
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from util import get_word_embedding_matrix, save_embedding, load_embedding
import os
from sklearn.decomposition import PCA
from annoy import AnnoyIndex


class SIFRetrievalModel:
    """
    A simple but tough-to-beat baseline for sentence embedding.
    from https://openreview.net/pdf?id=SyK00v5xx
    Principle : Represent the sentence by a weighted average of the word vectors, and then modify them using Principal Component Analysis.

    Issue 1: how to deal with big input size ?
    randomized SVD version will not be affected by scale of input, see https://github.com/PrincetonML/SIF/issues/4

    Issue 2: how to preprocess input data ?
    Even if you dont remove stop words SIF will take care, but its generally better to clean the data,
    see https://github.com/PrincetonML/SIF/issues/23

    Issue 3: how to obtain the embedding of new sentence ?
    Weighted average is enough, see https://www.quora.com/What-are-some-interesting-techniques-for-learning-sentence-embeddings
    """

    def __init__(self, corpus, pretrained_embedding_file, cached_embedding_file, embedding_dim):

        self.embedding_dim = embedding_dim
        self.max_seq_len = 0
        corpus_str = []
        # 遍历语料
        for line in corpus:
            corpus_str.append(' '.join(line))
            self.max_seq_len = max(self.max_seq_len, len(line))
        # 计算词频
        counter = CountVectorizer(token_pattern=r"(?u)\b\w+\b")
        # bag of words format, i.e., [[1.0, 2.0, ...], []]
        bow = counter.fit_transform(corpus_str).todense().astype('float')
        # word count
        word_count = np.sum(bow, axis=0)
        # word frequency, i.e., p(w)
        word_freq = word_count / np.sum(word_count)

        # the parameter in the SIF weighting scheme, usually in the range [1e-5, 1e-3]
        SIF_weight = 1e-3
        # 计算词权重
        self.word2weight = np.asarray(SIF_weight / (SIF_weight + word_freq))

        # number of principal components to remove in SIF weighting scheme
        self.SIF_npc = 1
        self.word2id = counter.vocabulary_

        # 语料 word id
        seq_matrix_id = np.zeros(shape=(len(corpus_str), self.max_seq_len), dtype=np.int64)
        # 语料 word 权重
        seq_matrix_weight = np.zeros((len(corpus_str), self.max_seq_len), dtype=np.float64)

        # 依次遍历每个样本
        for idx, seq in enumerate(corpus):
            seq_id = []
            for word in seq:
                if word in self.word2id:
                    seq_id.append(self.word2id[word])

            seq_len = len(seq_id)
            seq_matrix_id[idx, :seq_len] = seq_id

            seq_weight = [self.word2weight[0][id] for id in seq_id]
            seq_matrix_weight[idx, :seq_len] = seq_weight

        # if os.path.exists(cached_embedding_file):
        #     self.word_embeddings = load_embedding(cached_embedding_file)
        # else:
        self.word_embeddings = get_word_embedding_matrix(counter.vocabulary_, pretrained_embedding_file, embedding_dim=self.embedding_dim)
            # save_embedding(self.word_embeddings, cached_embedding_file)

        # 计算句向量
        self.sentence_embeddings = self.SIF_embedding(seq_matrix_id, seq_matrix_weight)

        # build search model
        # 在向量空间中做很多超平面的划分，帮助我们做向量的检索
        self.t = AnnoyIndex(self.embedding_dim, metric='angular')
        # 将sentence_embeddings放入annoy中，建立一棵树，就可以通过annoy来进行向量的检索
        for i in range(self.sentence_embeddings.shape[0]):
            self.t.add_item(i, self.sentence_embeddings[i, :])
        self.t.build(10)

    def SIF_embedding(self, x, w):
        """句向量计算"""
        # weighted averages
        n_samples = x.shape[0]
        emb = np.zeros((n_samples, self.word_embeddings.shape[1]))
        for i in range(n_samples):
            emb[i, :] = w[i, :].dot(self.word_embeddings[x[i, :], :]) / np.count_nonzero(w[i, :])

        # removing the projection on the first principal component
        # randomized SVD version will not be affected by scale of input, see https://github.com/PrincetonML/SIF/issues/4
        #svd = TruncatedSVD(n_components=self.SIF_npc, n_iter=7, random_state=0)
        svd = PCA(n_components=self.SIF_npc, svd_solver='randomized')
        svd.fit(emb)
        self.pc = svd.components_
        #print('pc shape:', pc.shape)

        if self.SIF_npc == 1:
            # pc.transpose().shape : embedding_size * 1
            # emb.dot(pc.transpose()).shape: num_sample * 1
            # (emb.dot(pc.transpose()) * pc).shape: num_sample * embedding_size
            common_component_removal = emb - emb.dot(self.pc.transpose()) * self.pc
        else:
            # pc.shape: self.SIF_npc * embedding_size
            # emb.dot(pc.transpose()).shape: num_sample * self.SIF_npc
            # emb.dot(pc.transpose()).dot(pc).shape: num_sample * embedding_size
            common_component_removal = emb - emb.dot(self.pc.transpose()).dot(self.pc)
        # 返回SIF_embedding向量
        return common_component_removal

    def get_top_similarities(self, query, topk=10):
        """query: [word1, word2, ..., wordn]"""
        query2id = []
        for word in query:
            if word in self.word2id:
                query2id.append(self.word2id[word])
        query2id = np.array(query2id)

        id2weight = np.array([self.word2weight[0][id] for id in query2id])

        # 得到query_embedding
        query_embedding = id2weight.dot(self.word_embeddings[query2id, :]) / query2id.shape[0]
        # 返回top_ids与top_distances
        top_ids, top_distances = self.t.get_nns_by_vector(query_embedding, n=topk, include_distances=True)
        return top_ids
