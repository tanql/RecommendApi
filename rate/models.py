from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from registration.models import MyUser
from datetime import datetime


# Create your models here.


class Genre(models.Model):
    genre=models.CharField(max_length=120, blank=False, null=False)
    user=models.ManyToManyField(MyUser)
class Movie(models.Model):
    movieName=models.CharField(max_length=200, blank=False, null=False)
    movieGenre=models.ManyToManyField(Genre)
    movieId=models.IntegerField()
    year=models.IntegerField()


class Rating(models.Model):
    ratingValue=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    movie=models.ForeignKey(Movie)
    user=models.ForeignKey(MyUser, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)

