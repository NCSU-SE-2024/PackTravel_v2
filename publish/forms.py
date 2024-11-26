"""
Forms module for handling Ride data in the Django application.

This module contains the form definition for creating and validating Ride objects. It includes form fields for the ride's source, destination, purpose, ride date, route, and route details. It uses Django's ModelForm to handle form validation and ensure the proper format and consistency of the input data.

Imports:
    - `forms`: Django forms module for creating and handling forms.
    - `ValidationError`: Exception used to raise validation errors during form processing.
    - `Ride`: The model representing the ride data.
    - `validate_date`: Custom validator for validating ride dates.
"""

from django import forms
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import Ride
from django.forms import ValidationError
from .validators import validate_date


class RideForm(forms.ModelForm):
    """
    A form for creating or editing Ride instances.

    This form provides fields for collecting ride-related information such as source, destination, purpose, ride date, route, and route details. The form performs validation to ensure that the source and destination are not the same and validates the ride date using a custom validator.

    Attributes:
        source (CharField): The starting point of the ride.
        destination (CharField): The destination of the ride.
        purpose (CharField): The purpose of the ride.
        rideDate (CharField): The date of the ride, validated by the `validate_date` validator.
        route (CharField): The route for the ride.
        routeDetails (CharField): Detailed description of the route.

    Methods:
        clean(): Performs custom validation to ensure the source and destination are different.
    """
    source = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':
                                                                          'Enter your start destination', 'class': 'form-control'}))
    destination = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':
                                                                               'Enter your end destination', 'class': 'form-control'}))
    purpose = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':
                                                                           'Enter your purpose', 'class': 'form-control'}))
    rideDate = forms.CharField(required=True, validators=[validate_date], widget=forms.TextInput(attrs={'placeholder':
                                                                                                        'Enter ride date', 'class': 'form-control'}))
    route = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':
                                                                         'Enter route', 'class': 'form-control'}))
    routeDetails = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':
                                                                                'Enter route details', 'class': 'form-control'}))

    class Meta:
        """
        Metadata for the RideForm.

        This inner class defines the model and fields that the form will handle. It links the form to the `Ride` model and specifies which fields from the model should be included in the form. 

        Attributes:
            model (Model): The model that this form is associated with. In this case, it is the `Ride` model.
            fields (tuple): A tuple of strings representing the fields from the `Ride` model that will be included in the form. These fields will be displayed to the user for input.
        """
        model = Ride

        fields = (
            'source',
            'destination',
            'purpose',
            'rideDate',
            'route',
            'routeDetails',
        )

    def clean(self):
        """
        Custom form validation to ensure source and destination are different.

        This method checks that the source and destination values are not identical. If they are the same, a `ValidationError` is raised with a message indicating that the source and destination must be different.

        Returns:
            dict: The cleaned data from the form after validation.
        
        Raises:
            ValidationError: If the source and destination are the same.
        """
        cleaned_data = super().clean()
        source = cleaned_data.get('source')
        destination = cleaned_data.get('destination')

        if source and destination and source == destination:
            raise ValidationError("Source and destination must be different.")

        return cleaned_data
