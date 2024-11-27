"""
This module contains unit tests for the `user` app in a Django project.
The tests focus on verifying the behavior of view functions, URL routing,
and database interactions using a mock MongoDB instance (`mongomock`).

Key functionalities tested include:
- Setting up mock databases and connections for isolation from the production database.
- Ensuring views respond with the correct status codes and render the appropriate templates.
- Validating the integration of user-related functionality such as login, profile, and ride management.

Test framework: `unittest` with Django's `TestCase` and mock utilities.
"""

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
    """
    Test case class for testing views related to user functionality in the application.
    """

    def setUp(self):
        """
        Sets up the test client and mock database connection for the test cases.
        """
        self.client = Client()
        self.mock_client = mongomock.MongoClient()
        self.mock_db = self.mock_client.SEProject

    def mock_db_setup(self):
        """
        Populates the mock database with sample user and route data for testing.
        """
        self.mock_db.userData.insert_many(
            [
                {
                    "_id": ObjectId(),
                    "username": "testuser1",
                    "password": "Password@123",
                    "fname": "Test",
                    "lname": "User1",
                    "email": "test1@ncsu.edu",
                    "rides": [],
                },
                {
                    "_id": ObjectId(),
                    "username": "testuser2",
                    "password": "Password@123",
                    "fname": "Test",
                    "lname": "User2",
                    "email": "test2@ncsu.edu",
                    "rides": [],
                },
            ]
        )
        self.mock_db.routes.insert_many(
            [
                {
                    "_id": ObjectId(),
                    "creator": ObjectId(),
                    "destination": "New York",
                    "date": "2023-12-01",
                },
                {
                    "_id": ObjectId(),
                    "creator": ObjectId(),
                    "destination": "Los Angeles",
                    "date": "2024-01-01",
                },
            ]
        )

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    def test_index_not_authenticated(
        self,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Tests the behavior of the 'index' view when the user is not authenticated.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/home.html")
        self.assertIsNone(response.context["username"])

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    def test_index_authenticated(
        self,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Tests the behavior of the 'index' view when the user is authenticated.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        mock_userDB = self.mock_db.userData

        session = self.client.session
        session["username"] = "testuser1"
        session.save()

        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/home.html")
        self.assertEqual(response.context["username"], "testuser1")

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    @patch("user.views.GoogleCloud")
    def test_register_get(
        self,
        mock_GoogleCloud,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Tests the 'register' view for GET requests to ensure the registration page is rendered.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/register.html")

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    @patch("user.views.GoogleCloud")
    def test_register_post_valid(
        self,
        mock_GoogleCloud,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Tests the 'register' view for POST requests with valid data to ensure successful user registration.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        mock_userDB = self.mock_db.userData

        post_data = {
            "username": "newuser",
            "unityid": "nu123",
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@ncsu.edu",
            "password1": "Test@password123",
            "password2": "Test@password123",
            "phone_number": "1234567890",
        }
        response = self.client.post(reverse("register"), data=post_data)
        self.assertEqual(response.status_code, 302)

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    def test_logout(
        self,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Tests the 'logout' view to ensure users are successfully logged out.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        session = self.client.session
        session["username"] = "testuser1"
        session.save()

        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("index"))
        self.assertNotIn("username", self.client.session)

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    def test_user_profile_valid(
        self,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Tests the 'user_profile' view for a valid user to ensure profile data is displayed correctly.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        mock_userDB = self.mock_db.userData
        mock_routesDB = self.mock_db.routes

        user = mock_userDB.find_one({"username": "testuser1"})
        user_id = str(user["_id"])

        response = self.client.get(reverse("user_profile", args=[user_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/profile.html")

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    def test_user_profile_invalid(
        self,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Tests the 'user_profile' view for an invalid user ID to ensure a 404 page is displayed.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        invalid_user_id = str(ObjectId())
        response = self.client.get(
            reverse(
                "user_profile",
                args=[invalid_user_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/404.html")

    # Additional test cases

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    @patch("user.views.GoogleCloud")
    def test_register_post_invalid(
        self,
        mock_GoogleCloud,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Tests the 'register' view for POST requests with invalid data to ensure proper error handling.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        mock_userDB = self.mock_db.userData

        post_data = {
            "username": "newuser",
            "unityid": "nu123",
            "first_name": "New",
            "last_name": "User",
            "email": "invalid_email",  # Invalid email
            "password1": "testpassword123",
            "password2": "testpassword456",  # Passwords don't match
            "phone_number": "1234567890",
        }
        response = self.client.post(reverse("register"), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/register.html")
        self.assertEqual(
            mock_userDB.count_documents(
                {}), 2)  # No new user added

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    def test_user_profile_with_rides(
        self,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Test the user profile view with rides.
        Ensures that the correct template is used and that the response includes
        past or current rides when valid data is present.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        mock_userDB = self.mock_db.userData
        mock_routesDB = self.mock_db.routes

        user = mock_userDB.find_one({"username": "testuser1"})
        user_id = str(user["_id"])

        # Add some routes for this user
        mock_routesDB.insert_many(
            [
                {
                    "_id": ObjectId(),
                    "creator": ObjectId(user_id),
                    "destination": "Chicago",
                    "date": "2023-11-01",
                },
                {
                    "_id": ObjectId(),
                    "creator": ObjectId(user_id),
                    "destination": "Miami",
                    "date": "2024-02-01",
                },
            ]
        )

        response = self.client.get(reverse("user_profile", args=[user_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/profile.html")
        self.assertTrue(
            len(response.context["pastrides"]) > 0
            or len(response.context["currentrides"]) > 0
        )

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    def test_logout(
        self,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Test the logout functionality.
        Ensures that the session is cleared, and the user is redirected to the index page.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        session = self.client.session
        session["username"] = "testuser1"
        session.save()

        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("index"))
        self.assertNotIn("username", self.client.session)

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    def test_user_profile_valid(
        self,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Test the user profile view with a valid user ID.
        Ensures that the correct template is used, and the response is successful.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        mock_userDB = self.mock_db.userData

        user = mock_userDB.find_one({"username": "testuser1"})
        user_id = str(user["_id"])

        response = self.client.get(reverse("user_profile", args=[user_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/profile.html")

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    def test_user_profile_invalid(
        self,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Test the user profile view with an invalid user ID.
        Ensures that the 404 template is used and the response is successful.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        invalid_user_id = str(ObjectId())
        response = self.client.get(
            reverse(
                "user_profile",
                args=[invalid_user_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/404.html")

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    def test_login_valid(
        self,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Test the login view with valid credentials.
        Ensures that the response is successful.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        mock_userDB = self.mock_db.userData
        post_data = {"username": "testuser1", "password": "Password@123"}

        response = self.client.post(reverse("login"), data=post_data)

        self.assertEqual(response.status_code, 200)

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    def test_login_invalid(
        self,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Test the login view with invalid credentials.
        Ensures that an error message is returned in the response.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        post_data = {"username": "invalid", "password": "wrongpassword"}

        response = self.client.post(reverse("login"), data=post_data)

        # Assertions
        assert response.status_code == 200
        assert "Invalid username or password" in str(response.content)

    # Test for rendering my rides view when the user is not authenticated
    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    def test_my_rides_not_authenticated(
        self,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Test the my rides view for unauthenticated users.
        Ensures that the user is redirected to the login page (HTTP 302).
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        response = self.client.get(reverse("myrides"))

        # Assertions
        assert response.status_code == 302

    # Test for rendering my rides view when the user is authenticated

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    def test_my_rides_authenticated(
        self,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Test the my rides view for authenticated users.
        Ensures that the response renders the correct page with the user's rides.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        session = self.client.session
        session["username"] = "testuser1"
        session.save()

        response = self.client.get(reverse("myrides"))

        # Assertions
        assert response.status_code == 200
        assert "My Rides" in str(response.content)

    # Test for deleting a ride with a valid ride ID

    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    def test_delete_ride_valid_id(
        self,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Test deleting a ride with a valid ride ID.
        Ensures that the ride is deleted and the user is redirected to the my rides page (HTTP 302).
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        ride_id = str(self.mock_db.routes.find_one({})["_id"])

        session = self.client.session
        session["username"] = "testuser1"
        session.save()

        response = self.client.post(reverse("delete_ride", args=[ride_id]))

        # Assertions
        assert response.status_code == 302  # Should redirect to my rides page

    # Test for editing user information with valid data
    @patch("user.views.get_client")
    @patch("user.views.client")
    @patch("user.views.db")
    @patch("user.views.userDB")
    @patch("user.views.ridesDB")
    @patch("user.views.routesDB")
    def test_edit_user_valid_data(
        self,
        mock_routesDB,
        mock_ridesDB,
        mock_userDB,
        mock_db,
        mock_client,
        mock_get_client,
    ):
        """
        Test editing user information with valid data.
        Ensures that the user information is updated and the user is redirected appropriately (HTTP 302).
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        session = self.client.session
        session["username"] = "testuser1"
        session.save()

        post_data = {
            "first_name": "Updated",
            "last_name": "User",
            "phone_number": "9876543210",
        }

        response = self.client.post(reverse("user_user"), data=post_data)

        # Assertions
        assert response.status_code == 302


if __name__ == "__main__":
    unittest.main()
