from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .models import MyUser
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, MyUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from rest_framework.authentication import SessionAuthentication, BasicAuthentication


userID = 945

class CurrentPatient(APIView):
    """
    View for details about currently logged in patient
    """

    def get(self, request, format=None):

        patient = User.objects.all().first()
        serializer = UserSerializer(instance=patient, context={'request': request})
        return Response(serializer.data)

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
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class=MyUserSerializer
    def post(self,request, format=None):

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                auth_login(request,user)
                patient = MyUser.objects.get(user=user)
                serializer = MyUserSerializer(instance=patient, context={'request': request})
                print(serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)






def login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect("/rate")
            else:
            # Return a 'disabled account' error message
                return HttpResponse("wrong")

        else:
            return HttpResponse("wrong")

    else:

        return render(request, "login.html")

def logout_view(request):
    logout(request)

    return render(request, "login.html")
    # Redirect to a success page.

class LogOut(APIView):
    def get(self,request, format=None):

        logout(request)



        return Response(status=status.HTTP_200_OK)