# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from restclients_core import models
from datetime import datetime
import gc


class TestModelBase(TestCase):
    def test_override_init(self):
        class ModelTest(models.Model):
            bools = models.BooleanField()

            def __init__(self, *args, **kwargs):
                pass

        model = ModelTest()
        model.bools = True
        self.assertTrue(model.bools)

    def test_field_types(self):
        class ModelTest(models.Model):
            bools = models.BooleanField()
            chars = models.CharField(max_length=20)
            dates = models.DateField()
            datetimes = models.DateTimeField()
            decimals = models.DecimalField()
            floats = models.FloatField()
            ints = models.IntegerField()
            nullbools = models.NullBooleanField()
            posints = models.PositiveIntegerField()
            possmalls = models.PositiveSmallIntegerField()
            slugs = models.SlugField()
            smallints = models.SmallIntegerField()
            texts = models.TextField()
            texts2 = models.TextField()
            times = models.TimeField()
            urls = models.URLField()

        model = ModelTest()

        now = datetime.now()

        model.bools = True
        model.chars = "Char value"
        model.dates = now.date()
        model.datetimes = now
        model.decimals = 12.1
        model.floats = 1.2312
        model.ints = 21
        model.nullbools = False
        model.posints = 113234234
        model.possmalls = 10
        model.slugs = "ok"
        model.smallints = -1
        model.texts = "text string"
        model.texts2 = "making sure fields are different"
        model.times = now.time()
        model.urls = "http://example.com/path"

        self.assertEqual(model.bools, True)
        self.assertEqual(model.chars, "Char value")
        self.assertEqual(model.dates, now.date())
        self.assertEqual(model.datetimes, now)
        self.assertEqual(model.decimals, 12.1)
        self.assertEqual(model.floats, 1.2312)
        self.assertEqual(model.ints, 21)
        self.assertEqual(model.nullbools, False)
        self.assertEqual(model.posints, 113234234)
        self.assertEqual(model.possmalls, 10)
        self.assertEqual(model.slugs, "ok")
        self.assertEqual(model.smallints, -1)
        self.assertEqual(model.texts, "text string")
        self.assertEqual(model.texts2, "making sure fields are different")
        self.assertEqual(model.times, now.time())
        self.assertEqual(model.urls, "http://example.com/path")

        del (model.urls)
        self.assertIsNone(model.urls)

    def test_2_fields_2_instances(self):
        class ModelTest(models.Model):
            f1 = models.TextField()
            f2 = models.TextField()

        m1 = ModelTest()
        m2 = ModelTest()

        m1.f1 = "m1_f1"
        m1.f2 = "m1_f2"
        m2.f1 = "m2_f1"
        m2.f2 = "m2_f2"

        self.assertEqual(m1.f1, "m1_f1")
        self.assertEqual(m1.f2, "m1_f2")
        self.assertEqual(m2.f1, "m2_f1")
        self.assertEqual(m2.f2, "m2_f2")

    def test_init_fields(self):
        class ModelTest(models.Model):
            f1 = models.TextField()
            f2 = models.BooleanField()

        m1 = ModelTest(f1="Input value", f2=True)

        self.assertEqual(m1.f1, "Input value")
        self.assertEqual(m1.f2, True)

    def test_default_values(self):
        class ModelTest(models.Model):
            f1 = models.TextField(default="Has Default")
            f2 = models.TextField()

        m1 = ModelTest()
        m2 = ModelTest(f1="override")

        self.assertEqual(m1.f1, "Has Default")
        self.assertEqual(m1.f2, None)

        self.assertEqual(m2.f1, "override")
        self.assertEqual(m2.f2, None)

    def test_char_choices(self):
        CHOICES = (('ok', 'OK!'), ('not_ok', 'Not OK!'))

        class ModelTest(models.Model):
            f1 = models.CharField(default='ok', choices=CHOICES)
            f2 = models.CharField(default='ok2')

        m1 = ModelTest()
        self.assertEqual(m1.f1, 'ok')
        self.assertEqual(m1.get_f1_display(), 'OK!')

        m1.f1 = 'not_ok'
        self.assertEqual(m1.f1, 'not_ok')
        self.assertEqual(m1.get_f1_display(), 'Not OK!')

        with self.assertRaises(AttributeError):
            m1.get_f2_display()

    def test_memory_leak(self):
        class MemTest2(models.Model):
            pass

        class MemTest(models.Model):
            mt0 = models.ForeignKey(MemTest2)

        def build():
            m = MemTest()
            m.mt0 = MemTest2()
            m.mt0.x = m

        def match_count():
            count = 0
            for obj in gc.get_objects():
                obj_str = repr(obj)
                if obj_str.find('restclients_core.models.fields') >= 0:
                    count += 1
            return count

        build()
        gc.collect()
        starting = match_count()

        build()
        gc.collect()
        after_2 = match_count()

        self.assertEqual(starting, after_2)
