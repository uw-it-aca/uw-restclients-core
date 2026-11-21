# Copyright 2026 UWIT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase

from restclients_core import models


class TestModelString(TestCase):
    def test_model_string(self):
        class ModelTest(models.Model):
            number = models.CharField(max_length=8)
            one = models.IntegerField()

        m = ModelTest(number="number", one=1)
        self.assertEqual(f"{m}", "number: number, one: 1")
