from django.db import models
from pickle import TRUE
from random import choices
from django.db import migrations, models
from django.contrib.auth.models import User 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = email.lower()        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=12, null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['name', 'name']

    # Add related_name arguments to avoid clashes with built-in User model
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )

    def __str__(self):
        return self.name

class Newsofcity(models.Model):
    title = models.CharField(max_length=100,blank=True)
    title_ar = models.CharField(max_length=100,blank=True)
    body = models.CharField(max_length=500, blank=True)
    body_ar = models.CharField(max_length=500, blank=True)
    date_publisher=models.DateTimeField(auto_now_add=True ,blank=True)
    picture = models.ImageField(max_length=500,null=True)
    user=models.CharField(User,null=True,max_length=100)

    def __str__(self):
         return self.title


class cityservices(models.Model):
    type = (
        ('hotels','hotels'),
        ('Banks','Banks'),
        ('Coffee and Resturant','Coffee and Resturant'),
        ('Rent Car','Rent Car'),
        ('Historical Places','Historical Places'),
        ('Beach','Beach'),
        ('Malls','Malls'),
        ('Entertainment','Entertainment'),
        ('Category','Category'),

    )
    name_en = models.CharField(max_length=100,blank=True)
    name_ar = models.CharField(max_length=100,null=True,blank=True)
    type=models.CharField(blank=True,max_length=100,choices=type)
    location = models.CharField(max_length=500,null=True)
    email = models.EmailField(max_length=500,null=True)
    num = models.IntegerField(null=True)
    description = models.CharField(max_length=500,blank=True)
    description_ar = models.CharField(max_length=500,blank=True)
    picture = models.ImageField(max_length=500,blank=True)
    address = models.CharField(max_length=100,blank=True)
    address_ar = models.CharField(max_length=100,blank=True)
    like=models.IntegerField(default=0)
    comment=models.TextField(blank=True,max_length=100)
    name=models.CharField(User,null=True,max_length=100)

    def save(self, *args, **kwargs):
        if self.picture and self.picture.is_empty():
            self.picture = None
        super().save(*args, **kwargs)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    service = models.ForeignKey(cityservices, on_delete=models.CASCADE, related_name='likes')
    servicelikes = models.IntegerField()


    class Meta:
        unique_together = ('user', 'service')


    def __str__(self):
        return 'Like : {} by {}'.format(self.service_id, self.user)



class comment(models.Model):
    nameservice = models.ForeignKey(cityservices, related_name='comments', on_delete=models.CASCADE)
    username = models.ForeignKey(User,max_length=100, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user_comment = models.TextField()

    def __str__(self):
        return 'Comment : {} by {}'.format(self.user_comment, self.username)

    
