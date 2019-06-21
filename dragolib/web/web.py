import json
import logging
import tornado
import addict
import functools
import errcode
from json import JSONEncoder
from tornado import gen
from tornado.web import RequestHandler
from tornado.web import HTTPError
from datetime import datetime, date


logger = logging.getLogger(__name__)


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


class BaseAPIHandler(RequestHandler):
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
            'code': errcode.success,
            'message': message,
            'data': kwargs
        })

    def fail(self, code, message, status_code=200, **kwargs):
        logger.info('status_code: %s, message: %s, kwargs: %s' % (status_code, message, kwargs))
        if status_code != 200:
            self.set_status(status_code)
            self.set_header('system_error_format', 'json')
        self.output({
            'code': code,
            'message': message
        })

    def info(self, status_code=200, **kwargs):
        logger.info('status_code: %s, kwargs: %s' % (status_code, kwargs))
        self.set_status(status_code)
        self.output(kwargs)

    @staticmethod
    def gen_return(result=None):
        raise gen.Return(result)

    def log_exception(self, typ, value, tb):
        super(BaseAPIHandler, self).log_exception(typ, value, tb)
        if isinstance(value, HTTPError):
            if value.log_message:
                format = "%d %s: " + value.log_message
                args = ([value.status_code, self._request_summary()] +
                        list(value.args))
                logger.error(format, *args)
        else:
            logger.exception(
                "Uncaught exception %s\n%r",
                self._request_summary(),
                self.request,
                exc_info=(typ, value, tb))

    def parse_error_info(self, err):
        if err.args and len(err.args) >= 1:
            return '%s: %s' % (err.message, err.args[0])
        return err.message

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
            self.fail(code=errcode.system_error, message=message)
            return
        data = self.api(params)
        if not self._finished:
            self.success(**data if data else {})


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            raise HTTPError(403, reason="Unauthorized")
        return method(self, *args, **kwargs)

    return wrapper
