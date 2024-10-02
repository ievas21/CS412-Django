
from django.urls import path
from django.conf import settings
from . import views

# Creates a list of urls for this app -- which is only the main page for now
# Ieva sagaitis, ievas@bu.edu

urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
]