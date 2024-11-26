import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse
from bson import ObjectId
import mongomock
from datetime import datetime
from django.contrib.auth.hashers import check_password

# Import your views module
from user import views


class userViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.mock_client = mongomock.MongoClient()
        self.mock_db = self.mock_client.SEProject

    def mock_db_setup(self):
        # Helper method to set up mock database
        self.mock_db.userData.insert_many([
            {'_id': ObjectId(), 'username': 'testuser1', 'password': 'Password@123',
             'fname': 'Test', 'lname': 'User1', 'email': 'test1@ncsu.edu', 'rides': []},
            {'_id': ObjectId(), 'username': 'testuser2', 'password': 'Password@123',
             'fname': 'Test', 'lname': 'User2', 'email': 'test2@ncsu.edu', 'rides': []}
        ])
        self.mock_db.routes.insert_many([
            {'_id': ObjectId(), 'creator': ObjectId(),
             'destination': 'New York', 'date': '2023-12-01'},
            {'_id': ObjectId(), 'creator': ObjectId(),
             'destination': 'Los Angeles', 'date': '2024-01-01'}
        ])

    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    def test_index_not_authenticated(self, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')
        self.assertIsNone(response.context['username'])

    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    def test_index_authenticated(self, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        mock_userDB = self.mock_db.userData

        session = self.client.session
        session['username'] = 'testuser1'
        session.save()

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')
        self.assertEqual(response.context['username'], 'testuser1')

    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    @patch('user.views.GoogleCloud')
    def test_register_get(self, mock_GoogleCloud, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')

    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    @patch('user.views.GoogleCloud')
    def test_register_post_valid(self, mock_GoogleCloud, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        mock_userDB = self.mock_db.userData

        post_data = {
            'username': 'newuser',
            'unityid': 'nu123',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@ncsu.edu',
            'password1': 'Test@password123',
            'password2': 'Test@password123',
            'phone_number': '1234567890'
        }
        response = self.client.post(reverse('register'), data=post_data)
        self.assertEqual(response.status_code, 302)

    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    def test_logout(self, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        session = self.client.session
        session['username'] = 'testuser1'
        session.save()

        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('index'))
        self.assertNotIn('username', self.client.session)

    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    def test_user_profile_valid(self, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        mock_userDB = self.mock_db.userData
        mock_routesDB = self.mock_db.routes

        user = mock_userDB.find_one({'username': 'testuser1'})
        user_id = str(user['_id'])

        response = self.client.get(reverse('user_profile', args=[user_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')

    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    def test_user_profile_invalid(self, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        invalid_user_id = str(ObjectId())
        response = self.client.get(
            reverse('user_profile', args=[invalid_user_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/404.html')

    # Additional test cases

    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    @patch('user.views.GoogleCloud')
    def test_register_post_invalid(self, mock_GoogleCloud, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        mock_userDB = self.mock_db.userData

        post_data = {
            'username': 'newuser',
            'unityid': 'nu123',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'invalid_email',  # Invalid email
            'password1': 'testpassword123',
            'password2': 'testpassword456',  # Passwords don't match
            'phone_number': '1234567890'
        }
        response = self.client.post(reverse('register'), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')
        self.assertEqual(mock_userDB.count_documents({}),
                         2)  # No new user added

    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    def test_user_profile_with_rides(self, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        mock_userDB = self.mock_db.userData
        mock_routesDB = self.mock_db.routes

        user = mock_userDB.find_one({'username': 'testuser1'})
        user_id = str(user['_id'])

        # Add some routes for this user
        mock_routesDB.insert_many([
            {'_id': ObjectId(), 'creator': ObjectId(user_id),
             'destination': 'Chicago', 'date': '2023-11-01'},
            {'_id': ObjectId(), 'creator': ObjectId(user_id),
             'destination': 'Miami', 'date': '2024-02-01'}
        ])

        response = self.client.get(reverse('user_profile', args=[user_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')
        self.assertTrue(len(response.context['pastrides']) > 0 or len(
            response.context['currentrides']) > 0)

    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    def test_logout(self, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        session = self.client.session
        session['username'] = 'testuser1'
        session.save()

        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('index'))
        self.assertNotIn('username', self.client.session)

    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    def test_user_profile_valid(self, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        mock_userDB = self.mock_db.userData

        user = mock_userDB.find_one({'username': 'testuser1'})
        user_id = str(user['_id'])

        response = self.client.get(reverse('user_profile', args=[user_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')

    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    def test_user_profile_invalid(self, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        invalid_user_id = str(ObjectId())
        response = self.client.get(
            reverse('user_profile', args=[invalid_user_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/404.html')

    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    def test_login_valid(self, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        mock_userDB = self.mock_db.userData
        post_data = {
            "username": "testuser1",
            "password": "Password@123"
        }

        response = self.client.post(reverse("login"), data=post_data)

        self.assertEqual(response.status_code, 200)

    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    def test_login_invalid(self, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        # Set up mocks and call the view
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        post_data = {
            "username": "invalid",
            "password": "wrongpassword"
        }

        response = self.client.post(reverse("login"), data=post_data)

        # Assertions
        assert response.status_code == 200
        assert "Invalid username or password" in str(response.content)

   # Test for rendering my rides view when user is not authenticated
    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    def test_my_rides_not_authenticated(self, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        # Set up mocks and call the view
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        response = self.client.get(reverse("myrides"))

        # Assertions
        assert response.status_code == 302

    # Test for rendering my rides view when user is authenticated
    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    def test_my_rides_authenticated(self, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        # Set up mocks and call the view
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        session = self.client.session
        session['username'] = "testuser1"
        session.save()

        response = self.client.get(reverse("myrides"))

        # Assertions
        assert response.status_code == 200
        assert "My Rides" in str(response.content)

    # Test for deleting a ride with valid ride ID
    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    def test_delete_ride_valid_id(self, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        # Set up mocks and call the view
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        ride_id = str(self.mock_db.routes.find_one({})['_id'])

        session = self.client.session
        session['username'] = "testuser1"
        session.save()

        response = self.client.post(reverse("delete_ride", args=[ride_id]))

        # Assertions
        assert response.status_code == 302  # Should redirect to my rides page

    # Test for editing user information with valid data
    @patch('user.views.get_client')
    @patch('user.views.client')
    @patch('user.views.db')
    @patch('user.views.userDB')
    @patch('user.views.ridesDB')
    @patch('user.views.routesDB')
    def test_edit_user_valid_data(self, mock_routesDB, mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        # Set up mocks and call the view
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        session = self.client.session
        session['username'] = "testuser1"
        session.save()

        post_data = {
            "first_name": "Updated",
            "last_name": "User",
            "phone_number": "9876543210"
        }

        response = self.client.post(reverse("user_user"), data=post_data)

        # Assertions
        assert response.status_code == 302


if __name__ == '__main__':
    unittest.main()
