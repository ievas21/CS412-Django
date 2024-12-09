from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Book, Person, Review, BookList
from django.urls import reverse
from .forms import UpdateReviewForm, CreateReviewForm, UpdateUserForm,  RegisterForm
from typing import Any
from django.db.models import Avg, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.http import HttpResponseRedirect
import random
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as AuthUser

# Create your views here.


class BooksListView(ListView):
    '''View to display list of books'''
    template_name = 'project/show_all_books.html'
    model = Book
    context_object_name = "results"
    paginate_by = 48

    def get_queryset(self):
        '''Override get_queryset to allow search functionality for book titles.'''
        query = self.request.GET.get('q')
        if query:
            return Book.objects.filter(title__icontains=query)
        else:
            return super().get_queryset()

    def get_context_data(self, **kwargs):
        '''Add a random book to the context.'''
        context = super().get_context_data(**kwargs)

        book_count = Book.objects.aggregate(count=Count('id'))['count']
        random_index = random.randint(0, book_count - 1)
        random_book = Book.objects.all()[random_index]
        context['random_book'] = random_book

        return context


class BookDetailView(DetailView):
    '''View to display the information for one book.'''
    template_name = "project/book_detail.html"
    model = Book
    context_object_name = "book"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        book = self.get_object()

        context['reviews'] = book.get_reviews()
        if self.request.user.is_authenticated:
            person = Person.objects.get(user=self.request.user)
            context['already_in_list'] = BookList.objects.filter(person=person, book=book).exists()
            context['is_currently_reading'] = (person.currently_reading == book)
        else:
            # For unauthenticated users, no personalized info
            context['already_in_list'] = False
            context['is_currently_reading'] = False
        return context

    def post(self, request, *args, **kwargs):
        # Retrieve the book object
        if not request.user.is_authenticated:
            # Redirect unauthenticated users to a login page or handle gracefully
            return HttpResponseRedirect(reverse('login'))

        book = self.get_object()
        person = Person.objects.get(user=request.user)

        if 'add_to_list' in request.POST:
            # Check if the book is already in the user's to-read list
            if not BookList.objects.filter(person=person, book=book).exists():
                BookList.objects.create(person=person, book=book)

        elif 'mark_as_currently_reading' in request.POST:
            person.currently_reading = book
            person.save()

        return HttpResponseRedirect(reverse('user_detail', kwargs={'pk': person.pk}))


class BookReviewDetailView(DetailView):
    '''View to display all reviews for one book.'''
    template_name = "project/book_reviews.html"
    model = Book
    context_object_name = "book"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['reviews'] = book.get_reviews()

        return context


class UserListView(ListView):
    '''View to display list of users'''
    template_name = 'project/show_all_users.html'
    model = Person
    context_object_name = "results"


class UserDetailView(DetailView):
    '''View to display the information for one user.'''
    template_name = "project/user_detail.html"
    model = Person
    context_object_name = "user"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['friends'] = profile.get_friends()
        context['reviews'] = profile.get_reviews()
        context['book_list'] = profile.get_book_list()
        context['books'] = Book.objects.all()

        return context

    def profile_detail(request, person_id):
        user = Person.objects.get(pk=person_id)
        return render(request, 'profile_detail.html', {'user': user})


