import uuid

class SessionUtils(object):
    def __init__(self, _redis_service, prefix, expire_sec=7 * 24 * 3600):
        self.prefix = prefix
        self.expire_sec = expire_sec
        self.redis_service = _redis_service

    def get_key(self, userid, sid):
        return "%s:%s@%s" % (self.prefix, str(userid), sid)

    def signin(self, userid, data):
        sid = uuid.uuid4().hex
        key = self.get_key(userid, sid)
        self.redis_service.set_data(key, data, self.expire_sec)
        return sid

    def signout(self, userid, sid):
        key = self.get_key(userid, sid)
        self.redis_service.delete(key)

    def get_session(self, userid, sid):
        key = self.get_key(userid, sid)
        data = self.redis_service.get_data(key)
        return data

    def update_session(self, userid, sid, data, expire_sec=None):
        key = self.get_key(userid, sid)
        old_data = self.redis_service.get_data(key)
        old_data.update(**data)
        self.redis_service.set_data(key, old_data, self.expire_sec)
