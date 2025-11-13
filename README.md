# Coursera-like Backend (Django + DRF)

A Django REST Framework backend for a Coursera-like platform with users, courses, enrollments, quizzes, and payments (PayPal).

## Tech Stack
- Django 5
- Django REST Framework
- JWT auth (djangorestframework-simplejwt)
- PostgreSQL (runtime)
- Redis cache (django-redis)
- Celery (configured, optional for local dev)
- PayPal Checkout SDK

## Project Structure
- core/ (project settings and urls)
- users/ (custom user model with Student/Instructor, auth endpoints)
- courses/ (subjects, courses, modules, content)
- enrollments/ (student enrollments)
- quiz/ (quizzes, questions, answers)
- payments/ (PayPal order create/capture)

## Requirements
- Python 3.11+
- PostgreSQL 13+
- Redis (optional for local dev; required if you want Redis cache)

## Setup
1) Create and activate a virtualenv
```
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies
```
pip install -r requirements.txt
```

3) Create .env in project root (same folder as manage.py)
```
SECRET_KEY=your-secret
DEBUG=True

DB_NAME=yourdb
DB_USER=youruser
DB_PASSWORD=yourpass
HOST=127.0.0.1
PORT=5432

# Redis (optional for local development)
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=1
# If your Redis needs auth
REDIS_USERNAME=
REDIS_PASSWORD=

# Celery (optional)
CELERY_BROKER_URL=redis://127.0.0.1:6379/2
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/3

# Email (optional for local dev)
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Payments
DEFAULT_CURRENCY=USD
PAYPAL_ENV=sandbox
PAYPAL_CLIENT_ID=
PAYPAL_CLIENT_SECRET=
PAYPAL_WEBHOOK_ID=
```

4) Run migrations
```
python manage.py migrate
```

5) Run server
```
python manage.py runserver
```

## Key Endpoints
- Auth
  - POST /user/register/
  - POST /user/logout/
  - POST /user/api/token/
  - POST /user/api/token/refresh/
- Courses
  - GET /courses/subjects/
  - CRUD via namespaced routes under /courses/
- Enrollments
  - POST /enrollments/create/
  - DELETE /enrollments/delete/
- Quiz
  - POST /quiz/courses/<slug:slug>/quizzes/create/
  - GET /quiz/quizzes/
  - GET /quiz/quizzes/<int:pk>/
  - PUT /quiz/quizzes/<int:id>/update/
  - DELETE /quiz/quizzes/<int:id>/delete/
- Payments
  - POST /payments/paypal/create-order/<int:course_id>/
  - POST /payments/paypal/capture/
  - POST /payments/paypal/webhook/

Note: Some enrollment URL patterns currently omit required parameters used by views. Tests illustrate current behavior.

## Testing
- Test runner: Django default (no extra config required)
- API tests use DRF APITestCase
- DB/cache in tests are overridden to in-memory sqlite and locmem cache

Run full test suite:
```
python manage.py test
```
Run a single app:
```
python manage.py test users
python manage.py test courses
python manage.py test enrollments
python manage.py test quiz
python manage.py test payments
```

## Payments (Sandbox)
- The PayPal client uses environment variables. Tests mock PayPal calls so no external network is needed.

## Notes
- Celery/Redis are configured but not required to run tests.
- Ensure PostgreSQL is running and credentials in .env are correct for local dev.
