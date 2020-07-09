import logging
logger = logging.getLogger(__name__)

class MongoConnection(object):

    def __init__(self, config):
        self.config = config

    def initdb(self):
        from mongoengine import connect
        dbs = {}
        for dbname, conn_config in self.config.items():
            alias = conn_config['alias']
            host = conn_config['host']
            logger.info('Connect to mongodb %s, %s' % (dbname, alias))
            dbs[alias] = connect(alias=alias, host=host, db=alias)
        return dbs
