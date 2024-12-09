from django.db import models
from django.contrib.auth.models import User
import csv

# Ieva sagaitis, ievas@bu.edu

class Book(models.Model):
    '''
    Store/represent the data from one book.
    Title, Author, Score, Ratings, Shelvings, Published, Description, Image
    '''

    title = models.TextField()
    author = models.TextField()
    score = models.FloatField()
    num_ratings = models.IntegerField()
    num_shelvings = models.IntegerField()
    yr_published = models.IntegerField()
    description = models.TextField()
    image_url = models.URLField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.title} by {self.author}'
    
    def get_reviews(self):
        '''Retrieve all reviews for this Book'''

        reviews = Review.objects.filter(book=self).order_by('-timestamp')
    
        return reviews
    
    
    
class Person(models.Model):
    '''Encapsulate the data for a Profile in our application'''

    # data attributes
    first_name = models.TextField(blank=False)
    last_name =  models.TextField(blank=False)
    email =  models.TextField(blank=False)
    image_url = models.TextField(blank=False) 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currently_reading = models.ForeignKey("Book", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        '''Return a string representation of this Profile'''
        return f"{self.first_name} {self.last_name}"
    
    def get_reviews(self):
        '''Retrieve all reviews for this Profile'''

    # use the ORM to filter Comments where this instance of an object is the FK
        reviews = Review.objects.filter(person=self).order_by('-timestamp')
        return reviews
    
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

        friends = Person.objects.filter(pk__in=friend_pks).exclude(pk = self.pk)
        return list(friends)
    
    def get_reviews(self):
        '''Retrieve all reviews that this user created.'''
        reviews = Review.objects.filter(person=self).order_by('-timestamp')
        return reviews
    
    def get_book_list(self):
        '''Retrieve all books that this user has in their to-read list.'''
        books = BookList.objects.filter(person=self)
        return books
    
    def get_feed(self):
        '''Gets all reviews for the profile and the profile's friends'''
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
        feed = Review.objects.filter(person_id__in=friend_pks).order_by('-timestamp')
        return feed
    
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
        
        suggestions = Person.objects.exclude(pk=self.pk).exclude(pk__in=pks)
        return suggestions
    
    
class Friend(models.Model):
    '''Encapsulate two profiles that are friends with one another.'''
    
    profile1 = models.ForeignKey("Person", related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey("Person", related_name="profile2", on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation method.'''
        return f'{self.profile1} & {self.profile2}'
    

class Review(models.Model):
    '''Encapsulate a review on a book.'''

    # create a 1 to many relationship between Book and Review
    book = models.ForeignKey("Book", on_delete=models.CASCADE) ## foreign key specification for book
    person = models.ForeignKey("Person", on_delete=models.CASCADE) ## foreign key specification for profile
    timestamp =  models.DateTimeField(auto_now=True)
    review = models.TextField(blank=False)
    rating = models.PositiveSmallIntegerField(default=5) 
    

    def __str__(self):
        '''Return a string representation method.'''
        return f'{self.review} - {self.person}'
    

class BookList(models.Model):
    '''Encapsulate a to-read list for a person.'''
    book = models.ForeignKey("Book", on_delete=models.CASCADE) ## foreign key specification for book
    person = models.ForeignKey("Person", on_delete=models.CASCADE) ## foreign key specification for a person

    def __str__(self):
        return f'{self.book} - {self.person}'


def load_data():
    '''Load the data records from a CSV file, and create Django model instances.'''

     # delete all records
    Book.objects.all().delete()

    filename = "C:\\Users\\ievas\\OneDrive\\Desktop\\CS412\Popular-Books.csv"
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        
        # Skip the header row
        next(reader)
        
        for fields in reader:
            try:
                # Creating a Book instance for each line
                result = Book(
                    title=fields[0],
                    author=fields[1],
                    score=float(fields[2]),
                    num_ratings=int(fields[3]),
                    num_shelvings=int(fields[4]),
                    yr_published=int(fields[5]),
                    description=fields[6],
                    image_url=fields[7]
                )
                result.save()
                print(f'Created result: {result}')
            except:
                print(f'Exception Occured: {fields}.')

    print("Done.")
