from django.contrib.auth.models import User
from django.test import TestCase
from .models import URL


class URLModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword")
        self.url_data = { "original_url": "https://example.com", "created_by": self.user }
        self.short_url = URL.objects.create(**self.url_data)

    def test_url_creation(self):
        self.assertIsNone(self.short_url.short_url)
        self.assertEqual(URL.original_url, 'https://www.google.com')

    def test_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
