from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from publish.views import publish_index, display_ride, create_route, select_route


class TestUrl(SimpleTestCase):

    def test_publish_index_resolved(self):
        url = reverse('publish')
        self.assertEquals(resolve(url).func, publish_index)

    def test_create_ride_resolved(self):
        url = reverse('create_route')
        self.assertEquals(resolve(url).func, create_route)

    def test_login_resolved(self):
        url = reverse('select_route')
        self.assertEquals(resolve(url).func, select_route)

    def test_display_ride_resolved(self):
        url = reverse('display_ride', args=["Huntsville, AL, USA"])
        self.assertEquals(resolve(url).func, display_ride)

        # def test_add_route_resolved(self):
    #     url = reverse('add_route')
    #     self.assertEquals(resolve(url).func, add_)


class TestUrl_Response(TestCase):
    def test_create_route_non_logged(self):
        response = self.client.get(reverse('create_route'))
        self.assertEqual(response.status_code, 200)

    def test_create_route_non_logged_template(self):
        response = self.client.get(reverse('create_route'))
        self.assertTemplateUsed(response, 'publish/publish.html')

    def test_select_route_non_logged(self):
        response = self.client.get(reverse('select_route'))
        self.assertEqual(response.status_code, 200)

    def test_select_route_non_logged_template(self):
        response = self.client.get(reverse('select_route'))
        self.assertTemplateUsed(response, 'publish/publish.html')

    def test_publish_non_logged(self):
        response = self.client.get(reverse('publish'))
        self.assertEqual(response.status_code, 302)

    def test_display_ride_non_logged(self):
        response = self.client.get(
            reverse('display_ride', args=["Raleigh, NC, USA"]))
        self.assertEqual(response.status_code, 200)

    def test_display_ride_non_logged_template(self):
        response = self.client.get(
            reverse('display_ride', args=["Raleigh, NC, USA"]))
        self.assertTemplateUsed(response, 'publish/route.html')
