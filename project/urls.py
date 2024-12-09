from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# Ieva sagaitis, ievas@bu.edu

urlpatterns = [
    path('', views.BooksListView.as_view(), name = "home"),
    path('books', views.BooksListView.as_view(), name = "books"),
    path('books/<int:pk>', views.BookDetailView.as_view(), name = "book_detail"),
    path('users', views.UserListView.as_view(), name = "users"),
    path('user/<int:pk>', views.UserDetailView.as_view(), name = "user_detail"),
    path('book_reviews/<int:pk>', views.BookReviewDetailView.as_view(), name = "book_reviews"),

    path(r'review/<int:pk>/update', views.UpdateReviewView.as_view(), name="update_review"),
    path(r'review/<int:pk>/delete', views.DeleteReviewView.as_view(), name="delete_review"),
    path(r'book/<int:book_pk>/review/create/', views.CreateReviewView.as_view(), name='create_review'),
    path(r'books/', views.BooksListView.as_view(), name='books_list'),
    path('statistics/', views.StatisticsListView.as_view(), name='statistics'),
    path('feed/', views.ReviewListView.as_view(), name='feed'),
    path(r'person/add_friends/<int:other_pk>', views.CreateFriendsView.as_view(), name="add_friends"),
    path(r'profile/friend_suggest', views.ShowFriendSuggestView.as_view(), name="friend_suggest"), #

    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
     path(r'register/', views.CreateUserView.as_view(), name="register"),
]