import json
from datetime import datetime
from unittest.mock import MagicMock
from .base import BaseTest
from ..web.web import APIHandler
from ..web.web import SessionAPI
from ..web.web import ApiJsonEncoder
from ..web.errcode import ErrorCode


class TestWeb(BaseTest):
    

    def setUp(self):
        self.request = MagicMock()
        self.application = MagicMock()
        self.apiHandler = APIHandler(self.application, self.request)
        self.sessionAPI = SessionAPI(self.application, self.request)
        self.apiHandler.finish = self.fake_finish
        self.sessionAPI.finish = self.fake_finish
        self.testData = {'a': 1}
        self._headers = {}
        self._status_code = 200
        self.message_validate_params_fail = 'fake_validate_params'
    
    def fake_finish(self):
        self.sessionAPI._finished = True
        self.apiHandler._finished = True
    
    def fake_set_status(self, code):
        self._status_code = code
    
    def fake_set_header(self, key, value):
        self._headers[key] = value

    def fake_validate_params(self, params):
        return False, 'fake_validate_params'

    def test_output(self):
        self.apiHandler.output(self.testData)
        result = json.loads(self.apiHandler._chunk)
        self.assertEqual(result['a'], self.testData['a'])

    def api(self, params):
        return self.testData

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
    
    def test_info(self):
        message = 'info'
        status_code = 400
        self.apiHandler.set_status = self.fake_set_status
        self.apiHandler.info(message=message, status_code=status_code, **self.testData)
        result = json.loads(self.apiHandler._chunk)
        self.assertEqual(result['message'], message)
        self.assertEqual(self._status_code, status_code)
        self.assertEqual(self.testData['a'], result['a'])
    
    def test_post(self):
        self.request.body = json.dumps(self.testData)
        self.apiHandler.api = self.api
        self.apiHandler.post()
        result = json.loads(self.apiHandler._chunk)
        self.assertEqual(result['message'], 'ok')
    
    def test_post_fail(self):
        self.request.body = json.dumps(self.testData)
        self.apiHandler.validate_params = self.fake_validate_params
        self.apiHandler.api = self.api
        self.apiHandler.post()
        result = json.loads(self.apiHandler._chunk)
        self.assertEqual(self.message_validate_params_fail, result['message'])

    def test_userid(self):
        self.request.headers = {'userid': '1'}
        self.assertEqual(self.apiHandler.userid, self.request.headers['userid'])

    def test_no_userid(self):
        self.request.headers = {'user': '1'}
        self.assertEqual(self.apiHandler.userid, None)
    
    def test_api(self):
        self.assertTrue(isinstance(self.apiHandler.api(self.testData), dict))

    def test_session_api_unauthorized(self):
        self.request.body = json.dumps(self.testData)
        self.sessionAPI.api = self.api
        self.sessionAPI.current_user = None
        self.sessionAPI.post()
        result = json.loads(self.sessionAPI._chunk)
        self.assertEqual(result['code'], ErrorCode.unauthorized)

    def test_session_api(self):
        self.request.body = json.dumps(self.testData)
        self.sessionAPI.api = self.api
        self.sessionAPI.current_user = {'name': 'zhou'}
        self.sessionAPI.post()
        result = json.loads(self.sessionAPI._chunk)
        self.assertEqual(result['code'], '0')
    
    def test_apiJsonEncoder(self):
        now = datetime.now()
        encoder = ApiJsonEncoder()
        s = encoder.default(now)
        self.assertIsInstance(s, str)

        today = now.date()
        s = encoder.default(today)
        self.assertIsInstance(s, str)

        today = now.date()
        s = encoder.default([])
        self.assertIsInstance(s, list)

        a = object()
        
        try:
            s = encoder.default(a)
        except Exception as e:
            self.assertIsInstance(e, TypeError)