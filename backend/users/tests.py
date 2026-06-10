from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import UserProfile


class UserProfileModelTest(APITestCase):
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


class UserAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="listuser", password="pass123"
        )
        UserProfile.objects.create(user=user, phone="987654321")

    def test_list_users_returns_200(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], "listuser")
