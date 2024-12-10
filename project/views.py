from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Book, Person, Review, BookList
from django.urls import reverse
from .forms import UpdateReviewForm, CreateReviewForm,  RegisterForm
from typing import Any
from django.db.models import Avg, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.http import HttpResponseRedirect
import random
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as AuthUser

# Ieva sagaitis, ievas@bu.edu

# Creates the views for our application 
# (implements the logic that will be displayed on the templates)

class BooksListView(ListView):
    '''View to display list of books from our database.'''
    template_name = 'project/show_all_books.html'
    model = Book
    # we want 48 books per page
    context_object_name = "results"
    paginate_by = 48

    def get_queryset(self):
        '''Override get_queryset to allow search functionality for book titles.'''
        # get the query from the GET request
        query = self.request.GET.get('q')
        # return the books that contain that specific title (case in-sensitive)
        if query:
            return Book.objects.filter(title__icontains=query)
        else:
            # else, return the default queryset
            return super().get_queryset()

    def get_context_data(self, **kwargs):
        '''Add a random book from the database to the context.'''
        context = super().get_context_data(**kwargs)
        # count the number of books using the aggregate function (count their ids)
        book_count = Book.objects.aggregate(count=Count('id'))['count']
        # get a random index from 0 to the number of books in the database
        random_index = random.randint(0, book_count - 1)
        # get the book at this index
        random_book = Book.objects.all()[random_index]
        # add it to our context variable to be able to use it in the template
        context['random_book'] = random_book
        return context


class BookDetailView(DetailView):
    '''View to display the information for one book instance.'''
    template_name = "project/book_detail.html"
    model = Book
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        '''Add context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        # call the get_reviews function to get the reviews for a book
        context['reviews'] = book.get_reviews()

        if self.request.user.is_authenticated:
            # if the user is authenticated (i.e. logged-in) then they can interact with the add to list and currently reading buttons
            person = Person.objects.get(user=self.request.user)
            # checks if the current book is in the to-read list already
            context['already_in_list'] = BookList.objects.filter(person=person, book=book).exists()
            # checks if the book is already the currently reading book
            context['is_currently_reading'] = (person.currently_reading == book)
        else:
            # For unauthenticated users, no personalized info, as they have no profile
            context['already_in_list'] = False
            context['is_currently_reading'] = False
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # redirect unauthenticated users to a login page, if they attempt to use this functionality
            return HttpResponseRedirect(reverse('login'))

        book = self.get_object()
        person = Person.objects.get(user=request.user)

        if 'add_to_list' in request.POST:
            # check if the book is already in the user's to-read list
            if not BookList.objects.filter(person=person, book=book).exists():
                # if not, add it to the list
                BookList.objects.create(person=person, book=book)

        elif 'mark_as_currently_reading' in request.POST:
            # add the book to the current user's currently reading book
            person.currently_reading = book
            # save this instance
            person.save()

        # redirect to user_detail to see the changes
        return HttpResponseRedirect(reverse('user_detail', kwargs={'pk': person.pk}))


class BookReviewDetailView(DetailView):
    '''View to display all reviews for one book instance.'''
    template_name = "project/book_reviews.html"
    model = Book
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the current book we are looking to get reviews for
        book = self.get_object()
        # call the get_reviews function from models.py
        context['reviews'] = book.get_reviews()
        return context

class UserListView(ListView):
    '''View to display the list of all users.'''
    template_name = 'project/show_all_users.html'
    model = Person
    context_object_name = "results"

class UserDetailView(DetailView):
    '''View to display the information for one user instance.'''
    template_name = "project/user_detail.html"
    model = Person
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the current person instance
        profile = self.get_object()
        # call the corresponding function from models.py to add to the context
        context['friends'] = profile.get_friends()
        context['reviews'] = profile.get_reviews()
        context['book_list'] = profile.get_book_list()
        context['books'] = Book.objects.all()
        # return context variable, in order to use these objects in the templates
        return context

    def profile_detail(request, person_id):
        # get the current logged-in user
        user = Person.objects.get(pk=person_id)
        # redirect to the user_detail view
        return render(request, 'user_detail.html', {'user': user})


class UpdateReviewView(UpdateView, LoginRequiredMixin):
    '''View used to update the information for a review (only for an authenticated user).'''

    model = Review
    form_class = UpdateReviewForm
    template_name = "project/update_review_form.html"

    def get_success_url(self):
        '''Redirect the user to their detail page after successful update.'''
        return reverse('user_detail', kwargs={'pk': self.object.person.pk})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Add the book associated with the review to the context.'''

        context = super().get_context_data(**kwargs)
        # get the current review object
        review = self.get_object()
        context['book'] = review.book
        return context

    def form_valid(self, form):
        '''Make sure the form is valid, before saving the new review as an instance.'''
        return super().form_valid(form)


