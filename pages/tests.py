from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("home"))

    def test_homepage_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "pages/home.html")
