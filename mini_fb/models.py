from django.db import models
from django.urls import reverse

# Ieva sagaitis, ievas@bu.edu
# Creates a profile model with the user's name, city, image, and email
class Profile(models.Model):
    '''Encapsulate the data for a Profile in our application'''

    # data attributes
    first_name = models.TextField(blank=False)
    last_name =  models.TextField(blank=False)
    city =  models.TextField(blank=False)
    email =  models.TextField(blank=False)
    image_url = models.TextField(blank=False) 

    def __str__(self):
        '''Return a string representation of this Profile'''
        return f"{self.first_name} {self.last_name}"
    
    def get_status_messages(self):
        '''Retrieve all status messages for this Profile'''

        # use the ORM to filter Comments where this instance of an object is the FK
        messages = StatusMessage.objects.filter(profile=self)
        return messages
    
    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})

    

class StatusMessage(models.Model):
    '''Encapsulate a status message on a profile.'''

    # create a 1 to many relationship between Profile and Status Message
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE) ## foreign key specification

    timestamp =  models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation method.'''
        return f'{self.message}'

