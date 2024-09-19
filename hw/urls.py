
from django.urls import path
from django.conf import settings
from . import views

# create a list of urls for this app

urlpatterns = [
    path(r'', views.home, name="home"), # for main page
    path(r'about', views.about, name="about"), # for about page
]