class DeleteReviewView(DeleteView, LoginRequiredMixin):
    '''A view used to delete review instances.'''

    model = Review
    template_name = "project/delete_review_form.html"

    def get_success_url(self):
        '''Redirect the user to their detail page after successful deletion.'''
        return reverse('user_detail', kwargs={'pk': self.object.person.pk})

    def get_context_data(self, **kwargs: Any) -> dict:
        '''Add the user and book to the context.'''

        context = super().get_context_data(**kwargs)
        # obtain the review 
        review = self.get_object()
        # add the user and book to the context, for use in the templates
        context['user'] = review.person
        context['book'] = review.book
        return context


class CreateReviewView(CreateView, LoginRequiredMixin):
    '''A view to show the create review form
        on GET: it sends back the form
        on POST: read the form data, create an instance of a Review; save to the database
    '''

    model = Review
    form_class = CreateReviewForm
    template_name = "project/create_review_form.html"

    def get_success_url(self):
        '''Redirect the user to the book review page after successful form submission.'''
        return reverse('book_reviews', kwargs={'pk': self.object.book.pk})

    def get_context_data(self, **kwargs: Any) -> dict:
        '''Add the user and book to the context.'''

        context = super().get_context_data(**kwargs)
        # get the book primary key
        book_pk = self.kwargs['book_pk']
        context['book'] = Book.objects.get(pk = book_pk)
        # get the person object who submitted the POST request
        context['user'] = Person.objects.get(user=self.request.user)
        return context

    def form_valid(self, form):
        '''Check that the review data is valid, and save it as an instance of a Review.'''
        # save the primary key of the book review
        form.instance.book_id = self.kwargs['book_pk']
        # save the person profile who created the review
        form.instance.person = Person.objects.get(user=self.request.user)
        return super().form_valid(form)


class StatisticsListView(ListView):
    '''View to display the meaningful report of the application.'''

    model = Book
    template_name = 'project/statistics.html'
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        '''Adds the ORM filters as context variables for use in the templates.'''
        context = super().get_context_data(**kwargs)

        # use the ORM to filter books by their total reviews
        most_reviewed = Book.objects.annotate(num_reviews=Count('num_ratings')).order_by('-num_ratings')[:12]
        # use the ORM to filter books by their total number of shelvings
        most_shelved = Book.objects.order_by('-num_shelvings')[:12]
        # use the ORM to filter the best rated books of 2024
        top_2024 = Book.objects.filter(yr_published=2024).order_by('-score', '-num_ratings', 'title')[:12]
        # use the ORM to filter the worst rated books of 2024
        worst = Book.objects.filter(score__gt=0, yr_published=2024).order_by('score')[:12]

        # add the results as context variables
        context['most_reviewed'] = most_reviewed
        context['most_shelved'] = most_shelved
        context['top_2024'] = top_2024
        context['worst'] = worst
        return context

