import sys
import pandas as pd
import numpy as np
import pickle

sys.path.append('..')
from text2vec import SentenceModel, cos_sim, semantic_search, EncoderType


# Corpus with example sentences
def read_corpus():
    qList = []
    # 问题的关键词列表
    qList_kw = []
    aList = []
    data = pd.read_csv('./data/data.csv', header=None)
    data_ls = np.array(data).tolist()
    for t in data_ls:
        qList.append(t[0])
        # qList_kw.append(seg.cut(t[0]))
        aList.append(t[1])
    return qList_kw, qList, aList

def retrieve(query):
    # with open('model.pkl', 'wb') as f:
    embedder = SentenceModel("shibing624/text2vec-base-chinese",
                              encoder_type=EncoderType.FIRST_LAST_AVG)
        # pickle.dump(embedder, f)
    
    _, corpus, ansList = read_corpus()
    print("finish loading corpus")
    corpus_embeddings = embedder.encode(corpus)
    # np.save('corpus_embed', corpus_embeddings)
    # corpus_embeddings = np.load('./QA_STS/corpus_embed.npy')
    print("finish loading corpus embeddings")
    # Query sentences:
    # queries = ["我梦到了有人在大声喊叫"]

    # while True:
    # query = input('请输入问题：')
    query_embedding = embedder.encode(query)
    hits = semantic_search(query_embedding, corpus_embeddings, top_k=5)
    # print("\n\n======================\n\n")
    print("Query:", query)
    print("\nTop 5 most similar sentences in corpus:")
    hits = hits[0]  # Get the hits for the first query
    re_Q = []
    highest_score = None
    flag = 0
    for hit in hits:
        re_Q.append(corpus[hit['corpus_id']] + "(Score: {:.4f})".format(hit['score']))
        if flag == 0: 
            highest_score = hit['score']
        # print(corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
    
    return re_Q, highest_score

# retrieve('你好')