from django import forms
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import Ride
from django.forms import ValidationError
from .validators import validate_date


class RideForm(forms.ModelForm):
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
        cleaned_data = super().clean()
        source = cleaned_data.get('source')
        destination = cleaned_data.get('destination')

        if source and destination and source == destination:
            raise ValidationError("Source and destination must be different.")

        return cleaned_data