class ReviewListView(LoginRequiredMixin, ListView):
    '''A view used to list all the review instances for a user's friends'''
    model = Review
    template_name = "project/feed.html"

    def get_queryset(self):
        '''Gets the user's feed (their reviews and their friends' reviews).'''
        # get the logged-in user's person instance
        profile = Person.objects.get(user=self.request.user)
        # return the feed queryset
        return profile.get_feed()

    def get_context_data(self, **kwargs):
        '''Add variables to our context, in order to display on the templates.'''
        context = super().get_context_data(**kwargs)
        # get the current person instance associated with the logged-in user
        profile = Person.objects.get(user=self.request.user)
        # get the feed from the get_feed method from models.py
        context['feed'] = profile.get_feed()
        context['user'] = self.request.user
        return context


class CreateUserView(CreateView):
    '''A view to show the create person form
        on GET: it sends back the form
        on POST: read the form data, create an instance of Person; save to the database
    '''
    model = Person
    form_class = RegisterForm
    template_name = "project/register.html"

    def form_valid(self, form):
        '''Makes sure the form to create the user and person instance is valid.'''
        # use the django authentication models user creation form
        user_form = UserCreationForm(self.request.POST)

        # check if the form is valid
        if user_form.is_valid():
            # save the form as an instance of a user
            auth_user = user_form.save()
            person = form.instance
            # set the person's user field to the saved user instance
            person.user = auth_user
            # save the person instance
            person.save()
            # login the newly created user
            login(self.request, auth_user)

        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict:
        '''Define context variables for the template.'''

        context = super().get_context_data(**kwargs)
        # allow us to use the built-in user creation form to display the form on the template
        context['user_creation_form'] = UserCreationForm()
        return context

    def get_success_url(self):
        '''Redirect the user to their detail page after successful user creation.'''
        return reverse('user_detail', kwargs={'pk': self.object.pk})
    

class CreateFriendView(CreateView):
    '''A view used to create Friend relationships between Persons.'''

    def dispatch(self, request, *args, **kwargs):

        # get the profile associated with the logged-in user
        self_profile = Person.objects.get(user=request.user)
        other_pk = kwargs.get('other_pk')

        # get the profile associated with the other user we are trying to create a relationship with
        other_profile = Person.objects.get(pk=other_pk)

        # create the friend relationship
        self_profile.add_friend(other_profile)

        # redirect the user to their detail page after friend creation
        return redirect('user_detail', pk=self_profile.pk)
    
class ShowFriendSuggestView(LoginRequiredMixin, DetailView):
    '''View to display the friend suggestions for the logged-in user.'''
    model = Person
    template_name = "project/friend_suggest.html"

    def get_context_data(self, **kwargs):
        '''Create a context that will store the friend suggestions.'''
        context = super().get_context_data(**kwargs)
        # get the current profile
        profile = self.get_object()
        # add the profile to the context variable
        context['profile'] = profile
        # add the suggestions to the context variable
        context['suggestions'] = profile.get_friend_suggestions()
        return context
    
    def get_login_url(self) -> str:
        '''Return the URL that is required for login.'''
        return reverse('login')
    
    def get_object(self):
        '''Return the person instance associated with the profile.'''
        if not self.request.user.is_authenticated:
            # make sure the user is logged-in, else redirect to the login page
            return redirect('login')
        return Person.objects.get(user=self.request.user)
    
class CreateFriendsView(CreateView):
    '''A view used to create Friend relationships between persons.'''

    def dispatch(self, request, *args, **kwargs):

        # get the profile associated with the logged-in user
        self_profile = Person.objects.get(user=request.user)
        other_pk = kwargs.get('other_pk')

        # get the profile associated with the other user we are trying to create a relationship with
        other_profile = Person.objects.get(pk=other_pk)

        # create the friend relationship
        self_profile.add_friend(other_profile)

        # redirect the user to their detail page after friend creation
        return redirect('user_detail', pk=self_profile.pk)
