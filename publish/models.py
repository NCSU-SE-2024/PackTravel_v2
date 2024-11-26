from django.db import models


# declare a new model with a name "GeeksModel"
class Ride(models.Model):
    # fields of the model
    destination = models.TextField()
    # rideDate = models.TextField()

    class Meta:
        app_label = 'PackTravel.publish'

    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.title
