from django.urls import path
from django.conf import settings
from . import views

# create a list of urls for this app

urlpatterns = [
    path(r'', views.quote, name="quote"), # for main page
    path(r'about', views.about, name="about"), # for about page
    path(r'showall', views.showall, name="showall"), # for show all page
]