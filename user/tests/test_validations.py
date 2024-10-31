from ..validators import validate_email_domain, validate_unique_unity_id, validate_unique_username, validate_password
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError

class UserUnityIDValidationTests(SimpleTestCase):
    def test_valid_unity_id(self):
        unityid = "testunityid"
        try:
            validate_unique_unity_id(unityid)
        except ValidationError:
            self.fail("Raised validation error on a valid unityid")

    def test_invalid_unity_id(self):
        unityid = "kl"
        with self.assertRaises(ValidationError):
            validate_unique_unity_id(unityid)

class UserUsernameValidationTests(SimpleTestCase):
    def test_valid_username(self):
        username = "abhishek"
        try:
            validate_unique_username(username)
        except ValidationError:
            self.fail("Raised validation error on a valid unityid")

    def test_invalid_unity_id(self):
        username = "test"
        with self.assertRaises(ValidationError):
            validate_unique_username(username)
            

class UserEmailValidationTests(SimpleTestCase):
    def test_valid_email(self):
        email = "student@ncsu.edu"
        try:
            validate_email_domain(email)
        except ValidationError:
            self.fail("Raised validation error on a valid email")

    def test_invalid_email_domain(self):
        email = "asd@gmail.com"
        with self.assertRaises(ValidationError):
            validate_email_domain(email)

    def test_invalid_email_address(self):
        email = "@ncsu.edu"
        with self.assertRaises(ValidationError):
            validate_email_domain(email)

    def test_invalid_email_address_no_domain(self):
        email = "bkbhayan"
        with self.assertRaises(ValidationError):
            validate_email_domain(email)

    def test_invalid_email_address_no_domain_2(self):
        email = "bkbhayan@"
        with self.assertRaises(ValidationError):
            validate_email_domain(email)
    

class PasswordValidationTests(SimpleTestCase):

    def test_valid_password(self):
        password = "Valid1Pass!"
        try:
            validate_password(password)
        except ValidationError:
            self.fail("Raised ValidationError on a valid password")

    def test_password_too_short(self):
        password = "Short1!"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("Password is too short", str(context.exception))

    def test_password_too_long(self):
        password = "ThisPasswordIsWayTooLong123!"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("Password is too long", str(context.exception))

    def test_password_no_lowercase(self):
        password = "NOLOWER123!"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("lowercase letter", str(context.exception))

    def test_password_no_uppercase(self):
        password = "noupper123!"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("uppercase letter", str(context.exception))

    def test_password_no_digit(self):
        password = "NoDigitPass!"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("digit", str(context.exception))

    def test_password_no_special_char(self):
        password = "NoSpecialChar1"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("special character", str(context.exception))

    def test_common_password(self):
        password = "Password!123456"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("too common", str(context.exception))

    def test_repeated_characters(self):
        password = "AAAbbbCcc123!"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)
        self.assertIn("repeated characters", str(context.exception))

    def test_password_with_spaces(self):
        password = "Valid Pass 1!"
        try:
            validate_password(password)
        except ValidationError:
            self.fail("Raised ValidationError on a valid password with spaces")

    def test_password_with_unicode(self):
        password = "Válíd1Páss!"
        try:
            validate_password(password)
        except ValidationError:
            self.fail("Raised ValidationError on a valid password with Unicode characters")

    def test_password_edge_case_length(self):
        password = "Valid1P!" 
        try:
            validate_password(password)
        except ValidationError:
            self.fail("Raised ValidationError on a valid password at minimum length")

        password = "Valid1Pass1234!"
        try:
            validate_password(password)
        except ValidationError:
            self.fail("Raised ValidationError on a valid password at maximum length")

    def test_password_with_all_special_chars(self):
        password = "!@#(),.?\":{}|<>"
        with self.assertRaises(ValidationError) as context:
            validate_password(password)