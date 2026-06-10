from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .models import UserProfile


class UserProfileModelTest(TestCase):
    def test_create_user_profile_on_user_creation(self):
        user = User.objects.create_user(
            username="testuser", password="pass123"
        )
        profile = UserProfile.objects.create(
            user=user, phone="123456789"
        )
        self.assertEqual(profile.user.username, "testuser")
        self.assertEqual(profile.phone, "123456789")
        self.assertEqual(str(profile), "Perfil de testuser")

    def test_user_profile_optional_phone(self):
        user = User.objects.create_user(
            username="nophone", password="pass123"
        )
        profile = UserProfile.objects.create(user=user)
        self.assertIsNone(profile.phone)

    def test_one_to_one_relation(self):
        user1 = User.objects.create_user(
            username="user1", password="pass123"
        )
        UserProfile.objects.create(user=user1)
        user2 = User.objects.create_user(
            username="user2", password="pass123"
        )
        profile2 = UserProfile.objects.create(user=user2)
        self.assertEqual(profile2.user.username, "user2")


class AuthAPITest(APITestCase):
    login_url = "/api/auth/login/"
    register_url = "/api/auth/register/"

    def test_register_returns_201_and_tokens(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "newuser",
                "email": "new@test.com",
                "password": "StrongPass1",
                "password2": "StrongPass1",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["username"], "newuser")
        self.assertEqual(User.objects.count(), 1)

    def test_register_password_mismatch_returns_400(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "newuser",
                "email": "new@test.com",
                "password": "StrongPass1",
                "password2": "DifferentPass1",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username_returns_400(self):
        User.objects.create_user(username="existing", password="pass123")
        response = self.client.post(
            self.register_url,
            {
                "username": "existing",
                "email": "dup@test.com",
                "password": "StrongPass1",
                "password2": "StrongPass1",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_returns_200_and_tokens(self):
        User.objects.create_user(
            username="loginuser", password="CorrectPass1"
        )
        response = self.client.post(
            self.login_url,
            {"username": "loginuser", "password": "CorrectPass1"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["username"], "loginuser")

    def test_login_wrong_password_returns_401(self):
        User.objects.create_user(
            username="loginuser", password="CorrectPass1"
        )
        response = self.client.post(
            self.login_url,
            {"username": "loginuser", "password": "wrong"},
            format="json",
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_login_missing_fields_returns_400(self):
        response = self.client.post(
            self.login_url, {"username": "nopass"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_reservations_returns_401(self):
        response = self.client.get("/api/reservations/")
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_unauthenticated_resources_returns_200(self):
        response = self.client.get("/api/resources/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
