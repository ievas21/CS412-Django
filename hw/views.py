from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.

# def home(request):
#     '''A function to respons to the /hw URL. 
#        Comment this out if using the next function with HTML template.
#     '''

        
#     response_text = f'''
#         <html>
#         <h1>Hello, world!</h1>
#         <p>
#             This is our first django web page!
#         </p>
#         <hr>
#         This page was generated at {time.ctime()}.
#         '''

#         # return a response to the client
#     return HttpResponse(response_text)

def home(request):
    '''A function to respons to the /hw URL. This function will delegate work to an HTML template
    '''
    
    template_name = "hw/home.html"

    # create a dictionary of context variables

    context = {
        'current_time': time.ctime(),
        'letter1': chr(random.randint(65,90)),
        'letter2': chr(random.randint(65,90)),
        'number': random.randint(1, 10),
    }

    # delegate response to the template:

    return render(request, template_name, context)

def about(request):
    '''A function to respons to the /hw URL. This function will delegate work to an HTML template
    '''
    
    template_name = "hw/about.html"

    # create a dictionary of context variables

    context = {
        'current_time': time.ctime(),
    }

    # delegate response to the template:

    return render(request, template_name, context)