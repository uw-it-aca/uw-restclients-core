import re
import weakref
from restclients_core.models.fields import (BooleanField, CharField, DateField,
                                            DateTimeField, DecimalField,
                                            FloatField, ForeignKey,
                                            IntegerField, NullBooleanField,
                                            PositiveIntegerField,
                                            PositiveSmallIntegerField,
                                            SlugField, SmallIntegerField,
                                            TextField, TimeField, URLField)


class MockHTTP(object):
    """
    An alternate object to HTTPResponse, for non-HTTP DAO
    implementations to use.  Implements the API of HTTPResponse
    as needed.
    """
    status = 0
    data = ""
    headers = {}

    def read(self):
        """
        Returns the document body of the request.
        """
        return self.data

    def getheader(self, field, default=''):
        """
        Returns the HTTP response header field, case insensitively
        """
        if self.headers:
            for header in self.headers:
                if field.lower() == header.lower():
                    return self.headers[header]

        return default


class Model(object):

    def __init__(self, *args, **kwargs):
        self._dynamic_fields = set()
        self._field_values = {}

        super(Model, self).__init__()

        for key in kwargs:
            setattr(self, key, kwargs[key])

    def _set_value(self, field_id, value):
        self._field_values[field_id] = value

    def _get_value(self, field_id):
        return self._field_values[field_id]

    def _delete(self, field_id):
        del(self._field_values[field_id])

    def _track_field(self, field):
        self._dynamic_fields.add(weakref.ref(field))

    def __getattribute__(self, name):
        # This is in place to catch get_<attribute>_display.  If there's
        # alrady a defined attribute here, just return it.  Otherwise if the
        # attribute name matches our pattern, and we can find that name in our
        # Class's dictionary, we try to let that field type get the right
        # value.  then we return a function that returns the value.
        try:
            base_value = super(Model, self).__getattribute__(name)
            return base_value
        except AttributeError as ex:
            base_value = None
            original_exception = ex

        match = re.match('get_(.*)_display', name)
        if match:
            try:
                field = self.__class__.__dict__[match.group(1)]

                value = field.get_display(self)
                return lambda: value

            except Exception:
                pass

        raise original_exception

    def clean_fields(self):
        for ref in self._dynamic_fields:
            field = ref()
            if field:
                field.clean(self)

        pass

PROTECT = None
