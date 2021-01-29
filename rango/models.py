from django.db import models

# Class that defines a Category
class Category(models.Model):
    # Field that holds the name of the category
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    # This handles the plural version of "Category" on the admin site
    class Meta:
        verbose_name_plural = "Categories"

    # Method to return the name of the category
    def __str__(self):
        return self.name


# Class that defines a Page of some Category
class Page(models.Model):
    # Fields
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    # Method to return the title of the page
    def __str__(self):
        return self.title
