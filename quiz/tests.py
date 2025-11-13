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
class QuizAPITests(APITestCase):
    def setUp(self):
        reg_url = reverse('users:register')
        inst_payload = {
            'role': 'instructor',
            'username': 'inst_quiz',
            'password': 'passw0rd!',
            'full_name': 'Inst Quiz',
            'title': 'Dr.',
            'specialization': 'CS',
        }
        inst_resp = self.client.post(reg_url, inst_payload, format='json')
        self.assertEqual(inst_resp.status_code, status.HTTP_201_CREATED)
        self.inst_access = inst_resp.data['tokens']['access']

        stud_payload = {
            'role': 'student',
            'username': 'stud_quiz',
            'password': 'passw0rd!',
            'full_name': 'Stud Quiz',
            'level': 'Beginner',
            'date_of_birth': '2000-01-01',
        }
        stud_resp = self.client.post(reg_url, stud_payload, format='json')
        self.assertEqual(stud_resp.status_code, status.HTTP_201_CREATED)
        self.stud_access = stud_resp.data['tokens']['access']

        subj = Subject.objects.create(title='Algorithms', slug='algorithms')
        from users.models import Instructor
        instructor = Instructor.objects.get(username='inst_quiz')
        self.course = Course.objects.create(subject=subj, title='Algo 101', slug='algo-101', overview='Intro', status='AV', instructor=instructor, price=10)

    def _auth(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_instructor_can_create_quiz_and_update_delete(self):
        self._auth(self.inst_access)
        create_url = reverse('quiz:quiz-create', kwargs={'slug': self.course.slug})
        payload = {'title': 'Quiz 1', 'description': 'Basics'}
        resp = self.client.post(create_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        list_url = reverse('quiz:quiz-list')
        resp_list = self.client.get(list_url)
        self.assertEqual(resp_list.status_code, status.HTTP_200_OK)
        quiz_id = resp_list.data[0]['id'] if isinstance(resp_list.data, list) and resp_list.data else resp_list.data['results'][0]['id']

        retrieve_url = reverse('quiz:quiz-retrieve', kwargs={'pk': quiz_id})
        resp_get = self.client.get(retrieve_url)
        self.assertEqual(resp_get.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_get.data['id'], quiz_id)

        update_url = reverse('quiz:quiz-update', kwargs={'id': quiz_id})
        resp_upd = self.client.put(update_url, {'title': 'Quiz 1 Updated', 'description': 'Basics'}, format='json')
        self.assertIn(resp_upd.status_code, [status.HTTP_200_OK, status.HTTP_202_ACCEPTED])

        delete_url = reverse('quiz:quiz-delete', kwargs={'id': quiz_id})
        resp_del = self.client.delete(delete_url)
        self.assertIn(resp_del.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])

    def test_student_cannot_create_or_modify_quiz_but_can_list_and_retrieve(self):
        self._auth(self.inst_access)
        create_url = reverse('quiz:quiz-create', kwargs={'slug': self.course.slug})
        self.client.post(create_url, {'title': 'Q', 'description': 'D'}, format='json')

        self._auth(self.stud_access)
        list_url = reverse('quiz:quiz-list')
        resp_list = self.client.get(list_url)
        self.assertEqual(resp_list.status_code, status.HTTP_200_OK)
        quiz_id = resp_list.data[0]['id'] if isinstance(resp_list.data, list) and resp_list.data else resp_list.data['results'][0]['id']
        retrieve_url = reverse('quiz:quiz-retrieve', kwargs={'pk': quiz_id})
        resp_get = self.client.get(retrieve_url)
        self.assertEqual(resp_get.status_code, status.HTTP_200_OK)

        update_url = reverse('quiz:quiz-update', kwargs={'id': quiz_id})
        resp_upd = self.client.put(update_url, {'title': 'Nope', 'description': 'x'}, format='json')
        self.assertIn(resp_upd.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED])

        delete_url = reverse('quiz:quiz-delete', kwargs={'id': quiz_id})
        resp_del = self.client.delete(delete_url)
        self.assertIn(resp_del.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED])
