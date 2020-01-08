from restclients_core.tests.dao_implementation.test_backend import TDAO
from unittest import TestCase
from prometheus_client import generate_latest, REGISTRY


class TestPrometheusObservations(TestCase):

    def test_prometheus_observation(self):
        response = TDAO().getURL('/ok')
        metrics = generate_latest(REGISTRY).decode('utf-8')
        self.assertIn('restclient_request_duration_seconds_bucket{le="0.005",'
                      'service="backend_test"} 9.0', metrics)
        self.assertIn('restclient_response_status_code_bucket{le="200.0",'
                      'service="backend_test"} 9.0', metrics)
