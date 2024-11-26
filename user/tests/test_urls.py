from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from user.views import index, register, logout, login, user_profile, my_rides


class TestUrl(SimpleTestCase):

    def test_search_resolved(self):
        url = reverse("myrides")
        self.assertEquals(resolve(url).func, my_rides)

    def test_index_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_register_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_login_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login)

    def test_logout_resolved(self):
        url = reverse('logout')

        self.assertEquals(resolve(url).func, logout)

    def test_profile_resolved(self):
        url = reverse('user_profile', args=["123"])
        self.assertEquals(resolve(url).func, user_profile)


class TestUrl_Response(TestCase):
    def test_index_route_non_logged(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_route_non_logged_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'home/home.html')

    def test_logout_route_non_logged(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_login_route_non_logged(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_route_non_logged_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'user/login.html')

    def test_profile_ride_non_logged(self):
        response = self.client.get(
            reverse('user_profile', args=["67240ab0b84ec3a5aa1e5cc8"]))
        self.assertEqual(response.status_code, 200)

    def test_profile_ride_non_logged_template(self):
        response = self.client.get(
            reverse('user_profile', args=["67240ab0b84ec3a5aa1e5cc8"]))
        self.assertTemplateUsed(response, 'user/404.html')
