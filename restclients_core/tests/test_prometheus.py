from restclients_core.tests.dao_implementation.test_live import TDAO
from unittest import TestCase, skipUnless
from prometheus_client import generate_latest, REGISTRY
import os


@skipUnless("RUN_LIVE_TESTS" in os.environ, "RUN_LIVE_TESTS=1 to run tests")
class TestPrometheusObservations(TestCase):
    def test_prometheus_observation(self):
        response = TDAO().getURL('/ok', {})

        metrics = generate_latest(REGISTRY).decode('utf-8')
        self.assertRegexpMatches(
            metrics,
            r'.*\nrestclient_request_duration_seconds_bucket{le="0.005",'
            r'service="backend_test"} [1-9].*', metrics)
        self.assertRegexpMatches(
            metrics,
            r'.*\nrestclient_response_status_code_bucket{le="200.0",'
            r'service="backend_test"} [1-9].*', metrics)
        self.assertIn('restclient_request_timeout_total counter', metrics)
        self.assertIn('restclient_request_ssl_error_total counter', metrics)
