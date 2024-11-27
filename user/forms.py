"""
User Forms Module

This module defines various Django forms related to user authentication and registration.
It includes forms for registering new users, logging in, and editing user profiles.
Custom validation logic is implemented for fields such as email, Unity ID, and username.
"""

from django import forms

# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import (
    validate_email_domain,
    validate_unique_unity_id,
    validate_password,
    validate_unique_username,
)


class RegisterForm(forms.ModelForm):
    """
    A form for registering a new user.

    This form allows users to provide their personal details such as username,
    Unity ID, first and last names, email, phone number, and profile picture.
    It also validates the uniqueness of the username and Unity ID, the validity of
    the email domain, and enforces password strength and confirmation.

    Fields:
        username (str): A unique username for the user.
        unityid (str): A unique Unity ID for the user.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address, which is validated for correct domain.
        password1 (str): The password for the user, validated for strength.
        password2 (str): A confirmation of the password.
        phone_number (str): The user's phone number.
        profile_picture (ImageField): An optional profile picture for the user.

    Methods:
        clean(): Validates the form data, ensuring the passwords match.
    """

    username = forms.CharField(
        required=True,
        validators=[validate_unique_username],
        widget=forms.TextInput(
            attrs={"placeholder": "Enter a username", "class": "form-control"}
        ),
    )
    unityid = forms.CharField(
        required=True,
        validators=[validate_unique_unity_id],
        widget=forms.TextInput(
            attrs={"placeholder": "Unity Id", "class": "form-control"}
        ),
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "First Name", "class": "form-control"}
        ),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Last Name", "class": "form-control"}
        ),
    )
    email = forms.EmailField(
        required=True,
        validators=[validate_email_domain],
        max_length=60,
        widget=forms.EmailInput(
            attrs={"placeholder": "abc@ncsu.edu", "class": "form-control"}
        ),
    )
    password1 = forms.CharField(
        required=True,
        validators=[validate_password],
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        ),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm Password", "class": "form-control"}
        ),
    )
    phone_number = forms.CharField(
        required=True,
        min_length=10,
        max_length=11,
        widget=forms.TextInput(
            attrs={"placeholder": "Phone Number", "class": "form-control"}
        ),
    )
    profile_picture = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )

    class Meta:
        """
        Meta class for RegisterForm.

        This class provides metadata for the form, defining the associated model
        (`User`) and the fields to be included in the form. The fields listed here
        correspond to the attributes that a user can fill out during registration,
        such as their username, Unity ID, and email.
        """

        model = User
        fields = (
            "username",
            "unityid",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "phone_number",
            "profile_picture",
        )

    def clean(self):
        """
        Validates the cleaned data from the form.

        This method checks that the passwords entered by the user match. If they do
        not match, an error is added to the 'password2' field.

        Returns:
            cleaned_data (dict): A dictionary of the form's cleaned data, with errors
                                  added if necessary.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match")

        return cleaned_data


class LoginForm(forms.ModelForm):
    """
    A form for logging in a user.

    This form allows users to input their username and password for authentication.

    Fields:
        username (str): The username of the user.
        password (str): The password of the user.

    Methods:
        clean(): This method is inherited from `forms.ModelForm` and is not overridden here.
    """

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your username",
                "class": "form-control"}
        ),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        ),
    )

    class Meta:
        """
        Meta class for LoginForm.

        This class provides metadata for the form, defining the associated model
        (`User`) and the fields to be included in the form. The fields listed here
        correspond to the attributes a user must provide to log in, such as `username`
        and `password`.
        """

        model = User
        fields = ("username", "password")


class EditUserForm(forms.ModelForm):
    """
    A form for editing a user's profile.

    This form allows users to update their first name, last name, phone number, and
    profile picture. The password and username cannot be edited by the user through
    this form.

    Fields:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        phone_number (str): The user's phone number.
        profile_picture (ImageField): An optional field for updating the user's profile picture.

    Methods:
        clean(): This method is inherited from `forms.ModelForm` and is not overridden here.
    """

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "First Name", "class": "form-control"}
        ),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Last Name", "class": "form-control"}
        ),
    )
    phone_number = forms.CharField(
        required=True,
        min_length=10,
        max_length=11,
        widget=forms.TextInput(
            attrs={"placeholder": "Phone Number", "class": "form-control"}
        ),
    )
    profile_picture = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )

    class Meta:
        """
        Meta class for EditUserForm.

        This class provides metadata for the form, defining the associated model
        (`User`) and the fields to be included in the form. It allows editing of
        user details such as `first_name`, `last_name`, `phone_number`, and `profile_picture`,
        while the `username` and `password` cannot be edited.
        """

        model = User
        fields = ("first_name", "last_name", "phone_number", "profile_picture")
