from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # Costruct a dictionary to pass the template engine as its context.
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    # Return a rendered response
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # Return a rendered response
    return render(request, 'rango/about.html')
