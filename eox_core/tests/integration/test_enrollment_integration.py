"""
Integration tests
"""
import json
from os import environ

import pytest
import requests
from django.test import TestCase


@pytest.mark.skipif(bool(environ.get('CI')), reason='Do not run on CI')
class TestEnrollmentIntegration(TestCase):
    """Test suite"""
    data = {}
    token = {}

    @classmethod
    def setUpClass(cls):
        with open('eox_core/tests/integration/test_data') as file_obj:
            cls.data = json.load(file_obj)
        cls.data['request_url'] = '{}/{}'.format(cls.data['base_url'],
                                                 'eox-core/api/v1/enrollment/')
        data = {
            'client_id': cls.data['client_id'],
            'client_secret': cls.data['client_secret'],
            'grant_type': 'client_credentials'
        }
        request_url = '{}/{}'.format(cls.data['base_url'],
                                     'oauth2/access_token/')
        response = requests.post(request_url, data=data)
        response.raise_for_status()
        cls.data['token'] = response.json()['access_token']

    def test_read_valid_email_course(self):
        # pylint: disable=invalid-name
        """
        Get a valid enrollment
        """
        create_enrollment(self.data)  # SetUp Initial Enrollment
        site1_data = self.data['site1_data']
        data = {
            'email': site1_data['user_email'],
            'course_id': site1_data['course']["id"],
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site1_data['host'],
        }
        expected_response = {
            'username': site1_data['user_id'],
            'course_id': data['course_id'],
        }
        response = requests.get(self.data['request_url'],
                                data=data,
                                headers=headers)
        self.assertEqual(response.status_code, 200)
        response_content = response.json()
        self.assertDictContainsSubset(expected_response, response_content)

    def test_read_invalid_enrollment(self):
        # pylint: disable=invalid-name
        """
        Get a invalid enrollment (doesn't exist)
        """
        site1_data = self.data['site1_data']
        site2_data = self.data['site2_data']
        data = {
            'username': site2_data['user_id'],
            'course_id': site1_data['course']['id'],
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site2_data['host'],
        }
        response = requests.get(self.data['request_url'],
                                data=data,
                                headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_read_invalid_enrollment_for_site(self):
        # pylint: disable=invalid-name
        """
        Get a invalid enrollment (enrollment from other site)
        """
        site1_data = self.data['site1_data']
        site2_data = self.data['site2_data']
        data = {
            'username': site1_data['user_id'],
            'course_id': site1_data['course']['id'],
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site2_data['host'],
        }
        response = requests.get(self.data['request_url'],
                                data=data,
                                headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_create_enrollment_valid_user_mode_course(self):
        # pylint: disable=invalid-name
        """
        Create enrollment with a valid user, valid course,
        valid mode
        """
        delete_enrollment(self.data)  # setUp (delete enrollment if exists)

        site1_data = self.data['site1_data']
        data = {
            'email': site1_data['user_email'],
            'course_id': site1_data['course']['id'],
            'mode': site1_data['course']['mode'],
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site1_data['host'],
        }
        response = requests.post(self.data['request_url'],
                                 data=data,
                                 headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_force_create_enrollment_valid_user_mode_course(self):
        # pylint: disable=invalid-name
        """
        Create enrollment with a valid user, valid course,
        valid mode using force
        """
        delete_enrollment(self.data)  # setUp (delete enrollment if exists)

        site1_data = self.data['site1_data']
        data = {
            'email': site1_data['user_email'],
            'course_id': site1_data['course']['id'],
            'mode': site1_data['course']['mode'],
            'force': 1,
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site1_data['host'],
        }
        response = requests.post(self.data['request_url'],
                                 data=data,
                                 headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_create_valid_course_mode_invalid_user(self):
        # pylint: disable=invalid-name
        """
        Create enrollment with a valid course, valid mode,
        and a non-existent user
        """
        site1_data = self.data['site1_data']
        data = {
            'username': site1_data['fake_user'],
            'course_id': site1_data['course']['id'],
            'mode': site1_data['course']['mode'],
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site1_data['host'],
        }
        response = requests.post(self.data['request_url'],
                                 data=data,
                                 headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_create_valid_course_mode_invalid_user_for_site(self):
        # pylint: disable=invalid-name
        """
        Create enrollment with a valid course, valid mode,
        and a user from another site
        """
        site1_data = self.data['site1_data']
        site2_data = self.data['site2_data']
        data = {
            'email': site2_data['user_email'],
            'course_id': site1_data['course']['id'],
            'mode': site1_data['course']['mode'],
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site1_data['host'],
        }
        response = requests.post(self.data['request_url'],
                                 data=data,
                                 headers=headers)
        self.assertEqual(response.status_code, 202)

    def test_create_valid_user_mode_invalid_course(self):
        # pylint: disable=invalid-name
        """
        Create enrollment with a valid user, valid mode,
        and non-existent course
        """
        site1_data = self.data['site1_data']
        data = {
            'email': site1_data['user_email'],
            'course_id': 'fake_course_id',
            'mode': 'audit',
            'force': 1,
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site1_data['host'],
        }
        response = requests.post(self.data['request_url'],
                                 data=data,
                                 headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_create_valid_user_mode_invalid_course_for_site(self):
        # pylint: disable=invalid-name
        """
        Create enrollment with a valid user, valid mode,
        and a course from another site
        """
        site1_data = self.data['site1_data']
        site2_data = self.data['site2_data']
        data = {
            'email': site2_data['user_email'],
            'course_id': site1_data['course']['id'],
            'mode': site1_data['course']['mode'],
            'force': 1,
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site2_data['host'],
        }
        response = requests.post(self.data['request_url'],
                                 data=data,
                                 headers=headers)
        self.assertEqual(response.status_code, 400)

    # NOTE: Mode changes are not working correctly on devstack
    # def test_create_valid_user_course_invalid_mode(self):
    #     # pylint: disable=invalid-name
    #     """
    #     Create enrollment with a valid user, valid course,
    #     and a not available mode
    #     """
    #     site1_data = self.data['site1_data']
    #     data = {
    #         'email': site1_data['user_email'],
    #         'course_id': site1_data['course']['id'],
    #         'mode': 'masters',
    #         'force': 1,
    #     }
    #     headers = {
    #         'Authorization': 'Bearer {}'.format(self.data['token']),
    #         'Host': site1_data['host'],
    #     }
    #     response = requests.post(self.data['request_url'],
    #                              data=data,
    #                              headers=headers)
    #     self.assertEqual(response.status_code, 400)

    def test_delete_valid_enrollment(self):
        # pylint: disable=invalid-name
        """
        Delete a valid enrollment
        """
        create_enrollment(self.data)  # SetUp Initial Enrollment
        site1_data = self.data['site1_data']
        data = {
            'email': site1_data['user_email'],
            'course_id': site1_data['course']["id"],
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site1_data['host'],
        }
        response = requests.delete(self.data['request_url'],
                                   data=data,
                                   headers=headers)
        self.assertEqual(response.status_code, 204)

    def test_delete_invalid_enrollment(self):
        # pylint: disable=invalid-name
        """
        Delete a invalid enrollment(doesn't exist)
        """
        site1_data = self.data['site1_data']
        site2_data = self.data['site2_data']
        data = {
            'email': site2_data['user_email'],
            'course_id': site1_data['course']["id"],
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site2_data['host'],
        }
        response = requests.delete(self.data['request_url'],
                                   data=data,
                                   headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_delete_invalid_enrollment_for_site(self):
        # pylint: disable=invalid-name
        """
        Delete a invalid enrollment(doesn't exist)
        """
        site1_data = self.data['site1_data']
        site2_data = self.data['site2_data']
        data = {
            'email': site1_data['user_email'],
            'course_id': site1_data['course']["id"],
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site2_data['host'],
        }
        response = requests.delete(self.data['request_url'],
                                   data=data,
                                   headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_update_valid_enrollment_change_is_active(self):
        # pylint: disable=invalid-name
        """
        Update an existing enrollment; change is_active flag
        """
        create_enrollment(self.data)  # SetUp Initial Enrollment
        site1_data = self.data['site1_data']
        data = {
            'email': site1_data['user_email'],
            'course_id': site1_data['course']["id"],
            'is_active': False,
            'mode': site1_data['course']["mode"],
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site1_data['host'],
        }
        expected_response = {
            'user': site1_data['user_id'],
            'is_active': False,
            'course_id': data['course_id'],
        }
        response = requests.put(self.data['request_url'],
                                data=data,
                                headers=headers)
        self.assertEqual(response.status_code, 200)
        response_content = response.json()
        self.assertDictContainsSubset(expected_response, response_content)

    # NOTE: Mode changes are not working correctly on devstack
    # def test_update_valid_enrollment_change_valid_mode(self):
    #     # pylint: disable=invalid-name
    #     """
    #     Update an existing enrollment; change mode
    #     """
    #     # create_enrollment(self.data)
    #     site1_data = self.data['site1_data']
    #     data = {
    #         'email': site1_data['user_email'],
    #         'course_id': site1_data['course']["id"],
    #         'is_active': True,
    #         'mode': 'masters',
    #     }
    #     headers = {
    #         'Authorization': 'Bearer {}'.format(self.data['token']),
    #         'Host': site1_data['host'],
    #     }
    #     expected_response = {
    #         'user': site1_data['user_id'],
    #         'is_active': True,
    #         'course_id': data['course_id'],
    #         'mode': 'masters',
    #     }
    #     response = requests.put(self.data['request_url'],
    #                             data=data,
    #                             headers=headers)
    #     self.assertEqual(response.status_code, 200)
    #     response_content = response.json()
    #     self.assertDictContainsSubset(expected_response, response_content)

    def test_update_valid_enrollment_change_invalid_mode(self):
        # pylint: disable=invalid-name
        """
        Update an existing enrollment; change to invalid mode
        """
        create_enrollment(self.data)  # SetUp Initial Enrollment
        site1_data = self.data['site1_data']
        data = {
            'email': site1_data['user_email'],
            'course_id': site1_data['course']["id"],
            'is_active': True,
            'mode': 'masters',
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site1_data['host'],
        }
        response = requests.put(self.data['request_url'],
                                data=data,
                                headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_update_invalid_enrollment_change_valid_mode(self):
        # pylint: disable=invalid-name
        """
        Update an non-existent enrollment; change mode
        """
        site1_data = self.data['site1_data']
        site2_data = self.data['site2_data']
        data = {
            'email': site2_data['user_email'],
            'course_id': site1_data['course']["id"],
            'is_active': True,
            'mode': 'masters',
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site2_data['host'],
        }
        response = requests.put(self.data['request_url'],
                                data=data,
                                headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_update_invalid_enrollment_change_is_active(self):
        """
        Update an non-existent enrollment; change is_active flag
        """
        # create_enrollment(self.data)
        site1_data = self.data['site1_data']
        site2_data = self.data['site2_data']
        data = {
            'email': site2_data['user_email'],
            'course_id': site1_data['course']["id"],
            'is_active': False,
            'mode': 'masters',
        }
        headers = {
            'Authorization': 'Bearer {}'.format(self.data['token']),
            'Host': site2_data['host'],
        }
        response = requests.put(self.data['request_url'],
                                data=data,
                                headers=headers)
        self.assertEqual(response.status_code, 400)

    @classmethod
    def tearDownClass(cls):
        pass


def create_enrollment(data):
    """
    Auxiliary function to setUp test fixtures
    """
    req_data = {
        'email': data['site1_data']['user_email'],
        'course_id': data['site1_data']['course']['id'],
        'mode': data['site1_data']['course']['mode']
    }
    headers = {
        'Authorization': 'Bearer {}'.format(data['token']),
        'Host': data['site1_data']['host'],
    }
    response = requests.post(data['request_url'],
                             data=req_data,
                             headers=headers)
    response.raise_for_status()


def delete_enrollment(data):
    """
    Auxiliary function to setUp test fixtures
    """
    req_data = {
        'email': data['site1_data']['user_email'],
        'course_id': data['site1_data']['course']['id']
    }
    headers = {
        'Authorization': 'Bearer {}'.format(data['token']),
        'Host': data['site1_data']['host'],
    }
    response = requests.delete(data['request_url'],
                               data=req_data,
                               headers=headers)
    if response.status_code == 404:
        return
    response.raise_for_status()
