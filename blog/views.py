from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView, CreateView
import random
from django.urls import reverse
from typing import Any

# Create your views here.
class ShowAllView(ListView):
    '''A view to show all Articles'''

    model = Article
    template_name ='blog/show_all.html'
    context_object_name = 'articles'

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

class CreateCommentView(CreateView):
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
    

class CreateArticleView(CreateView):
    '''View to create a new Article instance.'''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
        '''Add some debugging statements.'''
        print(f'CreateArticleView.form_valid: form.cleaned_data={form.cleaned_data}')

        # delegate work to the super class
        return super().form_valid(form)

    
 
