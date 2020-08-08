from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
ANALYZE_URL = reverse('analyze:analyze')


class AnalyzeApiTest(TestCase):
    """Test the Analyze API"""

    def set_up(self):
        self.client = APIClient()

    def with_out_space(self, response):
        """Common function for checking response of
        same string without space and upper/lower case"""
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = {
            "textLength":
                {
                    "withSpaces": 11,
                    "withoutSpaces": 11
                },
            "wordCount": 1,
            "characterCount": [
                {"e": 2},
                {"h": 1},
                {"i": 1},
                {"l": 2},
                {"m": 1},
                {"o": 1},
                {"s": 1},
                {"t": 1}]
        }

        self.assertEqual(expected_response, response.data)

    def test_payload_list(self):
        """1. Payload is array, api returns 400"""
        payload = []
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_payload_set(self):
        """2. Payload is set, api returns 400"""
        payload = set()
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_payload_tuple(self):
        """3. Payload is tuple type, api returns 400"""
        payload = ()
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_payload_lack_text_key(self):
        """4. Payload in dict, but lacks 'text' key in it, api returns 400"""
        payload = {'not-text': 'lorem ipsum'}
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('text', response.data.keys())
        self.assertEqual(response.data['text'][0], 'This field is required.')

    def test_payload_has_one_extra_key(self):
        """5. Payload has one extra key, api returns 400"""
        payload = {'text': "abc", "extra": "value"}
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data.keys())
        self.assertEqual(response.data['non_field_errors'][0],
                         'Unknown field(s): extra')

    def test_payload_has_two_extra_key(self):
        """6. Payload has two extra key, api returns 400"""
        payload = {'text': "abc", "extra1": "value", "extra2": "value2"}
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data.keys())
        self.assertEqual(response.data['non_field_errors'][0],
                         'Unknown field(s): extra1, extra2')

    def test_text_key_value_not_string(self):
        """7. Payload key 'text' value not string, api returns 400"""
        payload = {'text': {}}
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('text', response.data.keys())
        self.assertEqual(response.data['text'][0], 'Not a valid string.')

    def test_text_key_value_empty_string(self):
        """8. Payload key 'text' value empty string, api returns 400"""
        payload = {'text': ""}
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('text', response.data.keys())
        self.assertEqual(response.data['text'][0],
                         'This field may not be blank.')

    def test_analyze_payload_one_number(self):
        """9. Payload key 'text' has value number without space,
        api returns 200 with valid response"""
        payload = {'text': 2}
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = {
            "textLength": {
                "withSpaces": 1,
                "withoutSpaces": 1,
            },
            "wordCount": 1,
            "characterCount": [],
        }

        self.assertEqual(expected_response, response.data)

    def test_analyze_payload_two_numbers(self):
        """10. Payload ket 'text' has value 2 numbers,
        api returns 200 with valid response"""
        payload = {'text': 20}
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = {
            "textLength": {
                "withSpaces": 2,
                "withoutSpaces": 2,
            },
            "wordCount": 1,
            "characterCount": [],
        }

        self.assertEqual(expected_response, response.data)

    def test_analyze_payload_with_dream_broker_input(self):
        """11. Payload ket 'text' has value like dream broker,
        api returns 200 with valid response"""
        payload = {'text': "hello 2 times  "}
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = {
            "textLength":
                {
                    "withSpaces": 15,
                    "withoutSpaces": 11
                },
                "wordCount": 3,
                "characterCount": [
                    {"e": 2},
                    {"h": 1},
                    {"i": 1},
                    {"l": 2},
                    {"m": 1},
                    {"o": 1},
                    {"s": 1},
                    {"t": 1}]
        }

        self.assertEqual(expected_response, response.data)

    def test_analyze_payload_without_space(self):
        """12. Payload ket 'text' has value without space,
        api returns 200 with valid response"""
        payload = {'text': "hello2times"}
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.with_out_space(response=response)

    def test_analyze_payload_with_upper_and_lower_alphabet(self):
        """13. Payload ket 'text' has value both upper and lower alphabet,
        api returns 200 with valid response"""
        payload = {'text': "hElLo2times"}
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.with_out_space(response=response)

    def test_text_key_value_space_string(self):
        """14. Payload key 'text' value string with only space,
        api returns 200"""
        payload = {'text': "  "}
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = {
            "textLength":
                {
                    "withSpaces": 2,
                    "withoutSpaces": 0
                },
            "wordCount": 0,
            "characterCount": []
        }

        self.assertEqual(expected_response, response.data)

    def test_text_key_value_with_spacial_character(self):
        """15. Payload key 'text' value string with special character,
        api returns 200"""
        payload = {'text': "#& special character #%"}
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_response = {
            "textLength":
                {
                    "withSpaces": 23,
                    "withoutSpaces": 20
                },
            "wordCount": 4,
            "characterCount": [
                {'a': 3},
                {'c': 3},
                {'e': 2},
                {'h': 1},
                {'i': 1},
                {'l': 1},
                {'p': 1},
                {'r': 2},
                {'s': 1},
                {'t': 1}]
        }

        self.assertEqual(expected_response, response.data)

    def test_text_key_value_spacial_character(self):
        """16. Payload key 'text' value string only special character,
        api returns 200"""
        payload = {'text': "#&/?"}
        response = self.client.post(ANALYZE_URL, data=payload, format='json',
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_response = {
            "textLength":
                {
                    "withSpaces": 4,
                    "withoutSpaces": 4
                },
            "wordCount": 1,
            "characterCount": []
        }

        self.assertEqual(expected_response, response.data)
