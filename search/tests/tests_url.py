"""
Test cases for the URL resolution of the search index view in the SEProject Django application.

This module contains a unit test for verifying that the URL for the `search` view correctly resolves
to the `search_index` view function. It ensures that the URL pattern for `search` is properly configured
and resolves to the correct view function, `search_index`.

Tested components:
- URL resolution for the `search` view
- Mapping of the URL to the `search_index` view function

Dependencies:
- Django SimpleTestCase for testing URL resolution
- Django's reverse and resolve functions for URL pattern resolution
"""

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from search.views import search_index


class TestUrl(SimpleTestCase):
    """
    Test case for verifying the URL resolution of the search index view.

    This class contains a test method to ensure that the URL for the `search` view correctly resolves
    to the `search_index` view function.
    """

    def test_search_index_resolved(self):
        """
        Test that the `search` URL resolves to the `search_index` view function.

        This method uses Django's `reverse` function to get the URL for the `search` view and then
        uses the `resolve` function to ensure that the correct view function (`search_index`) is
        associated with the URL.

        Asserts:
            The URL resolves to the `search_index` view function.
        """
        url = reverse("search")
        self.assertEquals(resolve(url).func, search_index)
