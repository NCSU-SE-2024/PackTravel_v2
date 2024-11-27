"""
UserConfig Module

This module defines the configuration class for the 'user' Django application.
It is used to configure application settings within the Django project. This class
is inherited from Django's AppConfig, and is typically used for application-specific
setup such as default settings, model registration, etc.
"""

from django.apps import AppConfig


class UserConfig(AppConfig):
    """
    Configuration class for the 'user' application.

    This class is responsible for setting up the 'user' app's configuration in the
    Django project. It inherits from AppConfig and is used to define the name
    of the application and its primary key field type. The default primary key
    field type is set to BigAutoField, which is commonly used in modern Django
    projects for automatically generated integer IDs.

    Attributes:
        default_auto_field (str): The default type for automatically generated
                                  primary key fields. Set to 'BigAutoField' for
                                  64-bit integers.
        name (str): The Python path to the application, which is 'user' in this case.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "user"
