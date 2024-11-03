from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView, CreateView
import random
from django.urls import reverse
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.
class ShowAllView(ListView):
    '''A view to show all Articles'''

    model = Article
    template_name ='blog/show_all.html'
    context_object_name = 'articles'

    def dispatch(self, request):
        '''add this method to show/debug logged in user'''
        print(f"Logged in user: request.user={request.user}")
        print(f"Logged in user: request.user.is_authenticated={request.user.is_authenticated}")
        return super().dispatch(request)
    

class RandomArticleView(DetailView):
    '''Pick one random article and show it'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = "article"

    def get_object(self):
        '''Return the instance of the Article object to show.'''

        # get all articles
        all_articles = Article.objects.all() # SELECT *
        # pick one at random
        return random.choice(all_articles) 
    
    
class ArticleView(DetailView):
    '''Show one article by its primary key.'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = "article"

class CreateCommentView(LoginRequiredMixin, CreateView):
    '''A view to show the creare comment form
        on GET: it sends back the form
        on POST: read the form data, create an instance of Comment; save to the database
    '''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    # what to do after submission

    def get_success_url(self) -> str:
        return reverse("article", kwargs = self.kwargs)

    def form_valid(self, form):
        '''Executes after form submission'''

        print(f'CreateCommentView.form_valid(): form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid(): self.kwargs={self.kwargs}')

        # find the article with the PK from the URL
        article = Article.objects.get(pk=self.kwargs['pk'])

        # attatch the article to the comment
        # form.instance is the new Comment object
        form.instance.article = article

        return super().form_valid(form)
    
    def get_context_object_name(self, **kwargs: Any) -> dict[str, Any]:
        '''build a dictionary of key-value pairs that become context variables '''
        # superclass context data
        context = super().get_context_data(**kwargs)
        # find the pk from the URL
        pk = self.kwargs['pk']
        # find the corresponding article
        article = Article.objects.get(pk=pk)
        # add article to context data
        context['article'] = article
        return context
    

class CreateArticleView(LoginRequiredMixin, CreateView):
    '''View to create a new Article instance.'''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
        '''Add some debugging statements.'''
        print(f'CreateArticleView.form_valid: form.cleaned_data={form.cleaned_data}')
        # find which user is logged in
        user = self.request.user
        # attach the user to the new article instance
        form.instance.user = user
        # delegate work to the super class
        return super().form_valid(form)
    
    def get_login_url(self) -> str:
        '''Return the URL that is required for login.'''
        return reverse('login')
    

class RegistrationView(CreateView):
    '''Display and process the UserCreationForm for account registration'''

    template_name ='blog/register.html'
    form_class = UserCreationForm

    def dispatch(self, *args, **kwargs):
        '''Handle the User creation process.'''

        # we handle the HTTP POST request
        if self.request.POST:
 
            # reconstruct the UserCreationForm from the HTTP POST
            form =UserCreationForm(self.request.POST)
            print(f'Form={form}')

            if not form.is_valid():
                return super().dispatch(*args, **kwargs)

            # save the new User object -- creates a new instance of the User object in the database
            user = form.save() 

            # login the User
            login(self.request, user)

            ## mini_fb note: take the user and attatch it to Profile creation form before saving

            # re-direct to some page view
            return redirect(reverse('show_all'))

        # let the default superclass CreateView handle the HTTP GET
        return super().dispatch(*args, **kwargs)

    
 
