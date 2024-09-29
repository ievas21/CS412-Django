from django.shortcuts import render, redirect
import random
import time
from datetime import datetime, timedelta
from django.http import HttpRequest, HttpResponse

food = [
    'Kugelis - $13.99',
    'Pan Fried Zeppelins - $13.99',
    'Crepes with Cottage Cheese - $13.99'
]

prices = {
    'Potato Pancakes': 15.99,
    'Fried Bread with Cheese and Garlic': 16.99,
    'Summer Borshch with Potatoes': 5.99,
    'Bowl of Summer Borshch': 3.00,
    'Add Potatoes': 1.99,
    'Daily Special': 13.99, 
    'Chicken Kiev': 20.99
}

# Create your views here.
def main(request):
    '''A function to respond to the /main URL. This function will delegate work to an HTML template
    '''

    template_name = "restaurant/main.html"

    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
    }

    # delegate response to the template:
    return render(request, template_name, context)


def order(request):
    '''Handle the form submission. Read out the form data. Generate a response.
    '''

    template_name = 'restaurant/order.html'

    selected_food = random.choice(food)

    context = {
        'current_time': time.ctime(),
        'special': selected_food,
    }

    return render(request, template_name, context)


def confirmation(request):
    '''A function to respond to the /confirmation URL. This function will delegate work to an HTML template
    '''

    template_name = "restaurant/confirmation.html"

    selected_food = random.choice(food)

    # check if the request is a POST (versus a GET)
    if request.POST:
        items = request.POST.getlist('item')
        instructions = request.POST.get('instructions', '')
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')

        total_price = sum(prices[item] for item in items)

        random_minutes = random.randint(30, 60)
        time = datetime.now() + timedelta(minutes=random_minutes)

        # package the data up to be used in the response
        context = {
            'current_time': time.ctime(),
            'special': selected_food,
            'items': items,
            'instructions': instructions,
            'name': name,
            'phone': phone,
            'email': email,
            'total_price': f"${total_price:}",
            'time': time,
        }

        # generate a response
        return render(request, template_name, context)

    # GET lands down here: no return statements -- redirects to the correct url
    context = {
        'current_time': time.ctime(),
        'special': selected_food,
    }

    return redirect("order")