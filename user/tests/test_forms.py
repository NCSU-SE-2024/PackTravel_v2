from django.test import TransactionTestCase
from user.forms import RegisterForm,LoginForm

class TestForms(TransactionTestCase):
    def test_registerForm_validData(self):

        form = RegisterForm(data={
                            'username': 'John',
                            'unityid' : 'ajohn6',
                            'first_name' : 'John',
                            'last_name' : 'Dwyer',
                            'email' : 'jdwyer@ncsu.edu',
                            'password1' : 'jd45678',
                            'phone_number' : 987657890,
                            })
        self.assertTrue(form.is_valid())
    
    def test_registerForm_missingID(self):

        form = RegisterForm(data={
                            'username': 'John',
                            'unityid' : '',
                            'first_name' : 'John',
                            'last_name' : 'Dwyer',
                            'email' : 'jdwyer@ncsu.edu',
                            'password1' : 'jd45678',
                            'phone_number' : 987657890,
                            })
        self.assertFalse(form.is_valid())
        self.assertIn('unityid', form.errors)

    def test_registerForm_missing_username(self):
        form = RegisterForm(data={
            'username': '',
            'unityid': 'ajohn6',
            'first_name': 'John',
            'last_name': 'Dwyer',
            'email': 'jdwyer@ncsu.edu',
            'password1': 'jd45678',
            'phone_number': 987657890,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_registerForm_invalid_email(self):
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

    # def test_registerForm_short_password(self):
    #     form = RegisterForm(data={
    #         'username': 'John',
    #         'unityid': 'ajohn6',
    #         'first_name': 'John',
    #         'last_name': 'Dwyer',
    #         'email': 'jdwyer@ncsu.edu',
    #         'password1': '123',  # Too short
    #         'phone_number': 987657890,
    #     })
    #     self.assertFalse(form.is_valid())
    #     self.assertIn('password1', form.errors)

    def test_registerForm_invalid_phone_number(self):
        form = RegisterForm(data={
            'username': 'John',
            'unityid': 'ajohn6',
            'first_name': 'John',
            'last_name': 'Dwyer',
            'email': 'jdwyer@ncsu.edu',
            'password1': 'jd45678',
            # Invalid phone number  
            'phone_number': 123,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
    
    def test_loginForm_validData(self):

        form = LoginForm(data={
                            'username': 'John',
                            'password' : 'jd45678'
                            })
        self.assertTrue(form.is_valid())
    
    def test_loginForm_missing_username(self):

        form = LoginForm(data={
                            'username': '',
                            'password' : 'jd45678'
                            })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_loginForm_missing_password(self):

        form = LoginForm(data={
                            'username': 'John',
                            'password' : ''
                            })
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
    
    # def test_loginForm_short_password(self):
    #     form = LoginForm(data={
    #         'username': 'John',
    #         'password': '123'  # Too short
    #     })
    #     self.assertFalse(form.is_valid())
    #     self.assertIn('password', form.errors)
        