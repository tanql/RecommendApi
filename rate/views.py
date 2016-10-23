from django.shortcuts import render
from .serializers import MovieSerializer, RatingSerializer
from django.contrib.auth.models import User
from registration.models import MyUser
import numpy
import csv
from .models import Rating, Movie, Genre
from rest_framework import status
from csv import reader
from .disable import CsrfExemptSessionAuthentication
global dictionaryInit
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import pagination
from pyfm import pylibfm
from sklearn.feature_extraction import DictVectorizer
import numpy as np
import time


from rest_framework.authentication import BasicAuthentication


"""
def loadData(filename,path="data/"):
    data = []
    y = []
    users=set()
    items=set()
    with open(path+filename) as f:
        for line in f:
            (user,movieid,rating,ts)=line.split(',')
            data.append({ "user_id": str(user), "movie_id": str(movieid)})
            y.append(float(rating))
            users.add(user)
            items.add(movieid)

    return (data, np.array(y), users, items)

(train_data, y_train, train_users, train_items) = loadData("train.csv")
(test_data, y_test, test_users, test_items) = loadData("test.csv")
v = DictVectorizer()
X_train = v.fit_transform(train_data)
X_test = v.transform(test_data)

# Build and train a Factorization Machine
fm = pylibfm.FM(num_factors=10, num_iter=10, verbose=True, task="regression", initial_learning_rate=0.001, learning_rate_schedule="optimal")
fm.fit(X_train,y_train)
s=pickle.dumps(fm, -1)
"""
class CustomPaginator(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({'next': self.get_next_link(),
                         'previous': self.get_previous_link(),
                         'count': self.page.paginator.count,
                         'movies': data})



class RateView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, format=None):
        movielist = list(reversed(Movie.objects.all().order_by('year')))

        paginator = CustomPaginator()
        result_page = paginator.paginate_queryset(movielist, request)

        serializer = MovieSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    def post(self, request, format=None):
        user=MyUser.objects.get(user=request.user)
        movie = Movie.objects.get(movieId=request.POST['movieId'])
        rating = Rating(ratingValue=request.POST['ratingValue'], movie=movie, user=user)
        rating.save()

        with open('data/train.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow([user.userID,request.POST['movieId'],float(request.POST['ratingValue']), int(round(time.time(),0))])
        return Response(status=status.HTTP_200_OK)




class RecommendView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request, format=None):

        user=MyUser.objects.get(user=request.user)

        ratings = Rating.objects.filter(user=user)
        seenMovies = []
        for rating in ratings:
            seenMovies.append(rating.movie.movieId)

        if 'after' in request.GET:
            movies = Movie.objects.exclude(year__lt=request.GET.get('after')).exclude(movieId__in=seenMovies)
        elif 'before' in request.GET:
            movies = Movie.objects.exclude(year__gt=str(int(request.GET.get('before'))+1)).exclude(movieId__in=seenMovies)
        elif 'in' in request.GET:

            movies = Movie.objects.filter(year=request.GET.get('in')).exclude(movieId__in=seenMovies)
        elif 'filter' in request.GET:
            genre=Genre.objects.get(genre=request.GET.get('filter'))
            movies = Movie.objects.filter(movieGenre=genre).exclude(movieId__in=seenMovies)

        else:


            movies = Movie.objects.exclude(movieId__in=seenMovies)
        predictList=[]


        for movie in movies:
            predictList.append({'user_id':str(user.userID),'movie_id':str(movie.movieId)})
        v = DictVectorizer()



        predict=v.fit_transform(predictList)
        y=fm.predict(predict)

        for x in range(0,len(predictList)):
            predictList[x]['rating']=y[x]
            predictList[x]['movieName']=movies[x].movieName
            if predictList[x]['movie_id']=='121190':
                print movies[x].movieName

                print y[x]




        newlist = sorted(predictList, key=lambda k: k['rating'], reverse=True)



        paginator = CustomPaginator()
        result_page = paginator.paginate_queryset(newlist, request)


        return paginator.get_paginated_response(result_page)
    def post(self, request, format=None):
        user=MyUser.objects.get(user=request.user)

        ratings = Rating.objects.filter(user=user)
        seenMovies = []
        for rating in ratings:
            seenMovies.append(rating.movie.movieId)
        if 'year'in request.POST:
            print "yes"
            movies = Movie.objects.exclude(year__lt=request.POST['year']).exclude(movieId__in=seenMovies)


        predictList=[]

        for movie in movies:
            predictList.append({'user_id':str(user.userID),'movie_id':str(movie.movieId)})
            if movie.year<2000:
                print movie.movieName
        v = DictVectorizer()
        predict=v.fit_transform(predictList)
        y=fm.predict(predict)
        for x in range(0,len(predictList)):
            predictList[x]['rating']=y[x]
            predictList[x]['movieName']=movies[x].movieName



        newlist = sorted(predictList, key=lambda k: k['rating'], reverse=True)



        paginator = CustomPaginator()
        result_page = paginator.paginate_queryset(newlist, request)

        return paginator.get_paginated_response(result_page)




def getdata(request):
    global fm
    if Movie.objects.filter().count()>99999:
        def loadData(filename,path="data/"):
            data = []
            y = []
            users=set()
            items=set()
            with open(path+filename) as f:
                for line in f:
                    (user,movieid,rating,ts)=line.split(',')
                    data.append({ "user_id": str(user), "movie_id": str(movieid)})
                    y.append(float(rating))
                    users.add(user)
                    items.add(movieid)

            return (data, np.array(y), users, items)

        (train_data, y_train, train_users, train_items) = loadData("train.csv")
        (test_data, y_test, test_users, test_items) = loadData("test.csv")
        v = DictVectorizer()
        X_train = v.fit_transform(train_data)
        X_test = v.transform(test_data)

        # Build and train a Factorization Machine
        fm = pylibfm.FM(num_factors=10, num_iter=2, verbose=True, task="regression", initial_learning_rate=0.001, learning_rate_schedule="optimal")
        fm.fit(X_train,y_train)











        context={
            "text" : "Already uploaded"
        }
        return render(request, "getdata.html", context)
    else:
        movie_list=[]
        m = open('data/movies.csv', 'r')
        for line in reader(m):
            movie_list.extend(line)
        m.close

        for x in range(1,len(movie_list)):
            if x%3==1:
                s=movie_list[x]
                text = s[s.find("(")+1:s.find(")")]
                count=0
                while (text.isdigit()==False and count <15):
                    s=s[s.find(")")+1:]
                    text=s[s.find("(")+1:s.find(")")]
                    count = count +1


                if count == 15:
                    year=-1
                else:
                    year=int(text)
                movie = Movie(movieName=movie_list[x],movieId=movie_list[x-1], year=year)
                movie.save()
            elif x%3==0:
                for genre in movie_list[x-1].split('|'):
                    if genre != '(no genres listed)':
                        movie.movieGenre.add(Genre.objects.get(genre=genre))

        context={
            "text" : "Complete"
        }
        return render(request, "getdata.html", context)


