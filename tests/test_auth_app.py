import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_user_can_register_login_refresh_and_read_me(api_client):
    register = api_client.post(
        reverse("auth-register"),
        {
            "email": "ada@example.com",
            "username": "ada",
            "password": "password123",
        },
        format="json",
    )

    assert register.status_code == 201
    assert register.data["user"]["email"] == "ada@example.com"
    assert register.data["access"]
    assert register.data["refresh"]
    assert get_user_model().objects.filter(username="ada").exists()

    login = api_client.post(
        reverse("auth-login"),
        {"email": "ada@example.com", "password": "password123"},
        format="json",
    )
    assert login.status_code == 200
    assert login.data["access"]
    assert login.data["refresh"]

    refresh = api_client.post(
        reverse("auth-refresh"),
        {"refresh": login.data["refresh"]},
        format="json",
    )
    assert refresh.status_code == 200
    assert refresh.data["access"]

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
    me = api_client.get(reverse("auth-me"))
    assert me.status_code == 200
    assert me.data["username"] == "ada"


@pytest.mark.django_db
def test_logout_blacklists_refresh_token(api_client):
    register = api_client.post(
        reverse("auth-register"),
        {
            "email": "grace@example.com",
            "username": "grace",
            "password": "password123",
        },
        format="json",
    )

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {register.data['access']}")
    logout = api_client.post(reverse("auth-logout"), {"refresh": register.data["refresh"]}, format="json")

    assert logout.status_code == 205

