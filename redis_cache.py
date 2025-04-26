import redis
import hashlib
import json


class SearchCache:
    def __init__(self, host='localhost', port=6379, ttl=600):
        self.redis = redis.Redis(host=host, port=port)
        self.ttl = ttl  # 缓存有效期（秒）

    def _generate_key(self, query: str, knowledge_base: str) -> str:
        return hashlib.sha256(f"{query}_{knowledge_base}".encode()).hexdigest()

    def get(self, query: str, knowledge_base: str) -> List[Dict]:
        key = self._generate_key(query, knowledge_base)
        cached = self.redis.get(key)
        return json.loads(cached) if cached else None

    def set(self, query: str, knowledge_base: str, results: List[Dict]):
        key = self._generate_key(query, knowledge_base)
        self.redis.setex(key, self.ttl, json.dumps(results))