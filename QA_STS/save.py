import pickle
from text2vec import SentenceModel, cos_sim, semantic_search, EncoderType

embedder = SentenceModel("shibing624/text2vec-base-chinese",
                              encoder_type=EncoderType.FIRST_LAST_AVG)

with open('model.pkl', 'wb') as f:
    pickle.dump(embedder, f)