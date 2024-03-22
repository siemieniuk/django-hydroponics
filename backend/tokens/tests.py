from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestRegister(APITestCase):
    def setUp(self):
        self.body = {
            "username": "adam123",
            "email": "adam123@example.com",
            "password": "1@qwerty",
            "password2": "1@qwerty",
        }
        self.url = reverse("user_register")

    def test_create_user(self):
        response = self.client.post(self.url, data=self.body)
        self.assertEquals(
            status.HTTP_201_CREATED,
            response.status_code,
            f"The status code should be 201, got {response.status_code}",
        )

    def test_create_existing_user(self):
        response = self.client.post(self.url, data=self.body)
        self.assertEquals(
            status.HTTP_201_CREATED,
            response.status_code,
            f"The status code should be 201, got {response.status_code}",
        )

        response = self.client.post(self.url, data=self.body)
        self.assertEquals(
            status.HTTP_400_BAD_REQUEST,
            response.status_code,
            f"The status code should be 400, got {response.status_code}",
        )

    def test_passwords_do_not_match(self):
        data = self.body
        data["password2"] = "other_password"
        response = self.client.post(self.url, data=data)
        self.assertEquals(
            status.HTTP_400_BAD_REQUEST,
            response.status_code,
            f"The status code should be 400, got {response.status_code}",
        )
