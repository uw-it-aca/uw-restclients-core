class ImproperlyConfigured(Exception):
    """Required setting is missing"""
    pass


class DataFailureException(Exception):
    """
    This exception means there was an error fetching content
    in one of the rest clients.  You can get the url that failed
    with .url, the status of the error with .status, and any
    message with .msg
    """
    def __init__(self, url, status, msg):
        self.url = url
        self.status = status
        self.msg = msg

    def __str__(self):
        return ("Error fetching %s.  Status code: %s.  Message: %s." %
                (self.url, self.status, self.msg))


class InvalidRegID(Exception):
    """Exception for invalid regid."""
    pass


class InvalidNetID(Exception):
    """Exception for invalid netid."""
    pass


class InvalidEmployeeID(Exception):
    """Exception for invalid employee id."""
    pass
