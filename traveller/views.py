#مكاتب مطلوب اضافتها
from audioop import reverse
from email.headerregistry import Group
from io import BytesIO
from logging import raiseExceptions
from multiprocessing import AuthenticationError, context
import os
from tokenize import Name, group
from django.http import JsonResponse
from urllib import request, response
from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate,login,logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from .serializers import *
from django.shortcuts import get_object_or_404
from django.conf import settings
from .serializers import CustomUserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
import jwt ,datetime
from django.http import JsonResponse
from django.urls import reverse_lazy , reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.db.models.signals import post_save 
from django.dispatch import receiver 
from rest_framework.authtoken.models import Token
from .decorators import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework.authtoken.views import ObtainAuthToken
from .helpers import send_forget_password_mail
import uuid
from django.core.serializers import serialize
from rest_framework.decorators import api_view
from .models import cityservices, Like
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import cityservices, Like
from drf_yasg.utils import swagger_auto_schema
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from PIL import Image
from django.utils.text import slugify
from django.db.models import Count
from rest_framework import status
from django.contrib.auth.models import Group, User


#فنكشن  خاصة بانشاء توكن لكل مستخدم جديد
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        #اضافة كل مستخدم جديد اللي حقل ال'users'
        group = Group.objects.get(name='user')
        instance.groups.add(group)

#تسجيل مستخدم جديد بصيغة 'json'
class registerView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    

# عملية التحقق من تسجيل الدخول مع اعطاء المستخدم التوكن الخاص به
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id,'is_superuser':token.user.is_superuser,'is_staff':token.user.is_staff})


