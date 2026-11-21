# Copyright 2026 UWIT, University of Washington
# SPDX-License-Identifier: Apache-2.0


class ImproperlyConfigured(Exception):
    """Required setting is missing"""


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
        return (
            f"Error fetching {self.url}.  Status code: {self.status}.  Message: {self.msg}.")


class InvalidRegID(Exception):
    """Exception for invalid regid."""


class InvalidNetID(Exception):
    """Exception for invalid netid."""


class InvalidEmployeeID(Exception):
    """Exception for invalid employee id."""
