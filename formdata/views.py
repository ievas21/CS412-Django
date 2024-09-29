from django.shortcuts import render, redirect, HttpResponse

# Create your views here.


def show_form(request):
    '''Show the HTML form to the client'''

    template_name = 'formdata/form.html'
    return render(request, template_name)


def submit(request):
    '''Handle the form subission. Read out the form data. Generate a response.
    '''

    template_name = 'formdata/confirmation.html'

    # read the form data into python variables
    print(request)

    # check if the request is a POST (versus a GET)
    if request.POST:
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']

        # package the data up to be used in the response
        context = {
            'name': name,
            'favorite_color': favorite_color,

        }
        # generate a response
        return render(request, template_name, context)
    
    # GET lands down here: no return statements -- redirects to the correct url
    return redirect("show_form")

    # this is a better solution, but shows the wrong url
    # template_name = 'formdata/form.html'
    # return (request, template_name)
