"""
This module defines the `Ride` model, which is used to store information about rides in the PackTravel application.

The `Ride` model has a field for the destination of the ride. This model can be extended to include additional details as needed.

Models are used to represent database tables in Django and define the structure of the data.

"""

from django.db import models


# declare a new model with a name "GeeksModel"
class Ride(models.Model):
    """
    A model representing a ride.

    The `Ride` model is used to store information about a specific ride, including the ride's destination. This model can be extended to include more attributes like date, route, or other details as required.

    Attributes:
        destination (TextField): A field to store the destination of the ride.

    Meta:
        app_label (str): Specifies the app label to associate this model with the `PackTravel.publish` app.

    Methods:
        __str__(self): Returns a string representation of the `Ride` instance, in this case, its destination.
    """
    # fields of the model
    destination = models.TextField()
    # rideDate = models.TextField()

    class Meta:
        """
        Metadata options for the `Ride` model.

        The `Meta` class provides configuration options for the `Ride` model. It allows you to specify various behaviors, including the app label that the model belongs to. In this case, it sets the `app_label` to `PackTravel.publish` to explicitly associate the model with the `publish` app within the `PackTravel` project.

        Attributes:
            app_label (str): Specifies the app label to associate this model with the `PackTravel.publish` app.
        """
        app_label = 'PackTravel.publish'

    # renames the instances of the model
    # with their title name
    def __str__(self):
        """
        Returns a string representation of the `Ride` instance.

        This method is used to provide a human-readable string for each `Ride` object. In this case, it returns the title of the ride.

        Returns:
            str: The string representation of the ride, which is the ride's destination.
        """
        return self.title
