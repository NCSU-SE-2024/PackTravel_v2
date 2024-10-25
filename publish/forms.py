from django import forms
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import Ride

class RideForm(forms.ModelForm):
    source = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':
    'Enter your start destination', 'class': 'form-control'}))
    destination = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':
    'Enter your end destination', 'class': 'form-control'}))
    purpose = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':
    'Enter your purpose', 'class': 'form-control'}))
    rideDate = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':
    'Enter ride date', 'class': 'form-control'}))
    route = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':
    'Enter route', 'class': 'form-control'}))
    routeDetails = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':
    'Enter route details', 'class': 'form-control'}))

    class Meta:
        model = Ride

        fields = "__all__"
