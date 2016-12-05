from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from registration import views
from rate import views as rateview





router = routers.DefaultRouter()
urlpatterns = [
    # Examples:
    # url(r'^$', 'recommender.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/users/', views.CurrentPatient.as_view()),
    url(r'^api/login/', views.LoginView.as_view()),
    url(r'^api/register/', views.RegisterView.as_view()),
    url(r'^api/logout/', views.LogOut.as_view()),
    url(r'^api/rate/', rateview.RateView.as_view()),
    url(r'^api/movies/', rateview.MoviesView.as_view()),
    url(r'^api/recommend/', rateview.RecommendView.as_view()),
    url(r'^getdata/$','rate.views.getdata', name='getdata'),
    url(r'^api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    url(r'^', include(router.urls)),




]