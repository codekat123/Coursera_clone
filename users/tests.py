from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


SQLITE_DB_SETTINGS = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CACHE_SETTINGS = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


@override_settings(DATABASES=SQLITE_DB_SETTINGS, CACHES=CACHE_SETTINGS)
class UserAuthAPITests(APITestCase):
    def test_register_student_success(self):
        url = reverse('users:register')
        payload = {
            'role': 'student',
            'username': 'stud1',
            'password': 'passw0rd!',
            'full_name': 'Student One',
            'level': 'Beginner',
            'date_of_birth': '2000-01-01',
        }

        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', resp.data)
        self.assertIn('access', resp.data['tokens'])
        self.assertIn('refresh', resp.data['tokens'])
        self.assertEqual(resp.data['username'], 'stud1')

    def test_register_instructor_success(self):
        url = reverse('users:register')
        payload = {
            'role': 'instructor',
            'username': 'inst1',
            'password': 'passw0rd!',
            'full_name': 'Instructor One',
            'title': 'Dr.',
            'specialization': 'Math',
        }

        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', resp.data)
        self.assertIn('access', resp.data['tokens'])
        self.assertIn('refresh', resp.data['tokens'])
        self.assertEqual(resp.data['username'], 'inst1')

    def test_register_invalid_role(self):
        url = reverse('users:register')
        payload = {
            'role': 'admin',
            'username': 'who',
            'password': 'irrelevant',
        }
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', resp.data)

    def test_logout_with_refresh_token(self):
        # Register an instructor to obtain tokens
        reg_url = reverse('users:register')
        payload = {
            'role': 'instructor',
            'username': 'inst2',
            'password': 'passw0rd!',
            'full_name': 'Instructor Two',
            'title': 'Mr',
            'specialization': 'Science',
        }
        reg_resp = self.client.post(reg_url, payload, format='json')
        self.assertEqual(reg_resp.status_code, status.HTTP_201_CREATED)
        access = reg_resp.data['tokens']['access']
        refresh = reg_resp.data['tokens']['refresh']

        # Call logout with Bearer auth and provided refresh token
        logout_url = reverse('users:logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        resp = self.client.post(logout_url, {'refresh_token': refresh}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_requires_refresh_token(self):
        reg_url = reverse('users:register')
        reg_resp = self.client.post(reg_url, {
            'role': 'instructor',
            'username': 'inst3',
            'password': 'passw0rd!',
            'full_name': 'Instructor Three',
            'title': 'Ms',
            'specialization': 'Physics',
        }, format='json')
        access = reg_resp.data['tokens']['access']
        logout_url = reverse('users:logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        resp = self.client.post(logout_url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

