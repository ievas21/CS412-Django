from django import forms
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    '''A form to create Comment data.'''

    class Meta:
        '''Associate this form with the Comment model'''
        model = Comment

        # remove the article because we want this done automatically
        fields = ['author', 'text',]