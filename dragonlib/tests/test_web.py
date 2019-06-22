import json
from unittest.mock import MagicMock
# from tornado.test.test_web import WebTestCase
from .base import BaseTest
from ..web.web import BaseAPIHandler
from ..web.errcode import ErrorCode

# class MyBaseAPIHandler(BaseAPIHandler):
#     pass


class TestWeb(BaseTest):
    

    def setUp(self):
        request = MagicMock()
        application = MagicMock()
        self.apiHandler = BaseAPIHandler(application, request)
        self.apiHandler.finish = self.fake_finish
        self.testData = {'a': 1}
        self._headers = {}
        self._status_code = 200
    
    def fake_finish(self):
        pass
    
    def fake_set_status(self, code):
        self._status_code = code
    
    def fake_set_header(self, key, value):
        self._headers[key] = value

    def test_output(self):
        self.apiHandler.output(self.testData)
        result = json.loads(self.apiHandler._chunk)
        self.assertEqual(result['a'], self.testData['a'])
    
    def test_success(self):
        success_code = ErrorCode.success
        message = 'success'
        self.apiHandler.success(message, **self.testData)
        result = json.loads(self.apiHandler._chunk)
        self.assertEqual(result['message'], message)
        self.assertEqual(result['code'], success_code)
        self.assertEqual(result['data']['a'], self.testData['a'])
    
    def test_fail(self):
        self.apiHandler.set_status = self.fake_set_status
        self.apiHandler.set_header = self.fake_set_header
        message = 'fail'
        status_code = 400
        result_data = {'test': 1000}
        self.apiHandler.fail(code='-9999', message=message, status_code=status_code, **result_data)
        result = json.loads(self.apiHandler._chunk)
        self.assertEqual(result['message'], message)
        self.assertEqual(self._status_code, status_code)
        self.assertEqual(result_data['test'], result['data']['test'])