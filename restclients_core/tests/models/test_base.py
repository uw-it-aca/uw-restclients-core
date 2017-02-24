from unittest import TestCase
from restclients_core import models
from datetime import datetime


class TestModelBase(TestCase):
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

        self.assertEquals(model.bools, True)
        self.assertEquals(model.chars, "Char value")
        self.assertEquals(model.dates, now.date())
        self.assertEquals(model.datetimes, now)
        self.assertEquals(model.decimals, 12.1)
        self.assertEquals(model.floats, 1.2312)
        self.assertEquals(model.ints, 21)
        self.assertEquals(model.nullbools, False)
        self.assertEquals(model.posints, 113234234)
        self.assertEquals(model.possmalls, 10)
        self.assertEquals(model.slugs, "ok")
        self.assertEquals(model.smallints, -1)
        self.assertEquals(model.texts, "text string")
        self.assertEquals(model.texts2, "making sure fields are different")
        self.assertEquals(model.times, now.time())
        self.assertEquals(model.urls, "http://example.com/path")

        del(model.urls)
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

        self.assertEquals(m1.f1, "m1_f1")
        self.assertEquals(m1.f2, "m1_f2")
        self.assertEquals(m2.f1, "m2_f1")
        self.assertEquals(m2.f2, "m2_f2")

    def test_init_fields(self):
        class ModelTest(models.Model):
            f1 = models.TextField()
            f2 = models.BooleanField()

        m1 = ModelTest(f1="Input value", f2=True)

        self.assertEquals(m1.f1, "Input value")
        self.assertEquals(m1.f2, True)

    def test_default_values(self):
        class ModelTest(models.Model):
            f1 = models.TextField(default="Has Default")
            f2 = models.TextField()

        m1 = ModelTest()
        m2 = ModelTest(f1="override")

        self.assertEquals(m1.f1, "Has Default")
        self.assertEquals(m1.f2, None)

        self.assertEquals(m2.f1, "override")
        self.assertEquals(m2.f2, None)