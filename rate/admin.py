from django.contrib import admin
from .models import Rating, Movie, Genre
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Genre)
