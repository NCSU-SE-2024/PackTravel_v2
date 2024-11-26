"""
This module contains unit tests for Django form validation in the `user` app.
The tests ensure that forms correctly validate the input data and provide appropriate error messages for invalid cases.

Forms tested:
- RegisterForm: Handles user registration.
- LoginForm: Handles user login.
- EditUserForm: Handles editing user profile details.

Test framework: Django's `TransactionTestCase`.
"""

from django.test import TransactionTestCase
from user.forms import RegisterForm, LoginForm, EditUserForm


class TestForms(TransactionTestCase):
    """
    Test case class for validating user-related forms in the application.
    """

    def test_registerForm_validData(self):
        """
        Test that the RegisterForm is valid when all required fields are provided with valid data.
        """
        form = RegisterForm(data={
            'username': 'John',
            'unityid': 'ajohn6',
            'first_name': 'John',
            'last_name': 'Dwyer',
            'email': 'jdwyer@ncsu.edu',
            'password1': 'Jd!456789',
            'password2': 'Jd!456789',
            'phone_number': 9876578901,
        })
        self.assertTrue(form.is_valid())

    def test_registerForm_missingID(self):
        """
        Test that the RegisterForm is invalid when the 'unityid' field is missing.
        Ensures that the form returns an error for the 'unityid' field.
        """
        form = RegisterForm(data={
            'username': 'John',
            'unityid': '',
            'first_name': 'John',
            'last_name': 'Dwyer',
            'email': 'jdwyer@ncsu.edu',
            'password1': 'Jd!456789',
            'phone_number': 9876578901,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('unityid', form.errors)

    def test_registerForm_missing_username(self):
        """
        Test that the RegisterForm is invalid when the 'username' field is missing.
        """
        form = RegisterForm(data={
            'username': '',
            'unityid': 'ajohn6',
            'first_name': 'John',
            'last_name': 'Dwyer',
            'email': 'jdwyer@ncsu.edu',
            'password1': 'Jd!456789',
            'phone_number': 9876578901,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_registerForm_invalid_email(self):
        """
        Test that the RegisterForm is invalid when an invalid email is provided.
        """
        form = RegisterForm(data={
            'username': 'John',
            'unityid': 'ajohn6',
            'first_name': 'John',
            'last_name': 'Dwyer',
            'email': 'invalid-email',
            'password1': 'jd45678',
            'phone_number': 987657890,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_registerForm_missing_password(self):
        """
        Test that the RegisterForm is invalid when the 'password1' field is empty.
        """
        form = RegisterForm(data={
            'username': 'John',
            'unityid': 'ajohn6',
            'first_name': 'John',
            'last_name': 'Dwyer',
            'email': 'jdwyer@ncsu.edu',
            'password1': '',
            'phone_number': 987657890,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)

    def test_registerForm_short_password(self):
        """
        Test that the RegisterForm is invalid when the password is too short.
        """
        form = RegisterForm(data={
            'username': 'John',
            'unityid': 'ajohn6',
            'first_name': 'John',
            'last_name': 'Dwyer',
            'email': 'jdwyer@ncsu.edu',
            'password1': '123',  # Too short
            'phone_number': 987657890,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)

    def test_registerForm_invalid_phone_number(self):
        """
        Test that the RegisterForm is invalid when an invalid phone number is provided.
        """
        form = RegisterForm(data={
            'username': 'John',
            'unityid': 'ajohn6',
            'first_name': 'John',
            'last_name': 'Dwyer',
            'email': 'jdwyer@ncsu.edu',
            'password1': 'Jd!456789',
            'phone_number': 123,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)

    def test_loginForm_validData(self):
        """
        Test that the LoginForm is valid when valid username and password are provided.
        """
        form = LoginForm(data={
            'username': 'John',
            'password': 'jd45678'
        })
        self.assertTrue(form.is_valid())

    def test_loginForm_missing_username(self):
        """
        Test that the LoginForm is invalid when the 'username' field is missing.
        """
        form = LoginForm(data={
            'username': '',
            'password': 'jd45678'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_loginForm_missing_password(self):
        """
        Test that the LoginForm is invalid when the 'password' field is missing.
        """
        form = LoginForm(data={
            'username': 'John',
            'password': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_EditForm_validData(self):
        """
        Test that the EditUserForm is valid when valid first name, last name, and phone number are provided.
        """
        form = EditUserForm(data={
            'first_name': 'John',
            'last_name': 'Dwyer',
            'phone_number': 9876578901,
        })
        self.assertTrue(form.is_valid())

    def test_EditForm_invalid_phone_number(self):
        """
        Test that the EditUserForm is invalid when an invalid phone number is provided.
        """
        form = EditUserForm(data={
            'unityid': 'ajohn6',
            'first_name': 'John',
            'last_name': 'Dwyer',
            'email': 'jdwyer@ncsu.edu',
            'phone_number': 123,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
