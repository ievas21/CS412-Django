
from django.urls import path
from django.conf import settings
from . import views

# Creates a list of urls for this app
# Ieva sagaitis, ievas@bu.edu

urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name="show_profile"),
    path(r'profile/create_profile', views.CreateProfileView.as_view(), name="create_profile"),
    path(r'profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name="create_status"),
    
]