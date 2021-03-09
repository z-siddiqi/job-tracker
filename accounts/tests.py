from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="testpass")
        self.assertEqual(user.username, "testuser")
        self.assertFalse(user.is_guest)
        self.assertFalse(user.is_superuser)

    def test_create_guest(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser", password="testpass", is_guest=True
        )
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.is_guest)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        super_user = User.objects.create_superuser(
            username="superuser", email="superuser@email.com", password="testpass"
        )
        self.assertEqual(super_user.username, "superuser")
        self.assertEqual(super_user.email, "superuser@email.com")
        self.assertTrue(super_user.is_superuser)


class SignupPageTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("signup"))

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "registration/signup.html")
