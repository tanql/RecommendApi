from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import MyUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','email')

class MyUserSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = MyUser
        fields = ('user','userID','age','postCode')
