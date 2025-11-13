from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from courses.models import Subject, Course


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
class EnrollmentAPITests(APITestCase):
    def setUp(self):
        reg_url = reverse('users:register')
        stud_payload = {
            'role': 'student',
            'username': 'stud_enroll',
            'password': 'passw0rd!',
            'full_name': 'Stud Enroll',
            'level': 'Beginner',
            'date_of_birth': '2000-01-01',
        }
        stud_resp = self.client.post(reg_url, stud_payload, format='json')
        self.assertEqual(stud_resp.status_code, status.HTTP_201_CREATED)
        self.access = stud_resp.data['tokens']['access']

        subj = Subject.objects.create(title='Biology', slug='biology')
        from users.models import Student
        student = Student.objects.get(username='stud_enroll')
        from users.models import Instructor
        instructor = Instructor.objects.create_user(username='inst_enroll', password='passw0rd!')
        self.course = Course.objects.create(subject=subj, title='Bio 101', slug='bio-101', overview='Intro', status='AV', instructor=instructor, price=5)

    def _auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')

    def test_create_enrollment_missing_course_id_returns_400(self):
        self._auth()
        url = reverse('enrollments:enrollment-create')
        resp = self.client.post(url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_enrollment_without_slug_returns_404(self):
        self._auth()
        url = reverse('enrollments:enrollment-delete')
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
