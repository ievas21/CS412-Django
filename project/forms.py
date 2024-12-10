from django import forms
from .models import Person, Review

# Ieva sagaitis, ievas@bu.edu
# Creates forms for our project that are used for CRUD operations

class RegisterForm(forms.ModelForm):
    '''A form to create Person data.'''

    class Meta:
        '''Associate this form with the Person model.'''
        model = Person

        # define the fields that we want the user to fill in
        fields = ['first_name', 'last_name', 'email', 'image_url']

        # design the field inputs for styling
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


class UpdateReviewForm(forms.ModelForm):
    '''A form to update Review data.'''

    # define the rating choices that the user will select from in the form
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    # define the rating field to use the rating choices above as a radio select input
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(),
        label=''
    )

    class Meta:
        '''Associate this form with the Review model.'''
        model =Review

        # only change the review and rating field.
        fields = ['review', 'rating']

        widgets = {

            'review': forms.Textarea(attrs={
                'class': 'large-text-field',
                'style': 'width: 700px; height: 150px;',
                'rows': 8,
                'cols': 60,
            }),
        }
        labels = {
            'review': '', 
        }

class CreateReviewForm(forms.ModelForm):
    '''A form to create Review data.'''

    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(),
        label='Rating'
    )

    class Meta:
        '''Associate this form with the Review model'''
        model =Review

        # only change these fields
        fields = ['review', 'rating']

        # design the field inputs for styling
        widgets = {
            'review': forms.Textarea(attrs={
                'class': 'large-text-field',
                'style': 'width: 700px; height: 150px;',
                'rows': 8,
                'cols': 60,
            }),
        }
        # remove the label from review
        labels = {
            'review': '', 
        }