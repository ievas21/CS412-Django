from django.urls import path
from django.conf import settings
from . import views

# create a list of urls for this app

urlpatterns = [
    path(r'', views.main, name="main"), # for main page
    path(r'main',views.main, name="main"), # for main page again
    path(r'order',views.order, name="order"),
    path(r'confirmation',views.confirmation, name="confirmation"),
]