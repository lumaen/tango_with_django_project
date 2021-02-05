from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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


@login_required
def add_category(request):
    form = CategoryForm()

    # HTTP POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Is it a valid form?
        if form.is_valid():
            # Save the category to the db
            form.save(commit=True)
            # Confirm the category is saved by returning to index
            return redirect('/rango/')

        # 'Form has errors' case
        else:
            print(form.errors)

    #Handle the bad form, new form, no form
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    # Try and get the Page Category
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # It is not possible to add a Page without a Category
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    # HTTP POST
    if request.method == 'POST':
        form = PageForm(request.POST)

        # Is it a valid form?
        if form.is_valid():
            if category:
                # Save the page to the db
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                # Confirm the category is saved by returning to the Category
                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug': category_name_slug}))

            # 'Form has errors' case
            else:
                print(form.errors)

    #Handle the bad form, new form, no form
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):
    # Boolean to tell if the registration was successful
    registered = False

    # If it is an HTTP POST, we process the data
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # Is it a valid form?
        if user_form.is_valid() and profile_form.is_valid():
            # Save User's data to db
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # Is there a profile picture?
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            # All done
            registered = True

        # "Form has errors" case
        else:
            print(user_form.errors, profile_form.errors)

    # Not an HTTP POST
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template
    return render(request, 'rango/register.html',
                  context = {'user_form': user_form,
                            'profile_form': profile_form,
                            'registered': registered})


def user_login(request):
    # If it is an HTTP POST, we process the data
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Are the credentials correct?
        user = authenticate(username=username, password=password)

        # If we have an User object, then proceed
        if user:
            # Is the account active?
            if user.is_active:
                # Login the user
                login(request, user)
                return redirect(reverse('rango:index'))
            # "Not active" case
            else:
                return HttpResponse("Your Rango account is disabled.")

        # "Not User object" case
        else:
            # Wrong credentials
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    # Not an HTTP POST, go back to login page
    else:
        # Render the login template
        return render(request, 'rango/login.html')

@login_required
def user_logout(request):
    # Just logout the user
    logout(request)
    # Redirect the user to the Homepage
    return redirect(reverse('rango:index'))


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')
