import pytest

from django.urls import reverse


pytestmark = pytest.mark.django_db


class TestLogin:

    def test_login_successful(self, client, activated_user):
        data = {
            "email": activated_user.email,
            "password": "timetokill01_"
        }
        url = reverse("token_obtain_pair")

        response = client.post(url, data, format="json")
        assert response.status_code == 200
        assert response.data['message'] == "you've successfully logged in"
        assert "data" in response.data
        assert "refresh" in response.data
        assert "access" in response.data

    def test_invalid_credentials(self, client):
        data = {
            "email": "t@gmail.com",
            "password": "timetokill01_"
        }
        url = reverse("token_obtain_pair")

        response = client.post(url, data, format="json")
        assert response.status_code == 401
        assert str(response.data) == "{'detail': ErrorDetail(string='No active account found with the given credentials', code='no_active_account')}"

    # def test_inactivated_user_cannot_login(self, client, user):
    #     data = {
    #         "email": user.email,
    #         "password": "timetokill01_"
    #     }
    #     url = reverse("token_obtain_pair")

    #     response = client.post(url, data, format="json")
    #     assert response.status_code == 401
    #     print(response.data)
    #     assert "errors" in response.data
    #     assert response.data["errors"] == "No active account"

    # def test_missing_token(self, client, user):

    #     data = {
    #         "email": user.email,
    #         "password": "timetokill01_"
    #     }
    #     url = reverse("token_obtain_pair")

    #     response = client.post(url, data, format="json")
    #     assert response.status_code == 401
    #     assert "errors" in response.data
    #     assert response.data["errors"] == "Invalid credentials"

    # def test_invalid_token(self, client, token):
    #     ...

    # def test_refresh_token(self, client, user):
    #     ...

