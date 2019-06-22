import json
import redis


class RedisUtils(object):

    client = None

    def __init__(self, pool):
        self.pool = pool

    def _get_str(self, _byte):
        if isinstance(_byte, bytes):
            return str(_byte, 'utf8')
        else:
            return _byte

    def get_key(self, key):
        return key

    def get_client(self):
        if RedisUtils.client is None:
            RedisUtils.client = redis.Redis(
                connection_pool=self.pool, decode_responses=True)
        return RedisUtils.client

    def exists(self, key):
        rkey = self.get_key(key)
        return self.client.exists(rkey)

    def delete(self, key):
        rkey = self.get_key(key)
        return self.client.delete(rkey)

    def set_data(self, key, data, expire_sec=None):
        rkey = self.get_key(key)
        pipe = self.client.pipeline()
        p = pipe.set(rkey, json.dumps(data))
        if expire_sec:
            p.expire(rkey, expire_sec)
        result = p.execute()
        return all(result)

    def set(self, key, text, expire_sec=None):
        rkey = self.get_key(key)
        pipe = self.client.pipeline()
        p = pipe.set(rkey, text)
        if expire_sec:
            p.expire(rkey, expire_sec)
        result = p.execute()
        return self._get_str(result[0])

    def get(self, key, expire_sec=None):
        rkey = self.get_key(key)
        pipe = self.client.pipeline()
        p = pipe.get(rkey)
        if expire_sec:
            p.expire(rkey, expire_sec)
        result = p.execute()
        return self._get_str(result[0])

    def get_data(self, key, expire_sec=None):
        rkey = self.get_key(key)
        pipe = self.client.pipeline()
        p = pipe.get(rkey)
        if expire_sec:
            p.expire(rkey, expire_sec)
        result = p.execute()
        if isinstance(result, list):
            if result[0] is None:
                return None
        return json.loads(result[0])

    def hset(self, key, field, value, expire_sec=None):
        rkey = self.get_key(key)
        pipe = self.client.pipeline()
        p = pipe.hset(rkey, field, value)
        if expire_sec:
            p.expire(rkey, expire_sec)
        result = p.execute()
        return self._get_str(result[0])

    def hmset(self, key, mapping, expire_sec=None):
        rkey = self.get_key(key)
        pipe = self.client.pipeline()
        p = pipe.hmset(rkey, mapping)
        if expire_sec:
            p.expire(rkey, expire_sec)
        result = p.execute()
        return self._get_str(result[0])

    def hgetall(self, key, expire_sec=None):
        rkey = self.get_key(key)
        pipe = self.client.pipeline()
        p = pipe.hgetall(rkey)
        if expire_sec:
            p.expire(rkey, expire_sec)
        result = p.execute()
        return self._get_str(result[0])

    def hget(self, key, field, expire_sec=None):
        rkey = self.get_key(key)
        pipe = self.client.pipeline()
        p = pipe.hget(rkey, field)
        if expire_sec:
            p.expire(rkey, expire_sec)
        result = p.execute()
        return self._get_str(result[0])

    def exist(self, key):
        rkey = self.get_key(key)
        result = self.client.exists(rkey)
        return result

    def keys(self, pattern):
        return self.client.keys(pattern)
