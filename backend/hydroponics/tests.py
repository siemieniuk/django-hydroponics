from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from hydroponics.models import HydroponicSystem, Measurement


class TestMeasurementsEndpoints(APITestCase):
    def setUp(self):
        username = "adam123"
        email = "adam123@example.com"
        password = "1@qwerty"
        token = get_token_of_new_user(
            self.client, username=username, email=email, password=password
        )

        user = User.objects.get(username=username)
        system = HydroponicSystem(
            name="my_system", description="sample", owner=user
        )
        system.save()

        self.system_pk = system.pk
        self.headers = {"HTTP_AUTHORIZATION": token}
        self.body = {
            "water_ph": 7.0,
            "water_tds": 14.0,
            "water_temp": 21.5,
        }

    def test_add_full_measurement(self):
        response = self.client.post(
            reverse("measurements", kwargs={"hydroponics_id": self.system_pk}),
            data=self.body,
            hydroponics_id=self.system_pk,
            **self.headers,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            f"Expected status code is 201, got {response.status_code}",
        )

    def test_add_no_measurements(self):
        """Expected to not create any new measurement
        if nothing was provided in the request body
        """
        self.body = None
        response = self.client.post(
            reverse("measurements", kwargs={"hydroponics_id": self.system_pk}),
            data=self.body,
            hydroponics_id=self.system_pk,
            **self.headers,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            f"Expected status code is 400, got {response.status_code}",
        )

    def test_add_any_empty_measurement(self):
        """Expected to create a new measurement with partial information"""
        for key in self.body.keys():
            body = self.body.copy()
            body[key] = ""

            response = self.client.post(
                reverse(
                    "measurements", kwargs={"hydroponics_id": self.system_pk}
                ),
                data=body,
                hydroponics_id=self.system_pk,
                **self.headers,
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                f"Expected status code is 201, got {response.status_code}",
            )

    def test_add_partial_measurement(self):
        for key in self.body.keys():
            body = self.body.copy()
            body.pop(key)

            response = self.client.post(
                reverse(
                    "measurements", kwargs={"hydroponics_id": self.system_pk}
                ),
                data=body,
                hydroponics_id=self.system_pk,
                **self.headers,
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                f"Expected status code is 201, got {response.status_code}",
            )

    def test_add_measurement_by_wrong_user(self):
        token = get_token_of_new_user(
            self.client,
            username="other",
            email="other@example.com",
            password="password",
        )

        self.headers = {"HTTP_AUTHORIZATION": token}
        response = self.client.post(
            reverse("measurements", kwargs={"hydroponics_id": self.system_pk}),
            data=self.body,
            hydroponics_id=self.system_pk,
            **self.headers,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            f"Expected status code is 403, got {response.status_code}",
        )


class TestHydroponicsEndpoints(APITestCase):
    def setUp(self):
        username = "adam123"
        email = "adam123@example.com"
        password = "1@qwerty"
        token = get_token_of_new_user(self.client, username, email, password)

        user = User.objects.get(username=username)
        system = HydroponicSystem(
            name="my_system", description="sample", owner=user
        )
        system.save()
        self.system_pk = system.pk

        system2 = HydroponicSystem(
            name="my_other_system", description="other", owner=user
        )
        system2.save()

        self.headers = {
            "HTTP_AUTHORIZATION": token,
        }
        self.body = {
            "water_ph": 7.0,
            "water_tds": 14.0,
            "water_temp": 21.5,
        }

    def test_retrieve_my_system_with_no_measurements(self):
        response = self.client.get(
            reverse("hydroponic_system-detail", kwargs={"pk": self.system_pk}),
            **self.headers,
        )

        expected_data = {
            "name": "my_system",
            "pk": self.system_pk,
            "description": "sample",
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["details"]["id"], expected_data["pk"])
        self.assertEqual(
            response.data["details"]["name"], expected_data["name"]
        )
        self.assertEqual(
            response.data["details"]["description"],
            expected_data["description"],
        )
        self.assertEqual(len(response.data["measurements"]), 0)

    def test_retrieve_my_system_with_more_than_ten_measurements(self):
        # send 11 measurements
        for i in range(11):
            body = {
                "water_ph": i,
                "water_tds": i,
                "water_temp": i,
            }
            self.client.post(
                reverse(
                    "measurements", kwargs={"hydroponics_id": self.system_pk}
                ),
                body,
                **self.headers,
            )

        response = self.client.get(
            reverse("hydroponic_system-detail", kwargs={"pk": self.system_pk}),
            **self.headers,
        )

        expected_data = {
            "name": "my_system",
            "pk": self.system_pk,
            "description": "sample",
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["details"]["id"], expected_data["pk"])
        self.assertEqual(
            response.data["details"]["name"], expected_data["name"]
        )
        self.assertEqual(
            response.data["details"]["description"],
            expected_data["description"],
        )
        self.assertEqual(len(response.data["measurements"]), 10)

    def test_retrieve_stranger_system(self):
        token = get_token_of_new_user(
            self.client,
            username="other",
            email="other@example.com",
            password="1@qwerty",
        )

        headers = {
            "HTTP_AUTHORIZATION": token,
        }
        response = self.client.get(
            reverse("hydroponic_system-detail", kwargs={"pk": self.system_pk}),
            **headers,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_system_without_authorization(self):
        response = self.client.get(
            reverse("hydroponic_system-detail", kwargs={"pk": self.system_pk})
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_my_systems(self):
        response = self.client.get(
            reverse("hydroponic_system-list"),
            **self.headers,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_systems_without_authorization(self):
        response = self.client.get(reverse("hydroponic_system-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


def get_token_of_new_user(client, username: str, email: str, password: str):
    body = {
        "username": username,
        "email": email,
        "password": password,
        "password2": password,
    }
    response = client.post(reverse("user_register"), data=body)

    return f"Bearer {response.data['token']['access']}"
