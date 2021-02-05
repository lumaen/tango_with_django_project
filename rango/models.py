from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Class that defines a Category
class Category(models.Model):
    # Field that holds the name of the category
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    # Overridden method for saving a Category and formatting the URL
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    # This handles the plural version of "Category" on the admin site
    class Meta:
        verbose_name_plural = "categories"

    # Method to return the name of the category
    def __str__(self):
        return self.name


# Class that defines a Page of some Category
class Page(models.Model):
    # Fields
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    # Method to return the title of the page
    def __str__(self):
        return self.title

# Class that defines an User
class UserProfile(models.Model):
    # Link UserProfile to a User model instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional attributes to include
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
