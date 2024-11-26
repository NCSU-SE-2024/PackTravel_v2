"""
Unit tests for the `forum` module in the Django project.

This module contains test cases to verify the functionality of forum views,
including creating topics, adding comments, and retrieving topics and comments
associated with specific rides. Mocked MongoDB is used to simulate database interactions.
"""
import unittest
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from bson import ObjectId
import mongomock
from datetime import datetime

# Import your views module
from forum import views


class ForumViewsTestCase(TestCase):
    """
    Test cases for views in the `forum` application.

    This test class uses Django's TestCase to simulate HTTP requests and responses
    and verifies the expected behavior of views with various inputs and conditions.
    MongoDB collections are mocked to simulate database interactions.
    """
    def setUp(self):
        """
        Sets up the test client and a mocked MongoDB instance for use in tests.
        """
        self.client = Client()
        self.mock_client = mongomock.MongoClient()
        self.mock_db = self.mock_client.SEProject

    def mock_db_setup(self):
        """
        Initializes mock database collections with sample data for testing.
        """
        # Helper method to set up mock database
        self.mock_db.routes.insert_many([
            {'_id': ObjectId(), 'destination': 'New York'},
            {'_id': ObjectId(), 'destination': 'Los Angeles'}
        ])
        self.mock_db.topics.insert_many([
            {'_id': ObjectId(), 'ride_id': 'New York', 'title': 'Topic 1',
             'content': 'Content 1', 'creator': 'user1', 'created_at': datetime.now()},
            {'_id': ObjectId(), 'ride_id': 'Los Angeles', 'title': 'Topic 2',
             'content': 'Content 2', 'creator': 'user2', 'created_at': datetime.now()}
        ])
        self.mock_db.comments.insert_many([
            {'_id': ObjectId(), 'topic_id': ObjectId(), 'content': 'Comment 1',
             'creator': 'user3', 'created_at': datetime.now()}
        ])

    @patch('forum.views.get_client')
    @patch('forum.views.client')
    @patch('forum.views.db')
    @patch('forum.views.userDB')
    @patch('forum.views.ridesDB')
    @patch('forum.views.routesDB')
    @patch('forum.views.topicsDB')
    @patch('forum.views.commentsDB')
    def test_rides_with_topics(self, mock_commentsDB, mock_topicsDB, mock_routesDB,
                               mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        """
        Tests the `rides_with_topics` view for rendering the rides and their associated topics.

        Args:
            mock_commentsDB: Mock for the comments database collection.
            mock_topicsDB: Mock for the topics database collection.
            mock_routesDB: Mock for the routes database collection.
            mock_ridesDB: Mock for the rides database collection.
            mock_userDB: Mock for the user database collection.
            mock_db: Mock for the database.
            mock_client: Mock for the MongoDB client.
            mock_get_client: Mock for the `get_client` function.

        Asserts:
            The response status code is 200.
            The correct template is rendered.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        response = self.client.get(reverse('rides_with_topics'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/rides_with_topics.html')

    @patch('forum.views.get_client')
    @patch('forum.views.client')
    @patch('forum.views.db')
    @patch('forum.views.userDB')
    @patch('forum.views.ridesDB')
    @patch('forum.views.routesDB')
    @patch('forum.views.topicsDB')
    @patch('forum.views.commentsDB')
    def test_create_topic_get(self, mock_commentsDB, mock_topicsDB, mock_routesDB,
                              mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        """
        Tests the `create_topic` view when accessed with a GET request.

        Args:
            mock_commentsDB: Mock for the comments database collection.
            mock_topicsDB: Mock for the topics database collection.
            mock_routesDB: Mock for the routes database collection.
            mock_ridesDB: Mock for the rides database collection.
            mock_userDB: Mock for the user database collection.
            mock_db: Mock for the database.
            mock_client: Mock for the MongoDB client.
            mock_get_client: Mock for the `get_client` function.

        Asserts:
            The response status code is 200.
            The correct template is rendered.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        response = self.client.get(reverse('create_topic'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/create_topic.html')

    @patch('forum.views.get_client')
    @patch('forum.views.client')
    @patch('forum.views.db')
    @patch('forum.views.userDB')
    @patch('forum.views.ridesDB')
    @patch('forum.views.routesDB')
    @patch('forum.views.topicsDB')
    @patch('forum.views.commentsDB')
    def test_create_topic_post(self, mock_commentsDB, mock_topicsDB, mock_routesDB,
                               mock_ridesDB, mock_userDB, mock_db, mock_client, mock_get_client):
        """
        Test the 'create_topic' view for POST requests.

        Simulates posting data to create a new topic and verifies:
        - A successful redirection to the 'rides_with_topics' view.
        - The topic count in the mock database increases.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client

        session = self.client.session
        session['username'] = 'testuser'
        session.save()

        post_data = {
            'ride_id': 'New York',
            'title': 'New Topic',
            'content': 'New Content'
        }
        response = self.client.post(reverse('create_topic'), data=post_data)
        self.assertRedirects(response, reverse('rides_with_topics'))
        self.assertEqual(self.mock_db.topics.count_documents({}), 3)

    @patch('forum.views.get_client')
    @patch('forum.views.client')
    @patch('forum.views.db')
    @patch('forum.views.userDB')
    @patch('forum.views.ridesDB')
    @patch('forum.views.routesDB')
    @patch('forum.views.topicsDB')
    def test_add_comment_get(self, mock_commentsDB, mock_topicsDB,
                             mock_ridesDb, mock_userDb, mock_Db, mock_client, mock_get_client):
        """
        Test the 'add_comment' view for GET requests.

        Mocks the database client and verifies:
        - The view redirects successfully.
        """

        # Set up mocks and call the view
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        topic_id = str(self.mock_db.topics.find_one({})['_id'])
        response = self.client.get(reverse("add_comment", args=[topic_id]))
        # Assertions
        assert response.status_code == 302

    # Test for displaying a specific topic and its associated comments
    @patch('forum.views.get_client')
    @patch('forum.views.client')
    @patch('forum.views.db')
    @patch('forum.views.userDB')
    @patch('forum.views.ridesDB')
    @patch('forum.views.routesDB')
    @patch('forum.views.topicsDB')
    def test_forum_topic_details(self, mock_commentsDB, mock_topicsDB,
                                 mock_ridesDb, mock_userDb, mock_Db, mock_client, mock_get_client):
        """
        Test the 'forum_topic_details' view.

        Verifies that the view:
        - Returns a 200 status code.
        - Displays content associated with the specified topic.
        """
        # Set up mocks and call the view
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        topic_id = str(self.mock_db.topics.find_one({})['_id'])
        response = self.client.get(
            reverse("forum_topic_details", args=[topic_id]))
        # Assertions
        assert response.status_code == 200
        assert "Content 1" in str(response.content)

    # Test for adding a comment to a specific topic with valid data
    @patch('forum.views.get_client')
    @patch('forum.views.client')
    @patch('forum.views.db')
    @patch('forum.views.userDB')
    @patch('forum.views.ridesDB')
    @patch('forum.views.routesDB')
    @patch('forum.views.topicsDB')
    def test_add_comment_post_valid_data(self, mock_commentsDB, mock_topicsDB,
                                         mock_ridesDb, mock_userDb, mock_Db, mock_client, mock_get_client):
        """
        Test adding a comment with valid data via POST request.

        Verifies that:
        - The view redirects after successful addition.
        - The comment count in the mock database increases.
        """
        # Set up mocks and call the view
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        topic_id = str(self.mock_db.topics.find_one({})['_id'])
        session = self.client.session
        session['username'] = 'testuser'
        session.save()

        post_data = {'content': 'This is a comment'}
        response = self.client.post(
            reverse("add_comment", args=[topic_id]), data=post_data)

        # Assertions
        assert response.status_code == 302  # Redirects after successful comment addition
        assert self.mock_db.comments.count_documents(
            {}) == 2  # One comment added

    # Test for adding a comment to a specific topic with invalid data
    @patch('forum.views.get_client')
    @patch('forum.views.client')
    @patch('forum.views.db')
    @patch('forum.views.userDB')
    @patch('forum.views.ridesDB')
    @patch('forum.views.routesDB')
    @patch('forum.views.topicsDB')
    def test_add_comment_post_invalid_data(self, mock_commentsDB, mock_topicsDB,
                                           mock_ridesDb, mock_userDb, mock_Db, mock_client, mock_get_client):
        """
        Test adding a comment with invalid data via POST request.

        Verifies that:
        - The view redirects after unsuccessful addition.
        """
        # Set up mocks and call the view
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        topic_id = str(self.mock_db.topics.find_one({})['_id'])
        post_data = {'content': ''}

        response = self.client.post(
            reverse("add_comment", args=[topic_id]), data=post_data)

        # Assertions
        assert response.status_code == 302

    # Test for creating a topic without providing necessary information
    @patch('forum.views.get_client')
    @patch('forum.views.client')
    @patch('forum.views.db')
    @patch('forum.views.userDB')
    @patch('forum.views.ridesDB')
    @patch('forum.views.routesDB')
    @patch('forum.views.topicsDB')
    def test_create_topic_post_invalid_data(self, mock_commentsDB, mock_topicsDB,
                                            mock_ridesDb, mock_userDb, mock_Db, mock_client, mock_get_client):
        """
        Test creating a topic with invalid data via POST request.

        Verifies that:
        - The view renders the same page with a 200 status code.
        """
        # Set up mocks and call the view
        post_data = {
            "ride_id": "",
            "title": "",
            "content": ""
        }
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        response = self.client.post(reverse("create_topic"), data=post_data)

        # Assertions
        assert response.status_code == 200

    # Test for displaying rides when there are no rides available
    @patch('forum.views.get_client')
    @patch('forum.views.client')
    @patch('forum.views.db')
    @patch('forum.views.userDB')
    @patch('forum.views.ridesDB')
    @patch('forum.views.routesDB')
    @patch('forum.views.topicsDB')
    def test_rides_with_no_available_rides(self, mock_commentsDB, mock_topicsDB,
                                           mock_ridesDb, mock_userDb, mock_Db, mock_client, mock_get_client):
        """
        Test the 'rides_with_topics' view when no rides are available.

        Clears the routes collection in the mock database and verifies:
        - The view renders successfully with a 200 status code.
        """
        # Clear routes collection to simulate no rides available
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        self.mock_db.routes.delete_many({})

        # Call the view
        response = self.client.get(reverse("rides_with_topics"))

        assert response.status_code == 200

    # Test for displaying topics when there are no topics available
    @patch('forum.views.get_client')
    @patch('forum.views.client')
    @patch('forum.views.db')
    @patch('forum.views.userDB')
    @patch('forum.views.ridesDB')
    @patch('forum.views.routesDB')
    @patch('forum.views.topicsDB')
    def test_forum_topics_no_available_topics(self, mock_commentsDB, mock_topicsDB,
                                              mock_ridesDb, mock_userDb, mock_Db, mock_client, mock_get_client):
        """
        Test the 'forum_topics' view when no topics are available.

        Clears the topics collection in the mock database and verifies:
        - The view renders successfully with a 200 status code.
        """
        # Clear topics collection to simulate no topics available
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        self.mock_db.topics.delete_many({})

        response = self.client.get(reverse("forum_topics", args=["New York"]))

        assert response.status_code == 200

    # Test for displaying topic details when no comments are available
    @patch('forum.views.get_client')
    @patch('forum.views.client')
    @patch('forum.views.db')
    @patch('forum.views.userDB')
    @patch('forum.views.ridesDB')
    @patch('forum.views.routesDB')
    @patch('forum.views.topicsDB')
    def test_forum_topic_details_no_comments(self, mock_commentsDB, mock_topicsDB,
                                             mock_ridesDb, mock_userDb, mock_Db, mock_client, mock_get_client):
        """
        Test the 'forum_topic_details' view when no comments are available.

        Verifies that the view:
        - Renders successfully with a 200 status code.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        topic_id = str(self.mock_db.topics.find_one({})['_id'])
        response = self.client.get(
            reverse("forum_topic_details", args=[topic_id]))

        assert response.status_code == 200

    # Test for forum topics page with multiple topics
    @patch('forum.views.get_client')
    @patch('forum.views.client')
    @patch('forum.views.db')
    @patch('forum.views.userDB')
    @patch('forum.views.ridesDB')
    @patch('forum.views.routesDB')
    @patch('forum.views.topicsDB')
    def test_forum_multiple_topics(self, mock_commentsDB, mock_topicsDB,
                                   mock_ridesDb, mock_userDb, mock_Db, mock_client, mock_get_client):
        """
        Test the 'forum_topics' view with multiple topics.

        Inserts additional topics into the mock database and verifies:
        - The view displays the topics correctly.
        - Returns a 200 status code.
        """
        topic1 = {'_id': ObjectId(), 'ride_id': 'New York', 'title': 'Topic 3',
                  'content': 'Content 3', 'creator': 'user3',
                  'created_at': datetime.now()}
        topic2 = {'_id': ObjectId(), 'ride_id': 'New York', 'title': 'Topic 4',
                  'content': 'Content 4', 'creator': 'user4',
                  'created_at': datetime.now()}
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        self.mock_db.topics.insert_many([topic1, topic2])

        response = self.client.get(reverse("forum_topics", args=["New York"]))

        assert response.status_code == 200
        assert "Topic 3" in str(response.content)
        assert "Topic 4" in str(response.content)

    # Test for adding multiple comments to a topic
    # @patch('forum.views.get_client')
    @patch('forum.views.get_client')
    @patch('forum.views.client')
    @patch('forum.views.db')
    @patch('forum.views.userDB')
    @patch('forum.views.ridesDB')
    @patch('forum.views.routesDB')
    @patch('forum.views.topicsDB')
    def test_add_multiple_comments_to_topic(self, mock_commentsDB, mock_topicsDB,
                                            mock_ridesDb, mock_userDb, mock_Db, mock_client, mock_get_client):
        """
        Test adding multiple comments to a topic.

        This test verifies that:
        - Multiple comments can be added to a single topic.
        - The total comment count for the topic increases correctly.
        
        Steps:
        1. Setup the mock database and initialize a topic.
        2. Simulate a user session and add two comments to the topic via POST requests.
        3. Verify that the comment count in the mock database matches the expected value.
        """
        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        topic_id = str(self.mock_db.topics.find_one({})['_id'])

        session = self.client.session
        session['username'] = "testuser"
        session.save()

        post_data1 = {'content': 'First comment'}
        post_data2 = {'content': 'Second comment'}

        self.client.post(reverse("add_comment", args=[
                         topic_id]), data=post_data1)
        self.client.post(reverse("add_comment", args=[
                         topic_id]), data=post_data2)

        comments_count = self.mock_db.comments.count_documents(
            {'topic_id': ObjectId(topic_id)})

        assert comments_count == 2  # One original + two new comments

    # Test for redirecting to forum topics page after creating a new topic
    def test_create_topic_redirects_to_forum_topics(self):
        """
        Test the redirection after creating a new topic.

        This test ensures that:
        - After successfully creating a topic, the user is redirected to the forum topics page.
        
        Steps:
        1. Simulate a user session.
        2. Submit a valid POST request to create a new topic.
        3. Verify that the response status code indicates a redirection (302).
        """
        session = self.client.session
        session['username'] = "testuser"
        session.save()

        post_data = {
            "ride_id": "New York",
            "title": "Another Topic",
            "content": "Some content"
        }

        response = self.client.post(reverse("create_topic"), data=post_data)

        assert response.status_code == 302  # Should redirect after creation

    # Test for creating a topic with an invalid ride ID
    @patch('forum.views.get_client')
    @patch('forum.views.client')
    @patch('forum.views.db')
    @patch('forum.views.userDB')
    @patch('forum.views.ridesDB')
    @patch('forum.views.routesDB')
    @patch('forum.views.topicsDB')
    def test_create_topic_invalid_ride_id(self, mock_commentsDB, mock_topicsDB,
                                          mock_ridesDb, mock_userDb, mock_Db, mock_client, mock_get_client):
        """
        Test creating a topic with an invalid ride ID.

        This test checks the behavior when attempting to create a topic using an invalid ride ID.
        
        Steps:
        1. Setup the mock database and initialize a user session.
        2. Submit a POST request with invalid ride ID data to create a topic.
        3. Verify that the response status code is 200, indicating the page reloads with the form.
        """

        self.mock_db_setup()
        mock_get_client.return_value = self.mock_client
        session = self.client.session
        session['username'] = "testuser"
        session.save()

        post_data = {
            "ride_id": "",
            "title": "Invalid Topic",
            "content": "Some content"
        }

        response = self.client.post(reverse("create_topic"), data=post_data)

        assert response.status_code == 200

    if __name__ == '__main__':
        unittest.main()
