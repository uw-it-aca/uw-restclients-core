# Copyright 2026 UWIT, University of Washington
# SPDX-License-Identifier: Apache-2.0


class NoCache:
    """
    A cache implementation that never caches.
    """
    def getCache(self, service, url, headers):
        return None

    def processResponse(self, service, url, response):
        pass

    def deleteCache(self, service, url):
        return None
