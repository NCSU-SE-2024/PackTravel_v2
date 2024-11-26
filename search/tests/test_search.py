import unittest
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from bson import ObjectId
import mongomock
from datetime import datetime


class SearchViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.mock_client = mongomock.MongoClient()
        self.mock_db = self.mock_client.SEProject

    def mock_db_setup(self):
        # Set up mock database collections
        self.mock_db.userData.insert_one({
            '_id': ObjectId(),
            'username': 'testuser',
            'email': 'testuser@ncsu.edu',
            'rides': []
        })
        self.mock_db.rides.insert_many([
            {
                '_id': 'ride_1',
                'destination': 'New York, NY, USA',
                'route_id': ['route_1_NY_2024-11-25'],
            },
            {
                '_id': 'ride_2',
                'destination': 'Los Angeles, CA, USA',
                'route_id': ['route_2_CA_2023-11-20'],
            }
        ])
        self.mock_db.routes.insert_many([
            {
                '_id': 'route_1_NY_USA_2024-11-25',
                'creator': ObjectId(),
                'destination': 'New York, NY, USA',
                'date': '2024-11-25',
            },
            {
                '_id': 'route_2_CA_USA_2023-11-20',
                'creator': ObjectId(),
                'destination': 'Los Angeles, CA, USA',
                'date': '2023-11-20',
            },
        ])

    @patch('search.views.get_client')
    def test_search_index_not_authenticated(self, mock_get_client):
        """
        Test the behavior of search_index when the user is not authenticated.
        """
        mock_get_client.return_value = self.mock_client

        response = self.client.get(reverse('search'))
        self.assertRedirects(response, reverse('index'))

    @patch('search.views.get_client')
    def test_search_index_authenticated_no_rides(self, mock_get_client):
        """
        Test the behavior of search_index for an authenticated user when no rides exist.
        """
        mock_get_client.return_value = self.mock_client
        session = self.client.session
        session['username'] = 'testuser'
        session.save()

        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search.html')
        self.assertEqual(len(response.context['rides']), 0)

    @patch('search.views.get_client')
    @patch('search.views.DateUtils')
    def test_search_index_authenticated_with_rides(self, mock_date_utils, mock_get_client):
        """
        Test the behavior of search_index for an authenticated user when rides exist.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        mock_date_utils.has_date_passed.side_effect = lambda date: datetime.strptime(
            date, '%Y-%m-%d') < datetime.now()

        session = self.client.session
        session['username'] = 'testuser'
        session.save()

        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search.html')
        self.assertIn('rides', response.context)
        self.assertGreater(len(response.context['rides']), 0)

    @patch('search.views.get_client')
    @patch('search.views.DateUtils')
    def test_search_index_route_date_handling(self, mock_date_utils, mock_get_client):
        """
        Test if search_index correctly handles expired and upcoming routes.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        # Simulate one expired date and one future date
        mock_date_utils.has_date_passed.side_effect = lambda date: date == '2023-11-20'

        session = self.client.session
        session['username'] = 'testuser'
        session.save()

        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        rides = response.context['rides']

        # Ensure route count is calculated correctly
        for ride in rides:
            if ride['destination'] == 'New York':
                self.assertEqual(ride['count'], 1)  # Upcoming route
            elif ride['destination'] == 'Los Angeles':
                self.assertEqual(ride['count'], 0)  # Expired route
