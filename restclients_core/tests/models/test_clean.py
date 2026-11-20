# Copyright 2026 UWIT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from unittest import TestCase

from restclients_core import models


class TestModelCleanMethods(TestCase):
    def test_date_clean(self):
        class ModelTest(models.Model):
            d1 = models.DateField()

        now = datetime.now()
        m1 = ModelTest(d1=now)

        self.assertEqual(now, m1.d1)
        m1.clean_fields()
        self.assertEqual(now.date(), m1.d1)
