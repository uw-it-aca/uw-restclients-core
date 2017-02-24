class BaseField(object):
    default = None

    def __init__(self, *args, **kwargs):
        self.values = {}
        self.dynamics = set()

        if "default" in kwargs:
            self.default = kwargs["default"]

        super(BaseField, self).__init__()

    def __get__(self, instance, owner):
        key = self._key_for_instance(instance)
        set_value = self.values.get(key, None)

        if set_value is None:
            return self.default
        return set_value

    def __set__(self, instance, value):
        key = self._key_for_instance(instance)

        if key not in self.dynamics:
            instance._dynamic_fields.append(self)
            self.dynamics.add(key)

        self.values[key] = value

    def __delete__(self, instance):
        key = self._key_for_instance(instance)
        if key in self.dynamics:
            self.dynamics.remove(key)
        del self.values[key]

    def _key_for_instance(self, instance):
        return id(instance)

    def clean(self, instance):
        pass


class CharField(BaseField):
    def __init__(self, *args, **kwargs):
        self.default = u""
        super(CharField, self).__init__(*args, **kwargs)


class BooleanField(BaseField):
    pass


class DateField(BaseField):
    pass


class DateTimeField(BaseField):
    pass


class DecimalField(BaseField):
    pass


class FloatField(BaseField):
    pass


class IntegerField(BaseField):
    pass


class NullBooleanField(BaseField):
    pass


class PositiveIntegerField(BaseField):
    pass


class PositiveSmallIntegerField(BaseField):
    pass


class SlugField(BaseField):
    pass


class SmallIntegerField(BaseField):
    pass


class TextField(BaseField):
    pass


class TimeField(BaseField):
    pass


class URLField(BaseField):
    pass


class ForeignKey(BaseField):
    pass