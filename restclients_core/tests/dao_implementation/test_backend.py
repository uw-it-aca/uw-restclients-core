# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase, skipUnless
from commonconf import override_settings
from restclients_core.dao import DAO, MockDAO
from restclients_core.cache import NoCache
from restclients_core.models import MockHTTP, CacheHTTP
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


class TCache():
    def getCache(self, service, url, headers):
        if url == '/ok':
            response = CacheHTTP()
            response.cache_class = self.__class__
            response.status = 200
            response.data = 'ok - GET'
            return {'response': response}

    def processResponse(self, service, url, response):
        response.status = 404
        response.cache_class = self.__class__
        return {'response': response}


class TestBackend(TestCase):
    def setUp(self):
        DAO._cache_instance = None

    def test_get(self):
        response = TDAO().getURL('/ok')
        self.assertEqual(response.data, 'ok - GET')

    def test_post(self):
        response = TDAO().postURL('/ok')
        self.assertEqual(response.data, 'ok - POST')

    def test_put(self):
        response = TDAO().putURL('/ok', {}, '')
        self.assertEqual(response.data, 'ok - PUT')

    def test_delete(self):
        response = TDAO().deleteURL('/ok')
        self.assertEqual(response.data, 'ok - DELETE')

    def test_patch(self):
        response = TDAO().patchURL('/ok', {}, '')
        self.assertEqual(response.data, 'ok - PATCH')

    def test_error_level1(self):
        self.assertRaises(ImproperlyConfigured, E1DAO().getURL, '/ok')

    def test_error_level2(self):
        self.assertRaises(ImproperlyConfigured, E2DAO().getURL, '/ok')

    @override_settings(RESTCLIENTS_BACKEND_TEST_FOO=True,
                       RESTCLIENTS_FOO=False,
                       RESTCLIENTS_BAR=True)
    def test_service_settings(self):
        dao = TDAO()
        self.assertEqual(dao.get_setting('FOO'), False)
        self.assertEqual(dao.get_setting('BAR'), True)

        self.assertEqual(dao.get_service_setting('FOO'), True)
        self.assertEqual(dao.get_service_setting('BAR'), True)

    @skipUnless(hasattr(TestCase, 'assertLogs'), 'Python < 3.4')
    @override_settings(RESTCLIENTS_TIMING_LOG_ENABLED=True,
                       RESTCLIENTS_TIMING_LOG_RATE=1.0)
    def test_log(self):
        with self.assertLogs('restclients_core.dao', level='INFO') as cm:
            response = TDAO().getURL('/ok')
            self.assertEqual(len(cm.output), 1)
            (msg, time) = cm.output[0].split(' time:')
            self.assertEqual(msg,
                             'INFO:restclients_core.dao:service:backend_test '
                             'method:GET url:/ok status:200 from_cache:no'
                             ' cache_class:None')
            self.assertGreater(float(time), 0)

        with self.assertLogs('restclients_core.dao', level='INFO') as cm:
            response = TDAO().putURL('/api', {}, '')
            self.assertEqual(len(cm.output), 1)
            (msg, time) = cm.output[0].split(' time:')
            self.assertEqual(msg,
                             'INFO:restclients_core.dao:service:backend_test '
                             'method:PUT url:/api status:200 from_cache:no'
                             ' cache_class:None')
            self.assertGreater(float(time), 0)

    @skipUnless(hasattr(TestCase, 'assertLogs'), 'Python < 3.4')
    @override_settings(RESTCLIENTS_TIMING_LOG_ENABLED=True,
                       RESTCLIENTS_TIMING_LOG_RATE=1.0,
                       RESTCLIENTS_DAO_CACHE_CLASS=(
                           'restclients_core.tests.dao_implementation.'
                           'test_backend.TCache'))
    def test_log_cache(self):
        # Cached response
        with self.assertLogs('restclients_core.dao', level='INFO') as cm:
            response = TDAO().getURL('/ok')
            self.assertEqual(len(cm.output), 1)
            (msg, time) = cm.output[0].split(' time:')
            self.assertEqual(msg,
                             'INFO:restclients_core.dao:service:backend_test '
                             'method:GET url:/ok status:200 from_cache:yes'
                             ' cache_class:TCache')
            self.assertGreater(float(time), 0)

        # Cached post response
        with self.assertLogs('restclients_core.dao', level='INFO') as cm:
            response = TDAO().getURL('/ok2')
            self.assertEqual(len(cm.output), 1)
            (msg, time) = cm.output[0].split(' time:')
            self.assertEqual(msg,
                             'INFO:restclients_core.dao:service:backend_test '
                             'method:GET url:/ok2 status:404 from_cache:yes'
                             ' cache_class:TCache')
            self.assertGreater(float(time), 0)

    @override_settings(RESTCLIENTS_DAO_CACHE_CLASS=(
                           'restclients_core.tests.dao_implementation.'
                           'test_backend.TCache'))
    def test_cache_backend(self):
        cache1 = TDAO().get_cache()
        cache2 = TDAO().get_cache()
        self.assertTrue(cache1 == cache2, 'Cache objects are same instance')

        cache3 = E1DAO().get_cache()
        self.assertTrue(cache1 == cache3, 'Cache objects are same instance')

        cache4 = E2DAO().get_cache()
        self.assertTrue(cache1 == cache4, 'Cache objects are same instance')


class Backend(MockDAO):
    def load(self, method, url, headers, body):
        response = MockHTTP()
        response.status = 200
        response.data = "ok - {}".format(method)
        return response
