import unittest
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from bson import ObjectId
import mongomock
import json

class PublishViewsTestCase(TestCase):
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
        mock_get_client.return_value = self.mock_client
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    @patch('publish.views.get_client')
    def test_publish_index_authenticated(self, mock_get_client):
        mock_get_client.return_value = self.mock_client
        session = self.client.session
        session['username'] = 'testuser'
        session.save()

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

    @patch('publish.views.get_client')
    def test_display_ride_valid(self, mock_get_client):
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
        mock_get_client.return_value = self.mock_client
        with self.assertRaises(TypeError):
            self.client.get(reverse('display_ride', args=['invalid_id']))

    @patch('publish.views.get_client')
    def test_select_route_post_valid(self, mock_get_client):
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
        self.assertRedirects(response, reverse('display_ride', args=['ride_1']))

    @patch('publish.views.get_client')
    def test_select_route_post_invalid(self, mock_get_client):
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        post_data = {'hiddenInput': '', 'hiddenUser': '', 'hiddenRide': ''}

        response = self.client.post(reverse('select_route'), data=post_data)
        self.assertEqual(response.status_code, 400)  # Assuming 400 for invalid data

    @patch('publish.views.get_client')
    def test_create_route_post(self, mock_get_client):
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
        self.assertRedirects(response, reverse('display_ride', args=['New York']))

    @patch('publish.views.get_client')
    def test_packs_favorite(self, mock_get_client):
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        response = self.client.get(reverse('packs_favorite'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publish/packs_favorite.html')
        self.assertIn('top_picks', response.context)
