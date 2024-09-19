from django.urls import path
from django.conf import settings
from . import views

# create a list of urls for this app

urlpatterns = [
    path(r'', views.quote, name="quote"), # for main page
    path(r'quote', views.quote, name="quote"), # for main page again
    path(r'about', views.about, name="about"), # for about page
    path(r'show_all', views.show_all, name="show_all"), # for show all page
]