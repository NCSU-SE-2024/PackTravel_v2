"""
This module contains tests for the URL routing and responses of the `user` app in a Django project.
The tests ensure that URLs resolve to the correct views and return the expected status codes and templates.
"""

from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from user.views import index, register, logout, login, user_profile, my_rides


class TestUrl(SimpleTestCase):
    """
    Tests for URL resolution to the correct view functions in the `user` app.
    """

    def test_search_resolved(self):
        """
        Test that the 'myrides' URL resolves to the `my_rides` view.
        """
        url = reverse("myrides")
        self.assertEquals(resolve(url).func, my_rides)

    def test_index_resolved(self):
        """
        Test that the 'index' URL resolves to the `index` view.
        """
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_register_resolved(self):
        """
        Test that the 'register' URL resolves to the `register` view.
        """
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_login_resolved(self):
        """
        Test that the 'login' URL resolves to the `login` view.
        """
        url = reverse('login')
        self.assertEquals(resolve(url).func, login)

    def test_logout_resolved(self):
        """
        Test that the 'logout' URL resolves to the `logout` view.
        """
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout)

    def test_profile_resolved(self):
        """
        Test that the 'user_profile' URL resolves to the `user_profile` view with a valid argument.
        """
        url = reverse('user_profile', args=["123"])
        self.assertEquals(resolve(url).func, user_profile)


class TestUrl_Response(TestCase):
    """
    Tests for HTTP responses and template rendering for the `user` app URLs.
    """

    def test_index_route_non_logged(self):
        """
        Test the 'index' route for a non-logged-in user.
        Ensures that the HTTP response status code is 200 (OK).
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_route_non_logged_template(self):
        """
        Test the 'index' route for a non-logged-in user.
        Ensures that the correct template ('home/home.html') is used.
        """
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'home/home.html')

    def test_logout_route_non_logged(self):
        """
        Test the 'logout' route for a non-logged-in user.
        Ensures that the HTTP response status code is 302 (redirect).
        """
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_login_route_non_logged(self):
        """
        Test the 'login' route for a non-logged-in user.
        Ensures that the HTTP response status code is 200 (OK).
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_route_non_logged_template(self):
        """
        Test the 'login' route for a non-logged-in user.
        Ensures that the correct template ('user/login.html') is used.
        """
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'user/login.html')

    def test_profile_ride_non_logged(self):
        """
        Test the 'user_profile' route for a non-logged-in user with a valid ID.
        Ensures that the HTTP response status code is 200 (OK).
        """
        response = self.client.get(reverse('user_profile', args=["67240ab0b84ec3a5aa1e5cc8"]))
        self.assertEqual(response.status_code, 200)

    def test_profile_ride_non_logged_template(self):
        """
        Test the 'user_profile' route for a non-logged-in user with a valid ID.
        Ensures that the correct template ('user/404.html') is used for this scenario.
        """
        response = self.client.get(reverse('user_profile', args=["67240ab0b84ec3a5aa1e5cc8"]))
        self.assertTemplateUsed(response, 'user/404.html')
