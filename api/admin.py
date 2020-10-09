from django.contrib import admin
from .models import Genres, Categories, Titles


# Register your models here.
admin.site.register(Genres)
admin.site.register(Categories)
admin.site.register(Titles)