from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data for a Profile'''

    # data attributes
    first_name = models.TextField(blank=False)
    last_name =  models.TextField(blank=False)
    city =  models.TextField(blank=False)
    email =  models.TextField(blank=False)
    image_url = models.URLField(blank=False) 

    def __str__(self):
        '''Return a string representation of this Profile'''
        return f"{self.first_name} {self.last_name}"

