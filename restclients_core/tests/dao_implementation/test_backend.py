from unittest import TestCase, skipUnless
from restclients_core.dao import DAO, MockDAO
from restclients_core.models import MockHTTP
from restclients_core.exceptions import ImproperlyConfigured


class TDAO(DAO):
    def service_name(self):
        return "backend_test"

    def get_default_service_setting(self, key):
        if "DAO_CLASS" == key:
            return ('restclients_core.tests.dao_implementation.'
                    'test_backend.Backend')


class E1DAO(TDAO):
    def get_default_service_setting(self, key):
        if "DAO_CLASS" == key:
            return ('restclients_core.tests.dao_implementation.'
                    'test_backendX.Backend')


class E2DAO(TDAO):
    def get_default_service_setting(self, key):
        if "DAO_CLASS" == key:
            return ('restclients_core.tests.dao_implementation.'
                    'test_backend.BackendX')


class TestBackend(TestCase):
    def test_get(self):
        response = TDAO().getURL('/ok')
        self.assertEquals(response.data, 'ok - GET')

    def test_post(self):
        response = TDAO().postURL('/ok')
        self.assertEquals(response.data, 'ok - POST')

    def test_put(self):
        response = TDAO().putURL('/ok', {}, '')
        self.assertEquals(response.data, 'ok - PUT')

    def test_delete(self):
        response = TDAO().deleteURL('/ok')
        self.assertEquals(response.data, 'ok - DELETE')

    def test_patch(self):
        response = TDAO().patchURL('/ok', {}, '')
        self.assertEquals(response.data, 'ok - PATCH')

    def test_error_level1(self):
        self.assertRaises(ImproperlyConfigured, E1DAO().getURL, '/ok')

    def test_error_level2(self):
        self.assertRaises(ImproperlyConfigured, E2DAO().getURL, '/ok')

    @skipUnless(hasattr(TestCase, 'assertLogs'), 'Python < 3.4')
    def test_log(self):
        with self.assertLogs('restclients_core.dao', level='INFO') as cm:
            response = TDAO().getURL('/ok')
            self.assertEquals(len(cm.output), 1)
            (msg, time) = cm.output[0].split(' time:')
            self.assertEquals(msg,
                              'INFO:restclients_core.dao:service:backend_test '
                              'method:GET url:/ok from_cache:no')
            self.assertGreater(float(time), 0)

        with self.assertLogs('restclients_core.dao', level='INFO') as cm:
            response = TDAO().putURL('/api', {}, '')
            self.assertEquals(len(cm.output), 1)
            (msg, time) = cm.output[0].split(' time:')
            self.assertEquals(msg,
                              'INFO:restclients_core.dao:service:backend_test '
                              'method:PUT url:/api from_cache:no')
            self.assertGreater(float(time), 0)


class Backend(MockDAO):
    def load(self,  method, url, headers, body):
        response = MockHTTP()
        response.status == 404
        response.data = "ok - %s" % method

        return response
