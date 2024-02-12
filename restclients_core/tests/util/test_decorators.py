# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from commonconf import settings
from restclients_core.dao import DAO
from restclients_core.util.decorators import use_mock


class TDAO1(DAO):
    def service_name(self):
        return 'td1'


class TDAO2(DAO):
    def service_name(self):
        return 'td2'


class TestMockOverride(TestCase):
    def test_multi_service(self):
        self.assertEqual(getattr(settings, "RESTCLIENTS_TD1_DAO_CLASS", None),
                         None)

        with use_mock(TDAO1(), TDAO2()):
            self.assertEqual(settings.RESTCLIENTS_TD1_DAO_CLASS, 'Mock')
            self.assertEqual(settings.RESTCLIENTS_TD2_DAO_CLASS, 'Mock')

        self.assertEqual(getattr(settings, "RESTCLIENTS_TD1_DAO_CLASS", None),
                         None)
