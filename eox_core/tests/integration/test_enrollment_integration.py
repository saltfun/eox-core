import json
import pytest
import requests
from django.test import TestCase
from os import environ


@pytest.mark.skipif(environ.get('CI'), reason='Dont run on CI')
class TestEnrollmentIntegration(TestCase):
    ENDPOINT = 'eox-core/api/v1/enrollment/'
    TOKEN = ''
    data = {}

    @classmethod
    def setUpClass(cls):
        with open('eox_core/tests/integration/data.json') as f:
            data = json.load(f)

        cls.data = data
        request_token_url = '{}{}'.format(
            data['HOST'],
            'oauth2/access_token/'
        )
        request_data = {
            'client_id': data['client_id'],
            'client_secret': data['client_secret'],
            'grant_type': data['grant_type']
        }
        response = requests.post(request_token_url, data=request_data)
        response.raise_for_status()
        cls.TOKEN = response.json()['access_token']

    def test_1_get_valid_email_valid_course(self):
        """
        Test a GET request with valid email and valid course id
        """
        test_data = self.data['test_1_data']
        token = self.TOKEN
        request_url = '{}{}'.format(self.data['HOST'], self.ENDPOINT)
        data = {
            'course_id': test_data['course_id'],
            'email': test_data['email'],
        }
        expected_response = {
            'username': 'honor',
            'is_active': True,
            'mode': 'audit',
            'enrollment_attributes': [],
            'course_id': data['course_id'],
        }
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = requests.get(request_url, data=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_content = response.json()
        self.assertDictContainsSubset(expected_response, response_content)

    def test_2_get_valid_username_valid_course(self):
        """
        Test a GET request with valid username and valid course id
        """
        test_data = self.data['test_2_data']
        token = self.TOKEN
        request_url = '{}{}'.format(self.data['HOST'], self.ENDPOINT)
        data = {
            'course_id': test_data['course_id'],
            'username': test_data['username'],
        }
        expected_response = {
            'username': 'honor',
            'is_active': True,
            'mode': 'audit',
            'enrollment_attributes': [],
            'course_id': test_data['course_id'],
        }
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = requests.get(request_url, data=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_content = response.json()
        self.assertDictContainsSubset(expected_response, response_content)

    def test_3_delete_valid_username_valid_course(self):
        """
        Test a DELETE request with valid username and valid course id
        """
        test_data = self.data['test_3_data']
        token = self.TOKEN
        request_url = '{}{}'.format(self.data['HOST'], self.ENDPOINT)
        data = {
            'course_id': test_data['course_id'],
            'username': test_data['username'],
        }
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = requests.delete(request_url, data=data, headers=headers)
        self.assertEqual(response.status_code, 204)

    def test_4_post_valid_username_valid_course(self):
        """
        Test a POST request with valid username and valid course id
        """
        test_data = self.data['test_4_data']
        token = self.TOKEN
        request_url = '{}{}'.format(self.data['HOST'], self.ENDPOINT)
        data = {
            'course_id': test_data['course_id'],
            'username': test_data['username'],
            'mode': test_data['mode'],
        }
        expected_response = {
            'username': 'honor',
            'is_active': True,
            'mode': 'audit',
            'enrollment_attributes': [],
            'course_id': test_data['course_id'],
        }
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = requests.post(request_url, data=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_content = response.json()
        self.assertDictContainsSubset(expected_response, response_content)

    def test_5_delete_valid_email_valid_course(self):
        """
        Test a DELETE request with valid email and valid course id
        """
        test_data = self.data['test_5_data']
        token = self.TOKEN
        request_url = '{}{}'.format(self.data['HOST'], self.ENDPOINT)
        data = {
            'course_id': test_data['course_id'],
            'email': test_data['email'],
        }
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = requests.delete(request_url, data=data, headers=headers)
        self.assertEqual(response.status_code, 204)

    def test_6_post_valid_email_valid_course(self):
        """
        Test a POST request with valid email and valid course id
        """
        test_data = self.data['test_6_data']
        token = self.TOKEN
        request_url = '{}{}'.format(self.data['HOST'], self.ENDPOINT)
        data = {
            'course_id': test_data['course_id'],
            'email': test_data['email'],
            'mode': test_data['mode'],
        }
        expected_response = {
            'username': 'honor',
            'is_active': True,
            'mode': 'audit',
            'enrollment_attributes': [],
            'course_id': test_data['course_id'],
        }
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = requests.post(request_url, data=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_content = response.json()
        self.assertDictContainsSubset(expected_response, response_content)

    def test_7_put_valid_email_valid_course(self):
        """
        Test a PUT request with valid username and valid course id
        changing is_active flag
        """
        test_data = self.data['test_7_data']
        token = self.TOKEN
        request_url = '{}{}'.format(self.data['HOST'], self.ENDPOINT)
        data = {
            'course_id': test_data['course_id'],
            'email': test_data['email'],
            'is_active': test_data['is_active'],
            'mode': test_data['mode']
        }
        expected_response = {
            'user': 'honor',
            'is_active': test_data['is_active'],
            'mode': 'audit',
            'enrollment_attributes': [],
            'course_id': test_data['course_id'],
        }
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = requests.put(request_url, data=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_content = response.json()
        self.assertDictContainsSubset(expected_response, response_content)

    def test_8_put_valid_username_valid_course(self):
        """
        Test a PUT request with valid username and valid course id
        changing is_active flag
        """
        test_data = self.data['test_8_data']
        token = self.TOKEN
        request_url = '{}{}'.format(self.data['HOST'], self.ENDPOINT)
        data = {
            'course_id': test_data['course_id'],
            'username': test_data['username'],
            'is_active': test_data['is_active'],
            'mode': test_data['mode']
        }
        expected_response = {
            'user': 'honor',
            'is_active': test_data['is_active'],
            'mode': 'audit',
            'enrollment_attributes': [],
            'course_id': test_data['course_id'],
        }
        headers = {'Authorization': 'Bearer {}'.format(token)}
        response = requests.put(request_url, data=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_content = response.json()
        self.assertDictContainsSubset(expected_response, response_content)

    # NOTE: trying to change modes on a devstack enviroment will
    # return a 500 status code and fail the test
    # def test_9_put_valid_username_valid_course_modechange(self):
    #     """
    #     Test a PUT request with valid username and valid course id
    #     """
    #     test_data = self.data['test_9_data']
    #     token = self.TOKEN
    #     request_url = '{}{}'.format(self.data['HOST'], self.ENDPOINT)
    #     data = {
    #         'course_id': test_data['course_id'],
    #         'username': test_data['username'],
    #         'is_active': test_data['is_active'],
    #         'mode': test_data['mode']
    #     }
    #     expected_response = {
    #         'user': 'honor',
    #         'is_active': test_data['is_active'],
    #         'mode': 'audit',
    #         'enrollment_attributes': [],
    #         'course_id': test_data['course_id'],
    #     }
    #     headers = {'Authorization': 'Bearer {}'.format(token)}
    #     response = requests.put(request_url, data=data, headers=headers)
    #     self.assertEqual(response.status_code, 200)
    #     response_content = response.json()
    #     self.assertDictContainsSubset(expected_response, response_content)

    @classmethod
    def tearDownClass(cls):
        pass
