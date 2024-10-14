from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to create Profile data.'''

    class Meta:
        '''Associate this form with the Profile model'''
        model = Profile

        fields = ['first_name', 'last_name', 'city', 'email', 'image_url']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'small-text-field',
                'placeholder': 'First Name',
                'style': 'width: 150px; margin-right: 50px;',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'small-text-field',
                'placeholder': 'Last Name',
                'style': 'width: 150px; margin-right: 50px;',
            }),
            'city': forms.TextInput(attrs={
                'class': 'small-text-field',
                'placeholder': 'City',
                'style': 'width: 150px; margin-right: 0;',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'small-text-field',
                'placeholder': 'Email Address',
                'style': 'width: 150px; margin-right: 13px;',
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'small-text-field',
                'placeholder': 'Profile Image URL',
                'style': 'width: 150px; margin-right: 45px;',
            }),
        }

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to create Status Message data.'''

    class Meta:
        '''Associate this form with the Status Message model'''
        model = StatusMessage

        fields = ['message']

        widgets = {
            'message': forms.TextInput(attrs={
                'class': 'large-text-field',
                'style': 'width: 400px;',
            }),
        }

 