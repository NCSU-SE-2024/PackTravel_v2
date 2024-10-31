from django.test import SimpleTestCase
from django.urls import reverse, resolve
from search.views import search_index


class TestUrl(SimpleTestCase):

    def test_search_index_resolved(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, search_index)