# Copyright 2026 UWIT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from threading import current_thread
from unittest import TestCase

from restclients_core.util.local_cache import (
    LOCAL_CACHE,
    get_cache_value,
    local_cache,
    set_cache_value,
)


class TestCache(TestCase):
    def test_context(self):
        thread = current_thread()
        with local_cache():
            test_method1("init")

            self.assertTrue(thread in LOCAL_CACHE)
            v2 = test_method1("nope, old cached value")
            self.assertEqual(v2, "init")

        self.assertFalse(thread in LOCAL_CACHE)

    def test_decorator(self):
        thread = current_thread()

        @local_cache()
        def use_the_cache():
            test_method1("init decorator")

            self.assertTrue(thread in LOCAL_CACHE)
            v2 = test_method1("nope, old cached value")
            self.assertEqual(v2, "init decorator")

        use_the_cache()
        self.assertFalse(thread in LOCAL_CACHE)

    def test_no_cache(self):
        v1 = test_method1("init none")
        self.assertEqual(v1, "init none")

        v2 = test_method1("second, none")
        self.assertEqual(v2, "second, none")


def test_method1(val):
    key = "test_method1_key"
    value = get_cache_value(key)
    if value:
        return value

    set_cache_value(key, val)
    return val
