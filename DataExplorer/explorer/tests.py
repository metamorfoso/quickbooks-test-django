from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class ReadTestCase(TestCase):
    def test_read_responds_200(self):
        client = Client()
        response = client.get(reverse('explorer:read'))
        self.assertEqual(response.status_code, 200)

    def test_read_get_data(self):
        client = Client()
        dummy_data = {'entity': 'Account', 'entity_id': '33'}
        response = client.get(
            reverse('explorer:read'),
            data=dummy_data
        )
        # TODO: complete this test method

# TODO: Write tests for views that connect to the QBO API
