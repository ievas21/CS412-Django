from django.db import models
# Ieva sagaitis, ievas@bu.edu
# Creates a profile model with the user's name, city, image, and email
class Profile(models.Model):
    '''Encapsulate the data for a Profile in our application'''

    # data attributes
    first_name = models.TextField(blank=False)
    last_name =  models.TextField(blank=False)
    city =  models.TextField(blank=False)
    email =  models.TextField(blank=False)
    image_url = models.URLField(blank=False) 

    def __str__(self):
        '''Return a string representation of this Profile'''
        return f"{self.first_name} {self.last_name}"

