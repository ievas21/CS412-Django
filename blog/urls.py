
from django.urls import path
from django.conf import settings
from . import views

# create a list of urls for this app

urlpatterns = [
    path(r'', views.ShowAllView.as_view(), name="show_all"),
]
