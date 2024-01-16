from multiprocessing.spawn import import_main_path
from django.urls import URLPattern, path
from django.contrib.auth.views import PasswordResetView

from django.contrib.auth import views as auth_views
from . import views
from django.urls import re_path as url
from django.urls import path,include,re_path
from django.urls import path

from .views import *
from rest_framework.authtoken import views

urlpatterns = [
path('register/',registerView.as_view(),name='register'),
path('login/',CustomObtainAuthToken.as_view(), name='CustomObtainAuthToken'),
path('pre_Home/',pre_Home, name='pre_Home'),
path('Home/',Home,name='Home'),
#path('fav/', user_liked_services, name='fav'),
path('fav/<int:user_id>/', user_liked_services, name='fav'),

path('user_liked_services/', user_liked_services, name='user_liked_services'),

path('weather/',get_weather_data,name='weather'),
path('CityServices/',CityServices, name='CityServices'),
path('CityServicesReviews/<int:pk>/',CityServicesReviews, name='CityServices'),
path('like/',like_service,name='like'),

path('add_comment/', add_comment),

#path('add_comment/', add_comment),
path('logout/',logoutUser, name='logout'),
path('user/',UserView.as_view(), name='user'),
path('search/',search,name='searched'),
path('usercomments_delete/', User_delete_comment),
#path('admin/add_service/',add_service,name='add_service'),
path('add_service/',adding_service,name='add_service'),

path('admin/edit_service/',edit_service,name='edit_service'),

#path('admin/edit_service/<int:id>/',edit_services,name='edit_services'),



path('admin/delete_service/',delete_city_service,name='edit_service'),
path('admin/deletecomment/', delete_comment),
path('add_news/',add_news, name='add_news'),
path('update_news/',update_news, name='update_news'),
path('delete_news/',delete_news, name='delete_news'),
path('my_view/',my_view, name='CityServices'),
path('change_password/',change_password, name='change_password'),
path('password_reset/',password_reset, name='password_reset'),

path('getall/',get_all_users, name='getall'),
path('delete_user/<int:user_id>',delete_user, name='delete_user'),
path('convert_to_staff',convert_to_staff, name='convert_to_staff'),

path('user_staff',user_staff, name='user_staff'),






]