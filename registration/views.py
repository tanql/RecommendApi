from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .serializers import UserSerializer, MyUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rate.disable import CsrfExemptSessionAuthentication
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rate.models import Rating, Genre
from rate.serializers import RatingSerializer, GenreSerializer
import math
from functions.memoryBasedFiltering import pearson


userID = 945

#functions to calculate similarities (pearson correlation)


class CurrentUser(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request, format=None):
        if 'user' in request.GET:
            user = User.objects.get(username=request.GET['user'])
            myuser=MyUser.objects.get(user=user)
        else:
            myuser=MyUser.objects.get(user=request.user)
        genres=Genre.objects.filter(user=myuser)
        serializer = MyUserSerializer(instance=myuser)
        ratings=Rating.objects.filter(user=myuser).order_by('-date')
        listOfRatings = []
        babe=serializer.data
        babe['interests']=[]
        for genre in genres:
            babe['interests'].append(genre.genre)
        if (len(ratings)==0):
            return Response(babe)
        else:
            if 'user' in request.GET:
                listOfRatings=[]
                count = 0
                for rating in ratings:
                    count=count+1
                    newser=RatingSerializer(instance=rating)
                    listOfRatings.append(newser.data)
                    if (count==5):
                        break
                babe['ratedMovies']=listOfRatings
                #finding what each user has rated on similar movies
                thisUser=MyUser.objects.get(user=request.user)
                myUserRatings = Rating.objects.filter(user=thisUser)
                thisUserRatings =[]
                otherUserRatings = []
                for userRating in myUserRatings:
                    for otherRating in ratings:
                        if userRating.movie == otherRating.movie:
                            thisUserRatings.append(userRating.ratingValue)
                            otherUserRatings.append(otherRating.ratingValue)
                babe['similarity']=round(pearson(thisUserRatings,otherUserRatings)*10)
                return Response(babe)
            else:
                count =0
                for rating in ratings:
                    count=count+1
                    newser=RatingSerializer(instance=rating)
                    listOfRatings.append(newser.data)
                    if (count==5):
                        break
                babe['ratedMovies']=listOfRatings
                return Response(babe)


    def put(self,request,format=None):
        myuser=MyUser.objects.get(user=request.user)
        userGenres=Genre.objects.filter(user=myuser)
        for userGenre in userGenres:
            if userGenre.genre not in request.data['interests']:
                userGenre.user.remove(myuser)
        myuser.age=request.data['age']
        myuser.postCode=request.data['postCode']
        myuser.save()
        for genre in request.data['interests']:
            genres=Genre.objects.get(genre=genre)
            if myuser not in genres.user.all():
                genres.user.add(myuser)
        return Response({'data':"ok"},status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self,request, format=None):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            users = MyUser.objects.count()
            global userID
            userID=userID+users;
            theUser=form.save()
            newUser = MyUser(user=theUser, userID=userID)
            newUser.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = (BasicAuthentication,SessionAuthentication)
    serializer_class=UserSerializer
    def post(self,request, format=None):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request,user)
                patient = MyUser.objects.get(user=user)
                serializer = MyUserSerializer(instance=patient, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class LogOut(APIView):
    def get(self,request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)