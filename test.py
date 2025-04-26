import pytest
from algorithms.hybrid_search import HybridSearch


def test_hybrid_search():
    corpus = ["苹果是水果", "苹果公司市值很高", "香蕉是热带水果"]
    searcher = HybridSearch(corpus)
    results = searcher.search("苹果", alpha=0.5)

    assert len(results) == 2  # 应返回两条相关文档
    assert results[0]['doc_id'] in [0, 1]  # 最相关结果


def test_cache():
    cache = SearchCache()
    cache.set("test_query", "default", [{"doc_id": 1}])
    cached = cache.get("test_query", "default")
    assert cached == [{"doc_id": 1}]