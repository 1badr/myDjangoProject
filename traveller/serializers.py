from ast import Not
from dataclasses import fields
from rest_framework import serializers
from traveller.models import *
from django.contrib.auth.models import AbstractUser,BaseUserManager
from .models import cityservices, Like
from .models import CustomUser
from django.db import transaction
from bson import ObjectId
from rest_framework import serializers
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

#from rest_framework import UserSerializer

@transaction.atomic
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # تشفير كلمة المرور
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password','is_superuser']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()  
        return user  
    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comment
        fields = ('__all__')

    


class cityservicesSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField()

    class Meta:
        model = cityservices
        fields = '__all__'



class cityservicesdeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = cityservices
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Like
        fields = ['id','user_id','service','servicelikes']

    def create(self, validated_data):
        user_id = validated_data['user_id']
        service = validated_data['service']
        servicelikes = validated_data['servicelikes']

        like = Like.objects.create(
            user=CustomUser.objects.get(id=user_id),
            service=service,
            servicelikes=servicelikes
        )
        return like
    

class cityserviceslikeSerializer(serializers.ModelSerializer):
     likes = serializers.SerializerMethodField()

     class Meta:
        model = cityservices
        fields = ['id', 'name','description','likes']

     def get_likes(self, obj):
        likes = Like.objects.filter(service=obj)
        if likes.exists():
            return LikeSerializer(likes, many=True).data
        else:
            return []



class DeleteCommentSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()



class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsofcity
        fields = '__all__'



class ChangePasswordSerializer(serializers.Serializer):
    

    id = serializers.IntegerField(required=True)
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        # Validate that the new passwords match
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("not equal")
        return data

    def save(self, **kwargs):
        # Get the user object based on the provided ID
        user = kwargs.get('user', None)
        if not user:
            raise serializers.ValidationError("no user")

        if user.id != self.validated_data['id']:
            raise serializers.ValidationError("toy are not auth")

        # Save the new password
        form = PasswordChangeForm(user, self.validated_data)
        if form.is_valid():
            form.save()
            return True
        return False
    

class PasswordResetSerializer(serializers.Serializer):
    

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("not exist")

        return value

    def save(self):
        form = PasswordResetForm(self.validated_data)
        if form.is_valid():
            form.save(request=None)
            return True
        return False
    


class AddCityServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = cityservices
        fields = '__all__'

    def create(self, validated_data):
       
        AddServices = cityservices.objects.create(
            nameservice=validated_data['nameservice'],
           # username=username,
            user_comment=validated_data['user_comment'],

            name_en=validated_data['name_en'],
            name_ar=validated_data['name_ar'],
            type=validated_data['type'],
            description=validated_data['description'],
            description_ar=validated_data['description_ar'],
            address=validated_data['address'],
            address_ar=validated_data['address_ar'],
            picture=validated_data['picture'],

        )
        return AddServices
    


class ServivceSerializer(serializers.ModelSerializer):
    class Meta:
        model = cityservices
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']