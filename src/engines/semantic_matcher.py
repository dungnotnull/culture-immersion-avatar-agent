from sentence_transformers import SentenceTransformer, util
import torch

class SemanticMatcher:
    def __init__(self, model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)

    def is_similar(self, term1: str, term2: str, threshold=0.85):
        emb1 = self.model.encode(term1, convert_to_tensor=True)
        emb2 = self.model.encode(term2, convert_to_tensor=True)
        cosine_score = util.cos_sim(emb1, emb2)
        return cosine_score.item() > threshold
