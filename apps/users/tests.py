import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()

@pytest.mark.django_db
class TestUserAuthentication:
    def setup_method(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'

    def test_user_registration(self):
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.client.post(self.register_url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email=data["email"]).exists()

    def test_user_login(self):
        user = User.objects.create_user(
            email="login@example.com",
            username="loginuser",
            password="password123"
        )
        data = {
            "email": "login@example.com",
            "password": "password123"
        }
        response = self.client.post(self.login_url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
