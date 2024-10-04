import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

from core.tests.test_passwords import get_tokens


User = get_user_model()

pytestmark = pytest.mark.django_db


class TestUserRegistration:

    def test_successful_registration(self, client, user_data):
        data = {
            "email": user_data['email'],
            "password": user_data["password"]
        }
        url = reverse("users-list")
        response = client.post(url, data, format="json")
        assert response.status_code == 201
        assert response.data['detail'] == "User registration is successful, check your email for account verification link"

        # Check that an email was sent
        assert len(mail.outbox) == 1
        
        # Check the subject of the email
        assert mail.outbox[0].subject == "Account confirmation link"
        
        # Optionally check the recipient and body of the email
        assert mail.outbox[0].to == [user_data['email']]

        user = User.objects.filter(email=user_data['email']).first()
        assert not user.is_active
        assert not user.is_verified
        assert not user.is_superuser
        assert not user.is_staff

    def test_verify_account(self, client, user_data):
        data = {
            "email": user_data['email'],
            "password": user_data["password"]
        }
        url = reverse("users-list")
        response = client.post(url, data, format="json")

        uid, token = get_tokens(mail.outbox[0].body)

        assert (uid and token)

        # verify account
        data={
            "uid": uid,
            "token": token
        }
        url = reverse("users-verify")
        res = client.post(url, data, format="json")
        assert res.status_code == 200
        assert res.data['message'] == "Your account has been verified successfully"
        user = User.objects.filter(email=user_data['email']).first()

        assert user.is_active
        assert user.is_verified

    def test_missing_fields(self, client, user_data):
        data = {
            "email": user_data['email']
        }
        url = reverse("users-list")
        response = client.post(url, data, format="json")
        assert response.status_code == 400
        assert "errors" in response.data

    def test_less_password_characters(self, client, user_data):
        data = {
            "email": user_data['email'],
            "password": "1234"
        }
        url = reverse("users-list")
        response = client.post(url, data, format="json")
        assert response.status_code == 400
        assert "errors" in response.data
        assert response.data['errors']['password'] == "Password must be at least 8 characters long."
    
    def test_password_only_numbers(self, client, user_data):
        data = {
            "email": user_data['email'],
            "password": "123478977078098"
        }
        url = reverse("users-list")
        response = client.post(url, data, format="json")
        assert response.status_code == 400
        assert "errors" in response.data
        assert response.data['errors']['password'] == "Password must contain at least one letter."

    def test_password_doesnt_contain_special_characters(self, client, user_data):
        data = {
            "email": user_data['email'],
            "password": "timetokill01"
        }
        url = reverse("users-list")
        response = client.post(url, data, format="json")
        assert response.status_code == 400
        assert "errors" in response.data
        assert response.data['errors']['password'] == "Password must contain at least one special character."

    def test_passing_extra_fields(self, client, user_data):
        data={
            "email": user_data["email"],
            "password": user_data["password"],
            "username": 'test_username'
        }
        url = reverse("users-list")
        response = client.post(url, data, format="json")
        assert response.status_code == 201
        
        user = User.objects.filter(email=user_data['email']).first()
        assert user.username is None
        assert user.email == user_data['email']


    