class UserView(APIView):
    def get (self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("unauthenticated")

        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        user = User.objects.filter(id =payload['id']).first()
        serializer =UserSerializer(user)
        return Response(serializer.data)

#الصفحة ماقبل صفحة ال'home' 
#واللي يكون فيها الاخبار 
@csrf_exempt
def pre_Home(request):
    #استدعاء كل الاخبار 
    news = Newsofcity.objects.all()

    #طلب حقول معينة من ماهو مطلوب من الداتابيز
    context = {
        'breakingnews':list(news.values('title_ar','body_ar','date_publisher','picture')),
    }
    return JsonResponse(context)


#الصفحة الخاصة بالتصنيفات    
@csrf_exempt
def Home (request):
    CategoryServices = cityservices.objects.filter(type='Category')

    context = {
    'CategoryServices':list(CategoryServices.values('id','name_ar','picture')),
    }
    return JsonResponse(context)


#الصفحة الخاصة بباقي الخدمات 
@csrf_exempt
def CityServices(request):
    services = {
        'hotels': 'hotels',
        'Coffee and Resturant': 'Coffee and Resturant',
        'Banks': 'Banks',
        'Rent Car': 'Rent Car',
        'Historical Places': 'Historical Places',
        'Malls': 'Malls',
        'Beach': 'Beach',
        'Entertainment': 'Entertainment',
    }

    context = {}
    for service_name, service_var in services.items():
        service = cityservices.objects.filter(type=service_name)
        comments = comment.objects.filter(nameservice__in=service)
        likes = Like.objects.filter(service__in=service).values('service').annotate(count=Count('id'))
        context[service_var] = {
            'services': list(service.values('id', 'name_en', 'picture', 'type','location','num','email')),
            'comments': list(comments.values('nameservice', 'user_comment', 'username__username')),
            'likes': list(likes.values('service','user','count')),
        }

    return JsonResponse(context)



def my_view(request):
    name = request.GET.get('name')
    image_name = name
    image_path = os.path.join(settings.MEDIA_ROOT, image_name)

    
    with open(image_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="image/jpeg")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(image_path)
        return response


@csrf_exempt
def CityServicesReviews(request, pk):
    
    eachservice = cityservices.objects.get(id=pk)
    comments_json = comment.objects.get(id=pk)

    # الحصول على التعليق الوحيد المرتبط بـ eachservice
    eachservice_json = serialize('json', [eachservice], fields=('name_en','comment','like'))
    comments_json = serialize('json', [comments_json], fields=('nameservice','user_comment','username'))

    context = {
        
        'eachservice': eachservice_json,
        'comments': comments_json,
    }
    return JsonResponse(context, safe=False)


#عملية تسجيل الخروج 
@csrf_exempt
def logoutUser(request):
    logout(request)
    context={'message':"usccess"}
    return JsonResponse(context)

#API  خاص بطلب معلومات عن الجو 
#@login_required(login_url='login')
@csrf_exempt
def get_weather_data(request):
    #الAPI  نفسه
    api_url = 'http://api.openweathermap.org./data/2.5/weather?appid=a06f4ed96f651355f8c175c0b8d9863b&q='
    #لان المطلوب مدينة واحدة فقط تم تعريفها 
    city = 'Mukalla'
    url = api_url + city
    response = requests.get(url)
    #طلب المعلومات على شكل json
    content = response.json()
    
    #المعلومات المطلوبة
    city_weather = {
        'city' : city,
        'temperature' : content['main']['temp'],
        'description' : content['weather'][0]['description'],
        'icon' : content['weather'][0]['icon']
    }
    return JsonResponse (city_weather)

#الصفحة الخاصة بالاعجابات 

@csrf_exempt
def user_liked_services(request,user_id):
    
    if not user_id:
        return JsonResponse({'error': 'User ID not provided'}, status=400)

    likes = Like.objects.filter(user=user_id)

    services_list = []

    for like in likes:
        try:
            service = like.service
            service_dict = {
                'user_id': user_id,
                'service_id': service.id,
                'name_ar': service.name_ar,
                'picture': service.picture.url if service.picture else None,
            }
            services_list.append(service_dict)
        except cityservices.DoesNotExist:
            pass

    return JsonResponse(services_list, status=200, safe=False)

#عملية اضافة لايك لاحد الخدمات المقدمة


@csrf_exempt
@api_view(['POST'])
def like_service(request):
    service_id = request.data.get('service_id')
    user_id = request.data.get('user_id')
    servicelikes = request.data.get('servicelikes')
    existing_like = Like.objects.filter(service_id=service_id, user_id=user_id, servicelikes=servicelikes).first()

    if existing_like:
        existing_like.delete()
        message = 'no like'
    else:
        like = Like.objects.create(service_id=service_id, user_id=user_id, servicelikes=servicelikes)
        message = 'like'

    likes = Like.objects.filter(service_id=service_id)
    serializer = LikeSerializer(likes, many=True)

    total_likes = Like.objects.filter(service_id=service_id).count()

    response_data = {
        'message': message,
        'likes': serializer.data,
        'total_likes': total_likes,
    }
    return Response(response_data)



@csrf_exempt
def search(request):
    request_data = json.loads(request.body.decode('utf-8'))
    name_ar = request_data.get('name_ar')
    if not name_ar:
        return JsonResponse({'error': 'no service with this name'}, status=status.HTTP_400_BAD_REQUEST)

    prefixes = name_ar.lower().split()
    services = cityservices.objects.all()

    for prefix in prefixes:
        services = services.filter(name_ar__istartswith=prefix)

    if services.exists():
        context = {
            'services': list(services.values('name_ar', 'picture')),
        }
        return JsonResponse(context, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message': 'nothing'}, status=status.HTTP_404_NOT_FOUND)



def add_comment(request):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
def User_delete_comment(request):
    comment_id = request.data.get('id')
    if not comment_id:
        return JsonResponse({'error': 'no comment in this id'}, status=status.HTTP_400_BAD_REQUEST)

    comments = comment.objects.filter(id=comment_id).last()
    if comments is not None:
        service_id = comments.nameservice.id
        comments.delete()
    
    data = {'status':'success'}
    return JsonResponse(data)


@csrf_exempt
def edit_service(request):
    id = request.data.get('id')
    if not id:
        return JsonResponse({'message': 'no id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        service = cityservices.objects.get(id=id)
    except cityservices.DoesNotExist:
        return JsonResponse({'message': 'no service'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = cityservicesSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer = cityservicesSerializer(service)
    return JsonResponse(serializer.data)




@csrf_exempt
def edit_services(request, id):
    try:
        service = cityservices.objects.get(id=id)
    except cityservices.DoesNotExist:
        return JsonResponse({'message': 'no service'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = cityservicesSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer = cityservicesSerializer(service)
    return JsonResponse(serializer.data)


def delete_city_service(request):
    try:
        city_service = cityservices.objects.get(id=request.data['id'])
    except cityservices.DoesNotExist:
        return Response({'error': 'no service'}, status=status.HTTP_404_NOT_FOUND)

    city_service.delete()
    return Response({'success': 'donneeee'}, status=status.HTTP_204_NO_CONTENT)



def delete_comment(request):
    comment_id = request.data.get('id')
    if not comment_id:
        return Response({'error': 'no id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        comment_obj = comment.objects.get(id=comment_id)
    except comment.DoesNotExist:
        return Response({'error': 'no comment'}, status=status.HTTP_404_NOT_FOUND)

    comment_obj.delete()
    return Response({'message': 'donnnne'}, status=status.HTTP_204_NO_CONTENT)



def add_news(request):
    serializer = NewsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def adding_service(request):
    serializer = ServivceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def update_news(request):
    news_id = request.data.get('id')
    if not news_id:
        return Response({'message': 'no id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        news = Newsofcity.objects.get(id=news_id)
    except Newsofcity.DoesNotExist:
        return Response({'message': 'no idd'}, status=status.HTTP_404_NOT_FOUND)

    serializer = NewsSerializer(news, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def delete_news(request):
    news_id = request.data.get('id')
    if not news_id:
        return Response({'message': 'no id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        news = Newsofcity.objects.get(id=news_id)
    except Newsofcity.DoesNotExist:
        return Response({'message': 'no id'}, status=status.HTTP_404_NOT_FOUND)

    news.delete()
    return Response({'message': 'donnnne'})



def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=request.user.username,
            password=serializer.validated_data['old password']
        )
        if user is not None:
            if serializer.save(user=user):
                return Response({"success": True, "message": "donnne"},status=status.HTTP_200_OK)
            else:
                return Response({"success": False,"message": "somthing wrong"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"success": False, "message": "the old pass is wrong"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



@csrf_exempt
def password_reset(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.save():
            return Response({"success": True,"message": "go check your email"}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "message":"sorry"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


def get_all_users(request):
    users = User.objects.all().values()
    return JsonResponse(list(users), safe=False)


@csrf_exempt
def delete_user(request):
    user_id = request.data.get('id')
    if not user_id:
        return Response({'message':'where is id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        User = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'message': 'there is no user'}, status=status.HTTP_404_NOT_FOUND)

    User.delete()
    return Response({'message': 'donnnneee'})


def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'message':'doonnnneee'})
    except User.DoesNotExist:
        return Response({'message': 'no user'}, status=404)
    

def user_staff(request):
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'message':'where is id'}, status=400)

    try:
        user = User.objects.get(id=user_id)
        staff_group = Group.objects.get(name='Staff')
        if user.is_staff:
            user.is_staff = False
            user.groups.remove(staff_group)
            user.save()
            return Response({'message':'now he is normal user'})
        else:
            user.is_staff = True
            user.groups.add(staff_group)
            user.save()
            return Response({'message':'now he is admin'})
    except User.DoesNotExist:
        return Response({'message':'no user'}, status=404)

