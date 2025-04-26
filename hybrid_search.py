from typing import List, Dict
from rank_bm25 import BM25Okapi
import numpy as np
from sentence_transformers import SentenceTransformer


class HybridSearch:
    def __init__(self, corpus: List[str]):
        self.corpus = corpus
        self.bm25 = BM25Okapi([doc.split() for doc in corpus])
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.embeddings = self.model.encode(corpus)

    def search(self, query: str, alpha: float = 0.5) -> List[Dict]:
        # BM25 检索
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)

        # 语义检索
        query_embedding = self.model.encode(query)
        cosine_scores = np.dot(self.embeddings, query_embedding)

        # 混合得分
        combined_scores = alpha * bm25_scores + (1 - alpha) * cosine_scores
        sorted_indices = np.argsort(combined_scores)[::-1]

        return [{
            "doc_id": idx,
            "text": self.corpus[idx],
            "score": combined_scores[idx]
        } for idx in sorted_indices[:10]]