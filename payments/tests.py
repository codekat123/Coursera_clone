from types import SimpleNamespace
from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch

from courses.models import Subject, Course
from enrollments.models import Enrollment
from payments.models import Payment


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
class PaymentsAPITests(APITestCase):
    def setUp(self):
        reg_url = reverse('users:register')
        stud_payload = {
            'role': 'student',
            'username': 'stud_pay',
            'password': 'passw0rd!',
            'full_name': 'Stud Pay',
            'level': 'Beginner',
            'date_of_birth': '2000-01-01',
        }
        resp = self.client.post(reg_url, stud_payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.access = resp.data['tokens']['access']

        subj = Subject.objects.create(title='Payments', slug='payments')
        from users.models import Instructor
        instructor = Instructor.objects.create_user(username='inst_pay', password='passw0rd!')
        self.course = Course.objects.create(subject=subj, title='Pay 101', slug='pay-101', overview='Intro', status='AV', instructor=instructor, price=25)

    def _auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')

    @patch('payments.views.paypal_create_order')
    def test_create_order_success(self, mock_create_order):
        self._auth()
        approve_link = SimpleNamespace(rel='approve', href='https://paypal.test/approve/123')
        mock_create_order.return_value = SimpleNamespace(id='ORDER123', links=[approve_link])

        url = reverse('payments:paypal-create-order', kwargs={'course_id': self.course.id})
        resp = self.client.post(url, {'currency': 'USD'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['order_id'], 'ORDER123')
        self.assertEqual(resp.data['approve_url'], 'https://paypal.test/approve/123')

        payment = Payment.objects.get(provider_order_id='ORDER123')
        self.assertEqual(payment.status, Payment.Status.CREATED)
        self.assertEqual(payment.amount, self.course.price)

    @patch('payments.views.paypal_create_order')
    def test_create_order_when_already_enrolled_returns_400(self, mock_create_order):
        self._auth()
        from users.models import Student
        student = Student.objects.get(username='stud_pay')
        Enrollment.objects.create(student=student, course=self.course)

        url = reverse('payments:paypal-create-order', kwargs={'course_id': self.course.id})
        resp = self.client.post(url, {'currency': 'USD'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        mock_create_order.assert_not_called()

    @patch('payments.views.paypal_capture_order')
    @patch('payments.views.paypal_create_order')
    def test_capture_success_marks_payment_and_creates_enrollment(self, mock_create_order, mock_capture_order):
        self._auth()
        approve_link = SimpleNamespace(rel='approve', href='https://paypal.test/approve/123')
        mock_create_order.return_value = SimpleNamespace(id='ORDER789', links=[approve_link])
        create_url = reverse('payments:paypal-create-order', kwargs={'course_id': self.course.id})
        resp = self.client.post(create_url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        mock_capture_order.return_value = SimpleNamespace(status='COMPLETED')
        capture_url = reverse('payments:paypal-capture')
        resp2 = self.client.post(capture_url, {'order_id': 'ORDER789'}, format='json')
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        payment = Payment.objects.get(provider_order_id='ORDER789')
        self.assertEqual(payment.status, Payment.Status.CAPTURED)
        self.assertTrue(Enrollment.objects.filter(course=self.course, student__username='stud_pay').exists())

    def test_capture_missing_order_id_returns_400(self):
        self._auth()
        capture_url = reverse('payments:paypal-capture')
        resp = self.client.post(capture_url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('payments.views.paypal_capture_order')
    @patch('payments.views.paypal_create_order')
    def test_capture_non_completed_marks_failed(self, mock_create_order, mock_capture_order):
        self._auth()
        approve_link = SimpleNamespace(rel='approve', href='https://paypal.test/approve/123')
        mock_create_order.return_value = SimpleNamespace(id='ORDERBAD', links=[approve_link])
        create_url = reverse('payments:paypal-create-order', kwargs={'course_id': self.course.id})
        resp = self.client.post(create_url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        mock_capture_order.return_value = SimpleNamespace(status='PENDING')
        capture_url = reverse('payments:paypal-capture')
        resp2 = self.client.post(capture_url, {'order_id': 'ORDERBAD'}, format='json')
        self.assertEqual(resp2.status_code, status.HTTP_400_BAD_REQUEST)
        payment = Payment.objects.get(provider_order_id='ORDERBAD')
        self.assertEqual(payment.status, Payment.Status.FAILED)
