from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser", age=23, password="testpass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.age, 23)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        super_user = User.objects.create_superuser(
            username="superuser", email="superuser@email.com", password="testpass123"
        )
        self.assertEqual(super_user.username, "superuser")
        self.assertEqual(super_user.email, "superuser@email.com")
        self.assertTrue(super_user.is_superuser)


class SignupPageTests(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.age = 23
        self.response = self.client.get(reverse("signup"))

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "signup.html")
        self.assertContains(self.response, "Sign Up")

    def test_signup_form(self):
        User = get_user_model()
        new_user = User.objects.create_user(username=self.username, age=self.age)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(User.objects.all()[0].username, self.username)
        self.assertEqual(User.objects.all()[0].age, self.age)
