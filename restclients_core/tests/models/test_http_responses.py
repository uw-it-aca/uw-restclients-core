# Copyright 2026 UWIT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase

from restclients_core.models import CacheHTTP


class TestCacheHTTP(TestCase):

    def test_cache_http(self):
        obj = CacheHTTP()

        obj.cache_class = self.__class__
        self.assertEqual(obj.get_cache_class(), self.__class__)


class SubClassTest(TestCacheHTTP):

    def test_cache_http(self):
        obj = CacheHTTP()

        obj.cache_class = self.__class__
        self.assertEqual(obj.get_cache_class(), SubClassTest)
