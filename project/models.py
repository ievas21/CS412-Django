from django.db import models
from django.contrib.auth.models import User
import csv

# Ieva sagaitis, ievas@bu.edu

# Define that models for our project, which will determine what fields each 
# model instance will have.

class Book(models.Model):
    '''
    Store/represent the data from one book.
    Title, Author, Score, Ratings, Shelvings, Published, Description, Image
    '''
    # data attributes
    title = models.TextField()
    author = models.TextField()
    score = models.FloatField()
    num_ratings = models.IntegerField()
    num_shelvings = models.IntegerField()
    yr_published = models.IntegerField()
    description = models.TextField()
    image_url = models.URLField()

    def __str__(self):
        '''Return a string representation of the book instance.'''
        return f'{self.title} by {self.author}'
    
    def get_reviews(self):
        '''Retrieve all reviews for this Book'''
        # use the ORM to filter reviews made for the specific book and order by timestamp
        reviews = Review.objects.filter(book=self).order_by('-timestamp')
        return reviews
    

class Person(models.Model):
    '''
    Encapsulate the data for a Person in our application.
    '''
    # data attributes
    first_name = models.TextField(blank=False)
    last_name =  models.TextField(blank=False)
    email =  models.TextField(blank=False)
    image_url = models.TextField(blank=False) 
    user = models.OneToOneField(User, on_delete=models.CASCADE) # associate each person with a user (one-to-one relationship)
    # associate with a foreign key to a book, to represent a book a user is currently reading
    currently_reading = models.ForeignKey("Book", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        '''Return a string representation of this Person.'''
        return f"{self.first_name} {self.last_name}"
    
    def get_reviews(self):
        '''Retrieve all reviews that this Person instance made.'''
        # use the ORM to filter reviews where this person instance is the FK
        reviews = Review.objects.filter(person=self).order_by('-timestamp') # order by timestamp (most recent reviews show up first)
        return reviews
    
    def get_friends(self):
        '''Retrieve all friendships for this Person instance.'''
        # filter the friend objects where they contain a FK to this person
        friends1 = Friend.objects.filter(profile1=self)
        friends2 = Friend.objects.filter(profile2=self)
    
        # empty set of friend ids for the person (friendship relationship must go both ways)
        friend_pks = set()  
        for f in friends1:
            # add the friend's pk to the set
            friend_pks.add(f.profile2.pk) 

        for f in friends2:
            # add the friend's pk to the set 
            friend_pks.add(f.profile1.pk)

        # get the person objects associated with the friends and exclude the current logged-in person 
        friends = Person.objects.filter(pk__in=friend_pks).exclude(pk = self.pk)
        return list(friends)
    
    def get_reviews(self):
        '''Retrieve all reviews that this person created.'''
         # use the ORM to filter reviews where this person instance is the FK
        reviews = Review.objects.filter(person=self).order_by('-timestamp')
        return reviews
    
    def get_book_list(self):
        '''Retrieve all books that this user has in their to-read list.'''
        # use the ORM to filter the BookList object instance where this person is the FK
        books = BookList.objects.filter(person=self)
        return books
    
    def get_feed(self):
        '''Gets all reviews for the person and the person's friends'''
        friend_pks = set()

          # filter the friend objects where they contain a FK to this person
        friend1 = Friend.objects.filter(profile1=self)
        for friend in friend1:
             # add the friend's pk to the set 
            friend_pks.add(friend.profile2.pk)
                      
        friend2 = Friend.objects.filter(profile2=self)
        for friend in friend2:
             # add the friend's pk to the set 
            friend_pks.add(friend.profile1.pk)

        # add the profile itself, in order to display their reviews as well
        friend_pks.add(self.pk)

        # get the reviews associated with the friend profiles and order by their timestamp 
        feed = Review.objects.filter(person_id__in=friend_pks).order_by('-timestamp')
        return feed
    
    def add_friend(self, other):
        '''Allows for a person to create a friend relationship with another person.'''
        # check that we're not making a friend relationship for a Profile with itself
        if (self != other):
            # assign the friend objects friend1 and friend2 to make sure the relationship goes both ways
            friend1 = Friend.objects.filter(profile1=self, profile2=other)
            friend2 = Friend.objects.filter(profile1=other, profile2=self)
            # check that the friendship does not yet exist
            if (not friend1.exists() and not friend2.exists()):
                # create the friend relationship
                Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        '''Gets friend suggestions for a person (i.e. everyone is the database that is not yet
        friends with them)
        '''
        pks = set()

         # filter the friend objects where they contain a FK to profile1
        friend1 = Friend.objects.filter(profile1=self)
        for friend in friend1:
             # add the friend's pk to the set 
            pks.add(friend.profile2.pk)

         # filter the friend objects where they contain a FK to profile2
        friend2 = Friend.objects.filter(profile2=self)
        for friend in friend2:
             # add the friend's pk to the set 
            pks.add(friend.profile1.pk)
        
        # the suggestions should exclude the person themselves and any other person that
        # the user is already friends with
        suggestions = Person.objects.exclude(pk=self.pk).exclude(pk__in=pks)
        return suggestions
    
    
class Friend(models.Model):
    '''Encapsulate two profiles that are friends with one another.'''
    
    profile1 = models.ForeignKey("Person", related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey("Person", related_name="profile2", on_delete=models.CASCADE)
    # holds FKs to two profiles to create this relationship

    def __str__(self):
        '''Return a string representation method.'''
        return f'{self.profile1} & {self.profile2}'
    

class Review(models.Model):
    '''Encapsulate a review on a book.'''
    # create a 1 to many relationship between Book and Review
    book = models.ForeignKey("Book", on_delete=models.CASCADE) # foreign key specification for book
    person = models.ForeignKey("Person", on_delete=models.CASCADE) # foreign key specification for person
    timestamp =  models.DateTimeField(auto_now=True)
    review = models.TextField(blank=False)
    rating = models.PositiveSmallIntegerField(default=5) # set the default rating of a review to 5 stars, so that it is not null
    

    def __str__(self):
        '''Return a string representation method of a Review instance.'''
        return f'{self.review} - {self.person}'
    

class BookList(models.Model):
    '''Encapsulate a to-read list for a person instance.'''
    book = models.ForeignKey("Book", on_delete=models.CASCADE) # foreign key specification for book (can have many books)
    person = models.ForeignKey("Person", on_delete=models.CASCADE) # foreign key specification for a person (unique instance for each profile)

    def __str__(self):
        '''Return a string representation method of a BookList instance.'''
        return f'{self.book} - {self.person}'


def load_data():
    '''Load the data records from a CSV file, and create Django model instances.'''
     # delete all records, if we are attempting to load them again
    Book.objects.all().delete()
    # get the file path of the csv file
    filename = "C:\\Users\\ievas\\OneDrive\\Desktop\\CS412\Popular-Books.csv"
    # open the file
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        
        # skip the header row
        next(reader)
        # encase in a try except block, in order to ensure we leave out data that is invalid for our Book model
        for fields in reader:
            try:
                # creating a Book instance for each line
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
                # save the result in our database
                result.save()
                print(f'Created result: {result}')
            except:
                # print an exception if the book was not successfully created (invalid data)
                print(f'Exception Occured: {fields}.')

    print("Done.")
