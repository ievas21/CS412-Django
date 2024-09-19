from django.shortcuts import render
import random, time
from django.http import HttpRequest, HttpResponse

pictures = [
    'https://cs-people.bu.edu/ievas/a03/frida-1.jpg',
    'https://cs-people.bu.edu/ievas/a03/frida-3.jpg',
    'https://cs-people.bu.edu/ievas/a03/frida-4.jpeg',
    'https://cs-people.bu.edu/ievas/a03/frida-5.jpg',
]

quotes = [
    'I paint self-portraits because I am so often alone, because I am the person I know best.',
    'Fall in love with yourself, with life and then with whoever you want.',
    'At the end of the day, we can endure much more than we think we can.',
    'I am not sick. I am broken. But, I am happy to be alive as long as I can paint.',
    'Nothing is absolute. Everything changes, everything moves, everything revolves, everything flies and goes away.',
]

# Create your views here.
def quote(request):
    '''A function to respond to the /quote URL. This function will delegate work to an HTML template
    '''
    
    template_name = "quotes/quote.html"

    selected_image = random.choice(pictures)
    selected_quote = random.choice(quotes)

    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
        'chosen_picture': selected_image,
        'chosen_quote': selected_quote,
    }

    # delegate response to the template:
    return render(request, template_name, context)

def about(request):
    '''A function to respond to the /about URL. This function will delegate work to an HTML template
    '''
    
    template_name = "quotes/about.html"

    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
    }

    # delegate response to the template:
    return render(request, template_name, context)

def show_all(request):
    '''A function to respond to the /show_all URL. This function will delegate work to an HTML template
    '''
    
    template_name = "quotes/show_all.html"

    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
        'pictures': pictures,
        'quotes': quotes,
    }

    # delegate response to the template:
    return render(request, template_name, context)
