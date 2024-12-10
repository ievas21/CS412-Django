from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# Ieva sagaitis, ievas@bu.edu

urlpatterns = [
    path('', views.BooksListView.as_view(), name = "home"), # shows all the books (serves as the main page of the application)
    path('books', views.BooksListView.as_view(), name = "books"), # shows all the books (serves as the main page of the application)
    path('books/<int:pk>', views.BookDetailView.as_view(), name = "book_detail"), # shows the details on one specific book that the user chose
    path('users', views.UserListView.as_view(), name = "users"), # shows all the users in the application (can be accessed if not authenticated)
    path('user/<int:pk>', views.UserDetailView.as_view(), name = "user_detail"), # shows the details of one specific user
    path('book_reviews/<int:pk>', views.BookReviewDetailView.as_view(), name = "book_reviews"), # shows all reviews that pertain to one book

    path(r'review/<int:pk>/update', views.UpdateReviewView.as_view(), name="update_review"), # shows the form used to update a review that a user created
    path(r'review/<int:pk>/delete', views.DeleteReviewView.as_view(), name="delete_review"), # shows the form used to delete a review
    path(r'book/<int:book_pk>/review/create/', views.CreateReviewView.as_view(), name='create_review'), # shows the form to create a review
    path(r'books/', views.BooksListView.as_view(), name='books_list'), # shows the books as a list, another url
    path('statistics/', views.StatisticsListView.as_view(), name='statistics'), # shows the statistics report for the books
    path('feed/', views.ReviewListView.as_view(), name='feed'), # shows the logged-in user's feed
    path(r'person/add_friends/<int:other_pk>', views.CreateFriendsView.as_view(), name="add_friends"), # redirects the user after adding a friend
    path(r'profile/friend_suggest', views.ShowFriendSuggestView.as_view(), name="friend_suggest"), # shows the friend suggestions for a user

    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'), # shows the login page for users
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'), # shows the logout page for users
     path(r'register/', views.CreateUserView.as_view(), name="register"), # redirects the user to the page to register an account and a profile associated with it
]