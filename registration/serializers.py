from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import MyUser



class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('username','password')

class MyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('user','userID')
