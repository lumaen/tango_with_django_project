from django.contrib import admin
from rango.models import Category, Page

# Change the Page visualisation in the Admin page
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

# Class to autofill the slug blank in the Category
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Registered models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
