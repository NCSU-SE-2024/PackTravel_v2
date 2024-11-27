"""
Test module for user-related validators.

This module contains test cases for the following user data validators:
- validate_unique_unity_id: Ensures the Unity ID is unique and correctly formatted.
- validate_unique_username: Ensures the username is unique and correctly formatted.
- validate_email_domain: Ensures the email domain is valid and specific to the organization.
- validate_password: Ensures the password meets security requirements (e.g., length, complexity).

Each validator is tested for both valid and invalid inputs to ensure proper error handling and compliance.
"""

from ..validators import validate_email_domain, validate_unique_unity_id, validate_unique_username, validate_password
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError


class UserUnityIDValidationTests(SimpleTestCase):
    """
    Test cases for validating Unity IDs to ensure proper format and uniqueness.

    Methods:
    - test_valid_unity_id: Tests that a valid Unity ID passes validation.
    - test_invalid_unity_id: Tests that an invalid Unity ID raises a ValidationError.
    """

    def test_valid_unity_id(self):
        """
        Test that a valid Unity ID passes validation.

        A valid Unity ID should not trigger a ValidationError.
        """
        unityid = "testunityid"
        try:
            validate_unique_unity_id(unityid)
        except ValidationError:
            self.fail("Raised validation error on a valid Unity ID.")

    def test_invalid_unity_id(self):
        """
        Test that an invalid Unity ID raises a ValidationError.

        A Unity ID containing numbers like 'test1234' should raise a validation error.
        """
        unityid = "test1234"
        with self.assertRaises(ValidationError):
            validate_unique_unity_id(unityid)


class UserUsernameValidationTests(SimpleTestCase):
    """
    Test cases for validating usernames to ensure proper uniqueness and format.

    Methods:
    - test_valid_username: Tests that a valid username passes validation.
    - test_invalid_username: Tests that an invalid username raises a ValidationError.
    """

    def test_valid_username(self):
        """
        Test that a valid username passes validation.

        A valid username should not raise a ValidationError.
        """
        username = "rahul"
        try:
            validate_unique_username(username)
        except ValidationError:
            self.fail("Raised validation error on a valid username.")

    def test_invalid_unity_id(self):
        username = "test1234"
        with self.assertRaises(ValidationError):
            validate_unique_username(username)


class UserEmailValidationTests(SimpleTestCase):
    """
    Test cases for validating email addresses to ensure proper domain and format.

    Methods:
    - test_valid_email: Tests that a valid email passes validation.
    - test_invalid_email_domain: Tests that an invalid email domain raises a ValidationError.
    - test_invalid_email_address: Tests that an improperly formatted email address raises a ValidationError.
    - test_invalid_email_address_no_domain: Tests that an email address missing the domain part raises a ValidationError.
    - test_invalid_email_address_no_domain_2: Tests that an email address ending with '@' without domain raises a ValidationError.
    """

    def test_valid_email(self):
        """
        Test that a valid email address passes domain validation.

        Email addresses from the correct domain (e.g., 'student@ncsu.edu') should pass validation.
        """
        email = "student@ncsu.edu"
        try:
            validate_email_domain(email)
        except ValidationError:
            self.fail("Raised validation error on a valid email.")

    def test_invalid_email_domain(self):
        """
        Test that an invalid email domain raises a ValidationError.

        Emails from domains not specified in the validation (e.g., 'gmail.com') should fail.
        """
        email = "asd@gmail.com"
        with self.assertRaises(ValidationError):
            validate_email_domain(email)

    def test_invalid_email_address(self):
        """
        Test that an invalid email address with missing parts raises a ValidationError.

        Email addresses without a domain (e.g., '@ncsu.edu') should trigger an error.
        """
        email = "@ncsu.edu"
        with self.assertRaises(ValidationError):
            validate_email_domain(email)

    def test_invalid_email_address_no_domain(self):
        """
        Test that an email address without a domain raises a ValidationError.

        Emails with no '@' or domain part (e.g., 'bkbhayan') should raise a validation error.
        """
        email = "bkbhayan"
        with self.assertRaises(ValidationError):
            validate_email_domain(email)

    def test_invalid_email_address_no_domain_2(self):
        """
        Test that an email address missing the domain part raises a ValidationError.

        Emails ending with '@' and no domain part (e.g., 'bkbhayan@') should be invalid.
        """
        email = "bkbhayan@"
        with self.assertRaises(ValidationError):
            validate_email_domain(email)


