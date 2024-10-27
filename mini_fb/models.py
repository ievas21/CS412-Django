from django.db import models
from django.urls import reverse

# Ieva sagaitis, ievas@bu.edu
# Creates the models for our application (Profile, Status Message, Image)


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
        messages = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
        return messages
    
    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})
    
    def get_friends(self):
        '''Retrieve all friendships for this Profile'''

        friends1 = Friend.objects.filter(profile1=self)
        friends2 = Friend.objects.filter(profile2=self)
    
        # set of friend ids for the Profile
        friend_pks = set()  
        for f in friends1:
            friend_pks.add(f.profile2.pk) 

        for f in friends2:
            friend_pks.add(f.profile1.pk)

        friends = Profile.objects.filter(pk__in=friend_pks).exclude(pk = self.pk)
        return list(friends)
    
    def add_friend(self, other):
        # check that we're not making a friend relationship for a Profile with itself
        if (self != other):
            friend1 = Friend.objects.filter(profile1=self, profile2=other)
            friend2 = Friend.objects.filter(profile1=other, profile2=self)
            # check that the friendship does not yet exist
            if (not friend1.exists() and not friend2.exists()):
                # create the friend relationship
                Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        pks = set()

        friend1 = Friend.objects.filter(profile1=self)
        for friend in friend1:
            pks.add(friend.profile2.pk)
                      
        friend2 = Friend.objects.filter(profile2=self)
        for friend in friend2:
            pks.add(friend.profile1.pk)
        
        suggestions = Profile.objects.exclude(pk=self.pk).exclude(pk__in=pks)
        return suggestions
    
    def get_news_feed(self):
        '''Gets all status messages for the profile and the profile's friends'''
        friend_pks = set()

        friend1 = Friend.objects.filter(profile1=self)
        for friend in friend1:
            friend_pks.add(friend.profile2.pk)
                      
        friend2 = Friend.objects.filter(profile2=self)
        for friend in friend2:
            friend_pks.add(friend.profile1.pk)

        # add the profile itself, in order to display its messages as well
        friend_pks.add(self.pk)

        # get the messages associated with the friend profiles and order by their timestamp 
        messages = StatusMessage.objects.filter(profile_id__in=friend_pks).order_by('-timestamp')
        
        return messages


class StatusMessage(models.Model):
    '''Encapsulate a status message on a profile.'''

    # create a 1 to many relationship between Profile and Status Message
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE) ## foreign key specification

    timestamp =  models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation method.'''
        return f'{self.message}'
    
    def get_images(self):
        '''Retrieve all images for a status message.'''

        # use the ORM to filter Images where this instance of an object is the FK
        images = Image.objects.filter(status_message=self)
        return images
    

class Image(models.Model):
    '''Encapsulate an image on a status message.'''

    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE) ## foreign key specification

    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=False)

    def __str__(self):
        '''Return a string representation method.'''
        return f'{self.image_file}'

class Friend(models.Model):
    '''Encapsulate two profiles that are friends with one another.'''
    
    profile1 = models.ForeignKey("Profile", related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey("Profile", related_name="profile2", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation method.'''
        return f'{self.profile1} & {self.profile2}'


