"""
Configuration for the 'search' application in Django.

This module defines the configuration for the 'search' app using Django's AppConfig.
It includes settings such as the default auto field type and the name of the app.
"""

from django.apps import AppConfig


class SearchConfig(AppConfig):
    """
    Configuration class for the 'search' app.

    This class extends Django's AppConfig and is used to configure various settings for the 'search' app, such as
    defining the name of the app and setting the default field type for auto fields.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'
