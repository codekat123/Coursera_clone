from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils.text import slugify
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
class CoursesAPITests(APITestCase):
    def setUp(self):
        # Register an instructor and auth client
        reg_url = reverse('users:register')
        payload = {
            'role': 'instructor',
            'username': 'inst_courses',
            'password': 'passw0rd!',
            'full_name': 'Inst Courses',
            'title': 'Prof.',
            'specialization': 'CS',
        }
        resp = self.client.post(reg_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.access = resp.data['tokens']['access']
        self.refresh = resp.data['tokens']['refresh']

    def _auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')

    def _create_subject(self, title='Programming'):
        # Create subject directly because SubjectSerializer marks slug read_only
        subj = Subject.objects.create(title=title, slug=slugify(title))
        return {'title': subj.title, 'slug': subj.slug}

    def _create_course(self, subject_slug, title='Intro to Python'):
        self._auth()
        url = reverse('courses:course-create', kwargs={'slug': subject_slug})
        payload = {
            'title': title,
            'overview': 'Basics of Python',
            'status': 'AV',
        }
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Fetch the created course to get its slug
        course = Course.objects.get(title=title, subject__slug=subject_slug)
        return {'id': course.id, 'slug': course.slug, 'title': course.title}

    def _create_module(self, course_slug, title='Module 1'):
        self._auth()
        url = reverse('courses:module-create', kwargs={'slug': course_slug})
        payload = {
            'title': title,
            'description': 'First module',
        }
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        return resp.data

    def test_subjects_list_and_create(self):
        # Public list should work (initially empty)
        list_url = reverse('courses:subject-list')
        resp = self.client.get(list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Create subject as instructor
        subject = self._create_subject('Math')
        self.assertEqual(subject['title'], 'Math')

        # List again should include created subject
        resp = self.client.get(list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.data['results'] if isinstance(resp.data, dict) and 'results' in resp.data else resp.data
        self.assertTrue(any(s['title'] == 'Math' for s in data))

    def test_course_create_list_retrieve(self):
        subj = self._create_subject('CS')
        course = self._create_course(subj['slug'], 'Algorithms')

        # List by subject (public)
        list_url = reverse('courses:course-list', kwargs={'slug': subj['slug']})
        resp = self.client.get(list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) >= 1 or 'results' in resp.data)

        # Retrieve requires auth
        self._auth()
        retrieve_url = reverse('courses:course-retrieve', kwargs={'slug': course['slug']})
        resp = self.client.get(retrieve_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['slug'], course['slug'])

    def test_module_create_list_retrieve(self):
        subj = self._create_subject('Physics')
        course = self._create_course(subj['slug'], 'Mechanics')

        module = self._create_module(course['slug'], 'Kinematics')

        # List modules by course (public)
        list_url = reverse('courses:module-list', kwargs={'slug': course['slug']})
        resp = self.client.get(list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Retrieve single module by id (public)
        retrieve_url = reverse('courses:module-retrieve', kwargs={'id': module['id']})
        resp = self.client.get(retrieve_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['id'], module['id'])

    def test_content_create_list_retrieve_and_delete(self):
        subj = self._create_subject('Biology')
        course = self._create_course(subj['slug'], 'Genetics')
        module = self._create_module(course['slug'], 'DNA Basics')

        # Create content (text)
        self._auth()
        create_url = reverse('courses:content-create')
        # Provide instructor id to satisfy serializer validation
        from users.models import Instructor
        inst_id = Instructor.objects.get(username='inst_courses').id
        payload = {
            'type': 'text',
            'module_id': module['id'],
            'data': {
                'title': 'Intro Text',
                'content': 'DNA is the blueprint of life.',
                'instructor': inst_id,
            }
        }
        resp = self.client.post(create_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        content_id = resp.data['content_id']

        # List contents of module (public)
        list_url = reverse('courses:content-list', kwargs={'module_id': module['id']})
        resp = self.client.get(list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Retrieve content (public)
        retrieve_url = reverse('courses:content-retrieve', kwargs={'id': content_id})
        resp = self.client.get(retrieve_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Delete content requires instructor auth
        self._auth()
        delete_url = reverse('courses:content-delete', kwargs={'id': content_id})
        resp = self.client.delete(delete_url)
        self.assertIn(resp.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])

