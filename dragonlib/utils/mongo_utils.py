from mongoengine import connect


class MongoConnection(object):

    def __init__(self, db, host, port, authentication_source="admin", **extra):
        self.db = db
        self.host = host
        self.port = port
        self.authentication_source = authentication_source
        self.extra = extra

    def connect(self):
        connect(self.db,
                host=self.host,
                port=self.port,
                authentication_source=self.authentication_source,
                **self.extra)
