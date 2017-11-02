import redis

class SymbolCache:
    def __init__(self, *args, **kwargs):
        self.cache = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set(self, symbol, record_id):
        self.cache.set(symbol, record_id)

    def get(self, document_symbol):
        return self.cache.get(document_symbol)
