import json
import tornado
import addict
from tornado.testing import AsyncHTTPTestCase


class TestBase(AsyncHTTPTestCase):
    def setUp(self):
        super(TestBase, self).setUp()
        # self.drop_table()

    def tearDown(self):
        # self.drop_table()
        super(TestBase, self).tearDown()

    def drop_table(self, table_name):
        sql = "truncate table `%s`" % table_name
        self._db._exec_sql(sql)

    def get_app(self):
        raise Exception('__must_return_application_object')

    def get_new_ioloop(self):
        return tornado.ioloop.IOLoop.instance()

    def assemble_body(self, data):
        return json.dumps(data) if data else None

    def _test_response(self,
                       response,
                       http_code=200,
                       code=None,
                       message=None,
                       data=None):
        """ basic test for response.
        """
        # Check HTTP Status code
        self.assertEqual(response.code, http_code)
        body = response.body.decode('utf8')
        try:
            body = json.loads(body)
        except Exception as e:
            print('error when load json body: %s' % e)
            return body

        if code is not None:
            print('message: %s' % body.get('message'))
            self.assertEqual(body.get('code'), code)

        if message is not None:
            self.assertEqual(body.get('message'), message)

        if data:
            for item in data:
                self.assertIn(item, body['data'])

        if body.get('data'):
            return addict.Dict(body['data'])
        else:
            return body

    def _test_request(self, path, method="POST", headers={}, body={},
                      **kwargs):
        response = self.fetch(
            path,
            method=method,
            headers=headers,
            body=self.assemble_body(body),
            allow_nonstandard_methods=True)
        return self._test_response(response, **kwargs)

    def _raw_request(self, path, method="POST", headers={}, body='', **kwargs):
        response = self.fetch(
            path,
            method=method,
            headers=headers,
            body=body,
            allow_nonstandard_methods=True)
        return self._test_response(response, **kwargs)

    def _test_record_created(self, model_cls, **kwargs):
        record = model_cls.get(**kwargs)
        self.assertNotEqual(record, None)
        return record

    def _create_record(self, model_cls, **kwargs):
        record = model_cls(**kwargs)
        return record
