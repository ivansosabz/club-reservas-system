from django.contrib.auth.models import User
from django.test import TestCase
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
