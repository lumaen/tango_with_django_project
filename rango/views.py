# PAGE 108



from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

def index(request):
    # List of the Categories
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]

    # Costruct a dictionary to pass the template engine as its context.
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = pages_list

    # Return a rendered response
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    # Return a rendered response
    return render(request, 'rango/about.html')


def show_category(request, category_name_slug):
    # Costruct a dictionary to pass the template engine as its context.
    context_dict = {}

    try:
        # Get the Category that has the provided slug
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve the associated Pages
        pages = Page.objects.filter(category=category)

        # Add Category and Pages to the context dictionary
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        # If no category is found, then set them to null
        context_dict['pages'] = None
        context_dict['category'] = None

    # Return a rendered response
    return render(request, 'rango/category.html', context=context_dict)
