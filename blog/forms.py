from django import forms
from .models import Comment, Article

class CreateCommentForm(forms.ModelForm):
    '''A form to create Comment data.'''

    class Meta:
        '''Associate this form with the Comment model'''
        model = Comment

        # remove the article because we want this done automatically
        fields = ['author', 'text',]


class CreateArticleForm(forms.ModelForm):
    '''A form to create a new Article'''

    class Meta:
        '''Associate this form with a model.'''
        model = Article 
        fields = ['author', 'title', 'text', 'image_file']