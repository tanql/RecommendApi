from django.contrib.auth.models import User
from .models import Movie, Genre, Rating
from rest_framework import routers, serializers, viewsets




class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre

class MovieSerializer(serializers.ModelSerializer):
    movieGenre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ('movieName', 'movieGenre', 'movieId', 'year')

class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer
    movie = MovieSerializer

    class Meta:
        model = Rating
        fields = {'ratingValue','movie','user'}