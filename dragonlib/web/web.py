import json
import logging
import tornado
import addict
import functools
from .errcode import ErrorCode
from json import JSONEncoder
from tornado import gen
from tornado.web import RequestHandler
from tornado.web import HTTPError
from datetime import datetime, date


logger = logging.getLogger(__name__)


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            self.fail(code=ErrorCode.unauthorized, message='session_required')
        return method(self, *args, **kwargs)
    return wrapper


class ApiJsonEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            iterable = iter(obj)
        except TypeError as e:
            logger.warn(e)
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


class APIError(Exception):
    code = '-10000'


class BaseMixin(object):

    def dumpjson(self, response):
        return json.dumps(response, cls=ApiJsonEncoder)

    def output(self, response, **kwargs):
        self._chunk = self.dumpjson(response)
        if not kwargs.get('content_type'):
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(self._chunk)
        self.finish()

    def success(self, message='ok', **kwargs):
        self.output({
            'code': ErrorCode.success,
            'message': message,
            'cnmsg': self.LANGUAGE_MAP['zh-CN'].get('message', '未知'),
            'enmsg': self.LANGUAGE_MAP['en-US'].get('message', 'UNKNOWN'),
            'data': kwargs
        })


class BaseAPIHandler(RequestHandler, BaseMixin):

    ERR_PREFIX = None
    LANGUAGE_MAP = {}

    def fail(self, code, message, status_code=200, **kwargs):
        logger.info('status_code: %s, message: %s, kwargs: %s' % (status_code, message, kwargs))
        if status_code != 200:
            self.set_status(status_code)
            self.set_header('system_error_format', 'json')
        
        errcode = code
        if getattr(self, 'ERR_PREFIX', None):
            errcode = self.ERR_PREFIX + errcode

        self.output({
            'code': errcode,
            'message': message,
            'cnmsg': self.LANGUAGE_MAP['zh-CN'].get('message', '未知错误'),
            'enmsg': self.LANGUAGE_MAP['en-US'].get('message', 'UNKNOWN_ERROR'),
            'data': kwargs
        })

    def info(self, status_code=200, **kwargs):
        logger.info('status_code: %s, kwargs: %s' % (status_code, kwargs))
        self.set_status(status_code)
        self.output(kwargs)

    def get_current_user(self):
        userid = self.request.headers.get('userid')
        if not userid:
            return

        return userid

    @property
    def userid(self):
        return self.current_user


class APIHandler(BaseAPIHandler):

    def api(self, params):
        return {}

    def parse_params(self):
        return addict.Dict(tornado.escape.json_decode(
            self.request.body)) if self.request.body else {}

    def validate_params(self, params):
        '''
        params validate success return True value jump to finish
        else return None
        '''
        return True, ''

    def post(self):
        params = self.parse_params()
        result, message = self.validate_params(params)
        if result is False:
            self.fail(code=ErrorCode.system_error, message=message)
            return
        data = self.api(params)
        if not self._finished:
            self.success(**data if data else {})


class SessionAPI(APIHandler):

    @authenticated
    def post(self, *args, **kwargs):
        if self._finished:
            return
        super(SessionAPI, self).post(*args, **kwargs)

