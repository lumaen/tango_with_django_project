# Classes to represent forms

from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User

# Form for gathering data about Category
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # Class to provide additional information about the form
    class Meta:
        # Provide association between this form and ModelForm
        model = Category
        # Fields to include
        fields = ('name', )

# Form for gathering data about Page
class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200,
                            help_text='Please enter the URL of the page.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # Class to provide additional information about the form
    class Meta:
        # Provide association between this form and ModelForm
        model = Page
        # Fields to hide from the form
        exclude = ('category', )
        # Fields to include
        #fields = ('title', 'url', 'views')

    # Overridden version of clean() to better get the Page URL
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If URL is not empty and doesn't start with http://, then add it
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data

# Form for authenticating Users
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    # Class to provide additional information about the form
    class Meta:
        model = User
        fields = ('username', 'email', 'password', )

# Form for authenticating Users
class UserProfileForm(forms.ModelForm):
    # Class to provide additional information about the form
    class Meta:
        model = UserProfile
        fields = ('website', 'picture', )
