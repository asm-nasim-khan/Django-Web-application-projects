from django import urls
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('home',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    path('course_list',views.course_list,name='course_list'),
    path('search',views.search,name='search'),
    path('payment',views.payment,name='payment'),
    path('user',views.user,name='user')
]