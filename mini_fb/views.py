from django.shortcuts import render
from .models import *
from django.views.generic import ListView

# Ieva sagaitis, ievas@bu.edu
# Creates the views for the application -- only the list view of all profiles

class ShowAllProfilesView(ListView):
    '''A view to show all Profiles, take in a generic ListView to inherit from'''

    model = Profile
    template_name ='mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'