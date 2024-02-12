# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from threading import current_thread
from restclients_core.models import MockHTTP
import time


class PerformanceDegradation(object):
    _problem_data = {}
    problems = None

    @classmethod
    def set_problems(obj, problems):
        thread = current_thread()
        PerformanceDegradation._problem_data[thread] = problems

    @classmethod
    def clear_problems(obj):
        thread = current_thread()
        PerformanceDegradation._problem_data[thread] = None

    @classmethod
    def get_problems(obj):
        thread = current_thread()

        if thread in PerformanceDegradation._problem_data:
            return PerformanceDegradation._problem_data[thread]

        if hasattr(thread, 'parent'):
            thread = thread.parent
            if thread in PerformanceDegradation._problem_data:
                return PerformanceDegradation._problem_data[thread]

        return None

    @classmethod
    def get_response(obj, service, url):
        problems = PerformanceDegradation.get_problems()
        if not problems:
            return

        delay = problems.get_load_time(service)
        if delay:
            time.sleep(float(delay))

        status = problems.get_status(service)
        content = problems.get_content(service)

        if content and not status:
            status = 200

        if status:
            response = MockHTTP()
            response.status = int(status)

            if content:
                response.data = content

            return response

        return None
