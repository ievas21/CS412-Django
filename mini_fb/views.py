from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse
from typing import Any, Dict

# Ieva sagaitis, ievas@bu.edu
# Creates the views for the application

class ShowAllProfilesView(ListView):
    '''A view to show all Profiles, take in a generic ListView to inherit from'''

    model = Profile
    template_name ='mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    '''Show one profile by its primary key.'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = "profile"

class CreateProfileView(CreateView):
    '''A view to show the create profile form
        on GET: it sends back the form
        on POST: read the form data, create an instance of Profile; save to the database
    '''

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"
    
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    

class CreateStatusMessageView(CreateView):
    '''A view to show the create status message form
        on GET: it sends back the form
        on POST: read the form data, create an instance of Status Message; save to the database
    '''

    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    
    def form_valid(self, form):
        # Assign the profile to the status message based on the URL's pk

        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''build a dictionary of key-value pairs that become context variables '''

        # superclass context data
        context = super().get_context_data(**kwargs)

        # find the pk from the URL
        pk = self.kwargs['pk']

        # find the corresponding article
        profile = Profile.objects.get(pk=pk)

        # add article to context data
        context['profile'] = profile
        return context

