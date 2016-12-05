from django.contrib.auth.models import User
from .models import Movie, Genre, Rating
from rest_framework import serializers
from registration.serializers import MyUserSerializer




class GenreSerializer(serializers.ModelSerializer):
    user = MyUserSerializer(many=True)

    class Meta:
        model = Genre
        fields = ('genre', 'user')

class MovieSerializer(serializers.ModelSerializer):
    movieGenre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ('movieName', 'movieGenre', 'movieId', 'year')

class RatingSerializer(serializers.ModelSerializer):
    user = MyUserSerializer()
    movie = MovieSerializer()

    class Meta:
        model = Rating
        fields = ('ratingValue','movie','user')