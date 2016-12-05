from django.shortcuts import render
from .serializers import MovieSerializer, RatingSerializer
from registration.models import MyUser
import csv
from .models import Rating, Movie, Genre
from rest_framework import status
from csv import reader
from .disable import CsrfExemptSessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import pagination
from pyfm import pylibfm
from sklearn.feature_extraction import DictVectorizer
import numpy as np
import time
import math

from rest_framework.authentication import BasicAuthentication
def average(x):
    if len(x) > 0:
        return float(sum(x)) / len(x)
    else:
        return False
def pearson(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    if x == y:
        return 1
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0

    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y

        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff
    if math.sqrt(xdiff2 * ydiff2)==0:
        return 0
    else:
        return diffprod / math.sqrt(xdiff2 * ydiff2)

class CustomPaginator(pagination.PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({'next': self.get_next_link(),
                         'previous': self.get_previous_link(),
                         'count': self.page.paginator.count,
                         'movies': data})

class TimeCustomPaginator(pagination.PageNumberPagination):
    page_size=100;
    def get_paginated_response(self, data):
        return Response({'next': self.get_next_link(),
                         'previous': self.get_previous_link(),
                         'count': self.page.paginator.count,
                         'movies': data})


class MoviesView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request, format=None):
        user=MyUser.objects.get(userID=request.GET['user'])
        ratings = Rating.objects.filter(user=user).order_by('-ratingValue')

        serializer = RatingSerializer(instance=ratings, many=True)
        return Response(serializer.data)



class RateView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, format=None):
        user=MyUser.objects.get(user=request.user)

        if 'search' in request.GET:
            movie=[Movie.objects.get(movieName=request.GET['search'])]

            paginator = CustomPaginator()
            result_page = paginator.paginate_queryset(movie,request)
        else:

            seenMovies=[]
            ratings = Rating.objects.filter(user=user)
            for rating in ratings:
                seenMovies.append(rating.movie)
            movielist = list(reversed(Movie.objects.exclude().order_by('year')))
            for movie in movielist:
                if movie in seenMovies:
                    movielist.remove(movie)

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


        predict=v.transform(predictList)
        y=fm.predict(predict)

        for x in range(0,len(predictList)):
            predictList[x]['rating']=y[x]
            predictList[x]['movieName']=movies[x].movieName
            if predictList[x]['movie_id']=='121190':
                print movies[x].movieName

                print y[x]




        newlist = sorted(predictList, key=lambda k: k['rating'], reverse=True)

        if "time" in request.GET:
            paginator = TimeCustomPaginator()
            result_page = paginator.paginate_queryset(newlist, request)
        else:
            paginator = CustomPaginator()
            result_page = paginator.paginate_queryset(newlist, request)


        return paginator.get_paginated_response(result_page)





def getdata(request):
    global fm
    global v
    if Movie.objects.filter().count()>0:

        def loadData(filename,path="data/"):
            data = []
            y = []
            users=[]
            items=[]
            with open(path+filename) as f:
                for line in f:
                    (user,movieid,rating,ts)=line.split(',')
                    data.append({ "user_id": str(user), "movie_id": str(movieid)})
                    y.append(float(rating))
                    users.append(user)
                    items.append(movieid)

            return (data, np.array(y), users, items)

        (train_data, y_train, train_users, train_items) = loadData("train.csv")
        (test_data, y_test, test_users, test_items) = loadData("test.csv")

        #For testing accuracy of memory based filtering
        # ratingDictionary= {}
        # movieSets=[]
        # for x in range(0,len(train_data)):
        #     movieSets.append((str(train_data[x]['user_id']),str(train_data[x]['movie_id'])))
        #     if train_data[x]['user_id'] in ratingDictionary:
        #         ratingDictionary[train_data[x]['user_id']].append({train_data[x]['movie_id']:y_train[x]})
        #     else:
        #         ratingDictionary[train_data[x]['user_id']] = [{train_data[x]['movie_id']:y_train[x]}]
        #
        #
        #
        # countIndex=0;
        # predictions=[]
        # for user in test_users:
        #     userratings=[]
        #     similarusers= {}
        #     for userrating in ratingDictionary[user]:
        #         for key in userrating:
        #             userratings.append(userrating[key])
        #     for userTwo in ratingDictionary:
        #         if str(user) != userTwo and (userTwo,str(test_items[countIndex])) in movieSets:
        #             movieListOne= []
        #             movieListTwo=[]
        #             for rating in ratingDictionary[user]:
        #
        #                 for movieId in rating:
        #                     for ratingTwo in ratingDictionary[userTwo]:
        #                         for movieTwo in ratingTwo:
        #
        #                             if movieId == movieTwo:
        #                                 movieListOne.append(rating[movieId])
        #                                 movieListTwo.append(ratingTwo[movieTwo])
        #                                 continue
        #             if (len(movieListOne)>3):
        #                 similarity=pearson(movieListOne,movieListTwo)
        #
        #                 if similarity>0.6:
        #                     similarusers[userTwo]=similarity
        #                     similarusers[userTwo+'list']=movieListTwo
        #
        #
        #
        #
        #     teller = 0
        #     nevner = 0
        #     for simuser in similarusers:
        #         if isinstance(similarusers[simuser],int):
        #
        #             nevner = nevner + similarusers[simuser]
        #             for movie in ratingDictionary[simuser]:
        #                 if test_items[countIndex] in movie:
        #
        #                     teller=teller+similarusers[simuser]*(movie[test_items[countIndex]]-average(similarusers[simuser+'list']))
        #                     continue
        #     if nevner==0:
        #         predictions.append(average(userratings))
        #     else:
        #         predictions.append(average(userratings)+teller/nevner)
        #     print countIndex
        #     countIndex=countIndex+1;
        #     print countIndex


        v = DictVectorizer()
        X_train = v.fit_transform(train_data)
        X_test = v.transform(test_data)

        # Build and train a Factorization Machine
        fm = pylibfm.FM(num_factors=10, num_iter=100, verbose=True, task="regression", initial_learning_rate=0.001, learning_rate_schedule="optimal")
        fm.fit(X_train,y_train)
        predictions = fm.predict(X_test)
        from sklearn.metrics import mean_squared_error
        print("FM MSE: %.4f" % mean_squared_error(y_test,predictions))










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


