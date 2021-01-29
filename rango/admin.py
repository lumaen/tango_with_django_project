from django.contrib import admin
from rango.models import Category, Page

# Change the Page visualisation in the Admin page
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


# Registered models
admin.site.register(Category)
admin.site.register(Page, PageAdmin)
