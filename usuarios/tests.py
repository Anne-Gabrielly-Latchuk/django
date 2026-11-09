from django.test import TestCase


class HomeViewTests(TestCase):
    def test_home_redirects_to_login(self):
        response = self.client.get('/')

        self.assertRedirects(response, '/usuarios/login/')