class UpdateReviewView(UpdateView, LoginRequiredMixin):
    '''View used to update the information for a view.'''

    model = Review
    form_class = UpdateReviewForm
    template_name = "project/update_review_form.html"

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.object.person.pk})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Add the book associated with the review to the context'''

        context = super().get_context_data(**kwargs)
        review = self.get_object()
        context['book'] = review.book

        return context

    def form_valid(self, form):
        return super().form_valid(form)


class DeleteReviewView(DeleteView, LoginRequiredMixin):
    '''A view used to delete reviews.'''

    model = Review
    template_name = "project/delete_review_form.html"

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.object.person.pk})

    def get_context_data(self, **kwargs: Any) -> dict:
        '''Add the user and book to the context.'''

        context = super().get_context_data(**kwargs)
        review = self.get_object()
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
        return reverse('book_reviews', kwargs={'pk': self.object.book.pk})

    def get_context_data(self, **kwargs: Any) -> dict:
        '''Add the user and book to the context.'''

        context = super().get_context_data(**kwargs)
        book_pk = self.kwargs['book_pk']
        context['book'] = Book.objects.get(pk = book_pk)
        context['user'] = Person.objects.get(user=self.request.user)

        return context

    def form_valid(self, form):
        '''Check that the review data is valid, and save it as an instance of a Review.'''

        form.instance.book_id = self.kwargs['book_pk']
        form.instance.person = Person.objects.get(user=self.request.user)
        return super().form_valid(form)


class StatisticsListView(ListView):
    model = Book
    template_name = 'project/statistics.html'
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        most_reviewed = Book.objects.annotate(num_reviews=Count(
            'num_ratings')).order_by('-num_ratings')[:12]
        most_shelved = Book.objects.order_by('-num_shelvings')[:12]
        top_2024 = Book.objects.filter(yr_published=2024).order_by(
            '-score', '-num_ratings', 'title')[:12]
        worst = Book.objects.filter(
            score__gt=0, yr_published=2024).order_by('score')[:12]

        context['most_reviewed'] = most_reviewed
        context['most_shelved'] = most_shelved
        context['top_2024'] = top_2024
        context['worst'] = worst

        return context


class UpdateUserView(LoginRequiredMixin, UpdateView):
    '''A view used to update user data.'''

    model = Person
    form_class = UpdateUserForm
    template_name = "project/update_user_form.html"

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.request.person.profile.pk})

    def get_object(self):
        if not self.request.person.is_authenticated:
            return redirect('login')
        return Person.objects.get(person=self.request.person)


class ReviewListView(LoginRequiredMixin, ListView):
    '''A view used to list all the reviews for a user's friends'''

    model = Review
    template_name = "project/feed.html"

    def get_queryset(self):
        # Get the logged-in user's `Person` instance
        profile = Person.objects.get(user=self.request.user)
        # Return the feed queryset
        return profile.get_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Person.objects.get(user=self.request.user)
        context['feed'] = profile.get_feed()
        context['user'] = self.request.user
        return context


class CreateUserView(CreateView):
    '''A view to show the create user form
        on GET: it sends back the form
        on POST: read the form data, create an instance of User; save to the database
    '''
    model = Person
    form_class = RegisterForm
    template_name = "project/register.html"

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            auth_user = user_form.save()
            person = form.instance
            person.user = auth_user
            person.save()
            login(self.request, auth_user)

        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict:
        '''Define context variables for the template.'''

        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()

        return context

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.object.pk})
    

class CreateFriendView(CreateView):
    '''A view used to create Friends'''

    def dispatch(self, request, *args, **kwargs):

        # Get the profile associated with the logged-in user
        self_profile = Person.objects.get(user=request.user)
        other_pk = kwargs.get('other_pk')
        other_profile = Person.objects.get(pk=other_pk)

        # Create the friend relationship
        self_profile.add_friend(other_profile)

        return redirect('user_detail', pk=self_profile.pk)
    
class ShowFriendSuggestView(LoginRequiredMixin, DetailView):
    model = Person
    template_name = "project/friend_suggest.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        profile = self.get_object()
        context['profile'] = profile
        context['suggestions'] = profile.get_friend_suggestions()
        
        return context
    
    def get_login_url(self) -> str:
        '''Return the URL that is required for login.'''
        return reverse('login')
    
    def get_object(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return Person.objects.get(user=self.request.user)
    
class CreateFriendsView(CreateView):
    '''A view used to create Friends'''

    def dispatch(self, request, *args, **kwargs):

        # Get the profile associated with the logged-in user
        self_profile = Person.objects.get(user=request.user)
        other_pk = kwargs.get('other_pk')
        other_profile = Person.objects.get(pk=other_pk)

        # Create the friend relationship
        self_profile.add_friend(other_profile)

        return redirect('user_detail', pk=self_profile.pk)