class PasswordValidationTests(SimpleTestCase):
    """
    Test cases for validating password strength and security criteria.

    Methods:
    - test_valid_password: Tests that a valid password passes validation.
    - test_password_too_short: Tests that a password that is too short raises a ValidationError.
    - test_password_too_long: Tests that a password that is too long raises a ValidationError.
    - test_password_no_lowercase: Tests that a password without a lowercase letter raises a ValidationError.
    - test_password_no_uppercase: Tests that a password without an uppercase letter raises a ValidationError.
    - test_password_no_digit: Tests that a password without a digit raises a ValidationError.
    - test_password_no_special_char: Tests that a password without a special character raises a ValidationError.
    - test_common_password: Tests that a password deemed too common raises a ValidationError.
    - test_repeated_characters: Tests that passwords with repeated characters raise a ValidationError.
    - test_password_with_spaces: Tests that passwords with spaces are allowed.
    - test_password_with_unicode: Tests that passwords with unicode characters are allowed.
    - test_password_edge_case_length: Tests the edge cases for minimum and maximum password lengths.
    - test_password_with_all_special_chars: Tests a password with special characters.
    """

    def test_valid_password(self):
        """
        Test that a valid password meets all validation criteria.

        A password like 'Valid1Pass!' should not raise any validation errors.
        """
        password = "Valid1Pass!"
        try:
            validate_password(password)
        except ValidationError:
            self.fail("Raised ValidationError on a valid password.")

    def test_password_too_short(self):
        """
        Test that a password that is too short raises a ValidationError.

        Passwords shorter than the required length (e.g., 'Short1!') should trigger an error.
        """
        password = "Short1!"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("Password is too short", str(context.exception))

    def test_password_too_long(self):
        """
        Test that a password that is too long raises a ValidationError.

        Passwords longer than the maximum allowed length should trigger an error.
        """
        password = "ThisPasswordIsWayTooLong123!"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("Password is too long", str(context.exception))

    def test_password_no_lowercase(self):
        """
        Test that a password without a lowercase letter raises a ValidationError.

        Passwords must contain at least one lowercase letter.
        """
        password = "NOLOWER123!"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("lowercase letter", str(context.exception))

    def test_password_no_uppercase(self):
        """
        Test that a password without an uppercase letter raises a ValidationError.

        Passwords must contain at least one uppercase letter.
        """
        password = "noupper123!"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("uppercase letter", str(context.exception))

    def test_password_no_digit(self):
        """
        Test that a password without a digit raises a ValidationError.

        Passwords must contain at least one digit.
        """
        password = "NoDigitPass!"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("digit", str(context.exception))

    def test_password_no_special_char(self):
        """
        Test that a password without a special character raises a ValidationError.

        Passwords must contain at least one special character (e.g., !, @, #).
        """
        password = "NoSpecialChar1"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("special character", str(context.exception))

    def test_common_password(self):
        """
        Test that a common password raises a ValidationError.

        Common passwords (e.g., 'Password!123456') should be rejected.
        """
        password = "Password!123456"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("too common", str(context.exception))

    def test_repeated_characters(self):
        """
        Test that passwords with repeated characters raise a ValidationError.

        Passwords like 'AAAbbbCcc123!' with repeated characters should raise an error.
        """
        password = "AAAbbbCcc123!"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("repeated characters", str(context.exception))

    def test_password_with_spaces(self):
        """
        Test that passwords with spaces are allowed.

        Passwords can include spaces if they meet all other criteria.
        """
        password = "Valid password 123!"
        try:
            validate_password(password)
        except ValidationError:
            self.fail("Raised validation error on a valid password with spaces.")

    def test_password_with_unicode(self):
        """
        Test that passwords with unicode characters are allowed.

        Passwords like 'ValidPass!🌟' should be accepted.
        """
        password = "ValidPass!🌟"
        try:
            validate_password(password)
        except ValidationError:
            self.fail("Raised validation error on a password with unicode.")

    def test_password_edge_case_length(self):
        """
        Test the edge cases for minimum and maximum password lengths.

        Passwords on the edge of the valid length range should pass validation.
        """
        valid_short_password = "Short1!"
        valid_long_password = "ThisIsALongPassword1!"
        try:
            validate_password(valid_short_password)
            validate_password(valid_long_password)
        except ValidationError:
            self.fail("Edge case password length failed validation.")

    def test_password_with_all_special_chars(self):
        """
        Test a password with all special characters.

        Passwords with a wide variety of special characters like '!@#$%^&*()' should be valid.
        """
        password = "!@#$%^&*()123"
        try:
            validate_password(password)
        except ValidationError:
            self.fail("Raised validation error on a valid password with all special chars.")
