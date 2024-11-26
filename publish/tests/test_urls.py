"""
This module contains test cases for URL resolution and response behavior in the 'publish' application.

Test cases include:
- Checking the resolution of URLs to their respective view functions.
- Verifying the response status code and template used when accessing various views, including authenticated and non-authenticated users.

Dependencies:
- `django.test.SimpleTestCase`: For testing URL resolution without requiring database interaction.
- `django.test.TestCase`: For testing views and their responses, with database interaction.
- `django.urls.reverse`: For generating URLs from view names.
- `django.urls.resolve`: For resolving URLs to view functions.
"""

from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from publish.views import publish_index, display_ride, create_route, select_route


class TestUrl(SimpleTestCase):
    """
    Test suite for checking URL resolution in the 'publish' application.

    This class tests the URL resolution for various views in the 'publish' app. Each test ensures that the URL pattern correctly resolves to the corresponding view function.

    Test cases include:
    - Verifying that the 'publish', 'create_route', 'select_route', and 'display_ride' URLs resolve to the correct view functions.

    This class extends `SimpleTestCase` to focus solely on URL resolution without interacting with a database.
    """


    def test_publish_index_resolved(self):
        """
        Tests the URL resolution for the 'publish' view.

        This test ensures that the URL for the 'publish' view correctly resolves to the `publish_index` view function.

        Asserts:
            - The URL resolves to the `publish_index` view function.
        """

        url = reverse('publish')
        self.assertEquals(resolve(url).func, publish_index)

    def test_create_ride_resolved(self):
        """
        Tests the URL resolution for the 'create_route' view.

        This test ensures that the URL for the 'create_route' view correctly resolves to the `create_route` view function.

        Asserts:
            - The URL resolves to the `create_route` view function.
        """

        url = reverse('create_route')
        self.assertEquals(resolve(url).func, create_route)

    def test_login_resolved(self):
        """
        Tests the URL resolution for the 'select_route' view.

        This test ensures that the URL for the 'select_route' view correctly resolves to the `select_route` view function.

        Asserts:
            - The URL resolves to the `select_route` view function.
        """

        url = reverse('select_route')
        self.assertEquals(resolve(url).func, select_route)

    def test_display_ride_resolved(self):
        """
        Tests the URL resolution for the 'display_ride' view.

        This test ensures that the URL for the 'display_ride' view (with a specific ride argument) correctly resolves to the `display_ride` view function.

        Asserts:
            - The URL resolves to the `display_ride` view function.
        """

        url = reverse('display_ride', args=["Huntsville, AL, USA"])
        self.assertEquals(resolve(url).func, display_ride)

        # def test_add_route_resolved(self):
    #     url = reverse('add_route')
    #     self.assertEquals(resolve(url).func, add_)


class TestUrl_Response(TestCase):
    """
    Test suite for checking HTTP response status codes and templates for URLs in the 'publish' application.

    This class tests the responses for accessing various views, ensuring that correct status codes are returned and the appropriate templates are used.

    Test cases include:
    - Verifying that non-logged-in users can access the 'create_route', 'select_route', and 'display_ride' views.
    - Checking that a redirect is returned when accessing the 'publish' view as a non-logged-in user.
    - Ensuring the correct template is used for the views.

    This class extends `TestCase` to allow interaction with the database and simulate real HTTP requests.
    """

    def test_create_route_non_logged(self):
        """
        Tests the response for accessing the 'create_route' view as a non-logged-in user.

        This test ensures that when a non-logged-in user accesses the 'create_route' view, the response status code is 200 (OK).

        Asserts:
            - Status code 200 for the response.
        """

        response = self.client.get(reverse('create_route'))
        self.assertEqual(response.status_code, 200)

    def test_create_route_non_logged_template(self):
        """
        Tests the template used for the 'create_route' view when accessed by a non-logged-in user.

        This test ensures that when a non-logged-in user accesses the 'create_route' view, the correct template ('publish/publish.html') is used.

        Asserts:
            - The 'publish/publish.html' template is used.
        """

        response = self.client.get(reverse('create_route'))
        self.assertTemplateUsed(response, 'publish/publish.html')

    def test_select_route_non_logged(self):
        """
        Tests the response for accessing the 'select_route' view as a non-logged-in user.

        This test ensures that when a non-logged-in user accesses the 'select_route' view, the response status code is 200 (OK).

        Asserts:
            - Status code 200 for the response.
        """

        response = self.client.get(reverse('select_route'))
        self.assertEqual(response.status_code, 200)

    def test_select_route_non_logged_template(self):
        """
        Tests the template used for the 'select_route' view when accessed by a non-logged-in user.

        This test ensures that when a non-logged-in user accesses the 'select_route' view, the correct template ('publish/publish.html') is used.

        Asserts:
            - The 'publish/publish.html' template is used.
        """

        response = self.client.get(reverse('select_route'))
        self.assertTemplateUsed(response, 'publish/publish.html')

    def test_publish_non_logged(self):
        """
        Tests the response for accessing the 'publish' view as a non-logged-in user.

        This test ensures that when a non-logged-in user accesses the 'publish' view, the response status code is 302 (redirect).

        Asserts:
            - Status code 302 for the response (redirect).
        """

        response = self.client.get(reverse('publish'))
        self.assertEqual(response.status_code, 302)

    def test_display_ride_non_logged(self):
        """
        Tests the response for accessing the 'display_ride' view as a non-logged-in user.

        This test ensures that when a non-logged-in user accesses the 'display_ride' view, the response status code is 200 (OK).

        Asserts:
            - Status code 200 for the response.
        """

        response = self.client.get(
            reverse('display_ride', args=["Raleigh, NC, USA"]))
        self.assertEqual(response.status_code, 200)

    def test_display_ride_non_logged_template(self):
        """
        Tests the template used for the 'display_ride' view when accessed by a non-logged-in user.

        This test ensures that when a non-logged-in user accesses the 'display_ride' view, the correct template ('publish/route.html') is used.

        Asserts:
            - The 'publish/route.html' template is used.
        """

        response = self.client.get(
            reverse('display_ride', args=["Raleigh, NC, USA"]))
        self.assertTemplateUsed(response, 'publish/route.html')
