import tornado
import tornado.web
# from tornado.wsgi import WSGIAdapter
from .application import CoreApplication


class MicroService(object):

    def __init__(self, name, routes, port,
                 settings, autoreload=False, debug=False, cookie_secret=None, prefix="DRAGON_"):

        self.routes = routes
        self.port = port
        self.autoreload = autoreload
        self.debug = debug
        self.settings = settings
        self.cookie_secret = cookie_secret
        self.prefix = prefix
        self.init_services()

    def getSetting(self, name):
        return getattr(self.settings, '%s%s' % (self.prefix, name))

    def init_services(self):
        self.init_logger()
        self.init_database()
        self.application = self.make_app()
        self.init_redis()

    def init_database(self):
        # init database
        from dragonlib.utils.mongo_utils import MongoConnection
        mongodb = MongoConnection(
            host=self.getSetting('MONGODB_HOST'),
            port=int(self.getSetting('MONGODB_PORT')),
            db=self.getSetting('MONGODB_DB')
        )
        mongodb.connect()


    def init_redis(self):
        import redis
        from ..utils.redis_utils import RedisUtils
        pool = redis.ConnectionPool(
            host=self.getSetting('REDIS_HOST'),
            port=int(self.getSetting('REDIS_PORT')),
            db=self.getSetting('REDIS_DB'),
            decode_responses=True
        )
        redis_service = RedisUtils(pool)
        redis_service.get_client()
        self.application.settings['redis'] = redis_service

    def init_logger(self):
        import logging
        logging.basicConfig(
            level=logging.DEBUG,
            format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
        )
        logger = logging.getLogger('umbrella_api')
        logger.setLevel(logging.DEBUG)
        self.logger = logger

    def drop_services(self):
        pass

    def make_app(self):
        if getattr(self, 'application', None):
            return self.application

        settings = {
            'autoreload': self.autoreload,
            'debug': self.debug
        }
        if self.cookie_secret:
            settings['cookie_secret'] = self.cookie_secret

        self.application = CoreApplication(self.routes, **settings)
        return self.application

    # def get_wsgi_app(self):
    #     from gevent import monkey
    #     monkey.patch_all()
    #     wsgi_app = WSGIAdapter(self.application)
    #     return wsgi_app

    def start(self):
        self.application.listen(self.port, xheaders=True)
        print('@starting development: %s' % self.port)
        tornado.ioloop.IOLoop.instance().start()
