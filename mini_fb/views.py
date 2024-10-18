from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
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

        sm = form.save()
        files = self.request.FILES.getlist('files')

        for file in files:
            image = Image()
            image.status_message = sm
            image.image_file = file

            image.save()

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

class UpdateProfileView(UpdateView):
    '''A view used to update Profile data.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
class DeleteStatusMessageView(DeleteView):
    '''A view used to delete status messages.'''

    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"

    def get_success_url(self):

        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    def get_context_data(self, **kwargs: Any) -> dict:
        '''Add the profile and status message to the context.'''

        context = super().get_context_data(**kwargs)
        status_message = self.get_object()  
        context['profile'] = status_message.profile
        context['status_message'] = status_message  
        
        return context
    
    
class UpdateStatusMessageView(UpdateView):
    '''A view used to update status messages.'''

    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Add the profile associated with the status message to the context'''

        context = super().get_context_data(**kwargs)
        status_message = StatusMessage.objects.get(pk=self.kwargs['pk'])
        context['profile'] = status_message.profile

        return context
    

