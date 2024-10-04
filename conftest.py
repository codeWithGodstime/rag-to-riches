import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.conf import settings


pytestmark = pytest.mark.django_db

User = get_user_model()


@pytest.fixture
def client():
    client = APIClient()
    return client

# @pytest.fixture(autouse=True)
# def email_backend_override():
#     settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#     settings.EMAIL_HOST = "localhost"  # or '127.0.0.1'
#     settings.EMAIL_PORT = 1025


@pytest.fixture
def user_data():
    return {
        "email": "test@gmail.com",
        "password": "timetokill01_"
    }

@pytest.fixture
def user(user_data):
    def _create_user(data: dict):
        user = User.objects.create_user(email=data['email'], password=data['password'])
        user.save()
        return user
    return _create_user(user_data)

@pytest.fixture
def activated_user(user_data):
    def _create_user(data: dict):
        user = User.objects.create_user(email=data['email'], password=data['password'])
        user.is_active = True
        user.is_verified = True
        user.save()
        return user
    return _create_user(user_data)
    