"""
This module defines the configuration for the Forum app in the Django project.

The configuration class specifies metadata and default settings for the app,
such as its name and the default type of primary key fields for models.
"""

from django.apps import AppConfig


class ForumConfig(AppConfig):
    """
    Configures the Forum application.

    Attributes:
        default_auto_field (str): Specifies the default type of auto-generated primary key fields.
        name (str): The name of the application, used for identification within the Django project.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "forum"
