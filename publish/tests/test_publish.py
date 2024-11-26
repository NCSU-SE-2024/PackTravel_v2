"""
This module contains test cases for views in the 'publish' application. The tests are designed to verify the behavior of the views related to routes and rides, including both authenticated and unauthenticated user interactions.

Test cases include scenarios for:
- Valid and invalid route and ride data.
- Authentication checks.
- CRUD operations on routes and rides, such as creating routes, selecting routes, and displaying ride information.
- Handling of mock database data using `mongomock`.

Dependencies:
- `unittest`: Provides the testing framework.
- `mongomock`: Mock MongoDB client for simulating MongoDB operations in tests.
- `django.test.TestCase`: Base class for writing tests that interact with Django models and views.
- `django.urls.reverse`: Used for reversing URL patterns for view testing.
"""

import unittest
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from bson import ObjectId
import mongomock
import json


class PublishViewsTestCase(TestCase):
    """
    Test suite for the views of the 'publish' application.

    This class tests the views related to rides, routes, and user interactions in the 'publish' app. It verifies that the views function as expected, handling both valid and invalid data, proper routing, and template rendering.

    Test cases cover scenarios like:
    - Displaying routes and rides.
    - Selecting and creating routes.
    - Ensuring correct behavior when users are not authenticated.
    - Handling errors when invalid data is provided.

    The tests mock database operations using `mongomock` and interact with the views via Django's test client.

    This class extends `TestCase` to enable testing Django views and responses.
    """

    def setUp(self):
        """
        Sets up the test client and mock MongoDB client for use in the tests.

        This method initializes the `self.client` for simulating HTTP requests and `self.mock_client` for simulating interactions with a MongoDB database. It is run before each individual test to prepare the test environment.
        """

        self.client = Client()
        self.mock_client = mongomock.MongoClient()
        self.mock_db = self.mock_client.SEProject

    def mock_db_setup(self):
        """
        Sets up mock data in the mock database for use in the tests.

        This method creates mock collections in the `mock_db`, inserting sample data for users, routes, and rides. The mock data is used in various test cases to simulate interactions with the database without affecting an actual MongoDB instance.
        """

        # Set up mock database collections
        self.mock_db.userData.insert_one({
            '_id': ObjectId(),
            'username': 'testuser',
            'email': 'testuser@ncsu.edu',
            'rides': []
        })
        self.mock_db.routes.insert_one({
            '_id': ObjectId(),
            'creator': ObjectId(),
            'destination': 'New York',
            'users': [],
            'distance': 20.5
        })
        self.mock_db.rides.insert_one({
            '_id': 'ride_1',
            'destination': 'New York',
            'route_id': [ObjectId()]
        })

    @patch('publish.views.get_client')
    def test_publish_index_not_authenticated(self, mock_get_client):
        """
        Tests the behavior of the index view when the user is not authenticated.

        This test ensures that the index view returns a 200 OK response and does not redirect or require authentication for unauthenticated users.

        Asserts:
            - Status code 200 for the response.
        """

        mock_get_client.return_value = self.mock_client
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    @patch('publish.views.get_client')
    def test_publish_index_authenticated(self, mock_get_client):
        """
        Tests the behavior of the index view when the user is authenticated.

        This test simulates an authenticated user by setting the session with a username. It ensures that the index view returns a 200 OK response and uses the correct template for authenticated users.

        Asserts:
            - Status code 200 for the response.
            - Template 'home/home.html' is used for authenticated users.
        """

        mock_get_client.return_value = self.mock_client
        session = self.client.session
        session['username'] = 'testuser'
        session.save()

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

    @patch('publish.views.get_client')
    def test_display_ride_valid(self, mock_get_client):
        """
        Tests the behavior of the 'display_ride' view with valid ride data.

        This test ensures that when valid ride data is provided (after mock data setup), the `display_ride` view renders the correct template and returns a 200 OK response.

        Asserts:
            - Status code 200 for the response.
            - Template 'publish/route.html' is used.
        """

        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        session = self.client.session
        session['username'] = 'testuser'
        session.save()

        ride_id = str(self.mock_db.rides.find_one({})['_id'])
        response = self.client.get(reverse('display_ride', args=[ride_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publish/route.html')

    @patch('publish.views.get_client')
    def test_display_ride_invalid(self, mock_get_client):
        """
        Tests the behavior of the 'display_ride' view with invalid ride data.

        This test simulates a case where an invalid ride ID is passed to the `display_ride` view, expecting the view to raise a `TypeError`.

        Asserts:
            - A `TypeError` is raised for invalid ride ID.
        """

        mock_get_client.return_value = self.mock_client
        with self.assertRaises(TypeError):
            self.client.get(reverse('display_ride', args=['invalid_id']))

    @patch('publish.views.get_client')
    def test_select_route_post_valid(self, mock_get_client):
        """
        Tests the behavior of the 'select_route' view with valid POST data.

        This test ensures that when valid data is submitted for selecting a route (after mock data setup), the view processes the data correctly and redirects the user to the 'display_ride' view.

        Asserts:
            - The response redirects to the 'display_ride' view.
        """

        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        session = self.client.session
        session['username'] = 'testuser'
        session['email'] = 'testuser@ncsu.edu'
        session.save()

        route_id = str(self.mock_db.routes.find_one({})['_id'])
        ride_data = json.dumps({'_id': 'ride_1'})

        post_data = {
            'hiddenInput': route_id,
            'hiddenUser': 'testuser',
            'hiddenRide': ride_data
        }

        response = self.client.post(reverse('select_route'), data=post_data)
        self.assertRedirects(response, reverse(
            'display_ride', args=['ride_1']))

    @patch('publish.views.get_client')
    def test_select_route_post_invalid(self, mock_get_client):
        """
        Tests the behavior of the 'select_route' view with invalid POST data.

        This test ensures that when invalid or empty data is submitted to the `select_route` view, the view responds with a 400 error.

        Asserts:
            - Status code 400 for the response.
        """

        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        post_data = {'hiddenInput': '', 'hiddenUser': '', 'hiddenRide': ''}

        response = self.client.post(reverse('select_route'), data=post_data)
        # Assuming 400 for invalid data
        self.assertEqual(response.status_code, 400)

    @patch('publish.views.get_client')
    def test_create_route_post(self, mock_get_client):
        """
        Tests the behavior of the 'create_route' view with valid POST data.

        This test ensures that when valid data is submitted to create a route, the view processes the data correctly and redirects the user to the 'display_ride' view for the newly created route.

        Asserts:
            - The response redirects to the 'display_ride' view.
        """

        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        session = self.client.session
        session['username'] = 'testuser'
        session.save()

        post_data = {
            'purpose': 'Work',
            's_point': 'Point A',
            'destination': 'New York',
            'date': '2024-11-30',
            'hour': '10',
            'minute': '30',
            'ampm': 'AM',
            'details': 'This is a test route',
            'slat': '35.7796',
            'slong': '-78.6382',
            'dlat': '40.7128',
            'dlong': '-74.0060'
        }

        response = self.client.post(reverse('create_route'), data=post_data)
        self.assertRedirects(response, reverse(
            'display_ride', args=['New York']))

    @patch('publish.views.get_client')
    def test_packs_favorite(self, mock_get_client):
        """
        Tests the behavior of the 'packs_favorite' view.

        This test ensures that when the 'packs_favorite' view is accessed, it returns a 200 OK response, uses the correct template, and includes the 'top_picks' context data.

        Asserts:
            - Status code 200 for the response.
            - Template 'publish/packs_favorite.html' is used.
            - 'top_picks' is present in the response context.
        """

        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        response = self.client.get(reverse('packs_favorite'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publish/packs_favorite.html')
        self.assertIn('top_picks', response.context)
