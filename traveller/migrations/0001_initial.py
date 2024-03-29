# Generated by Django 3.0.5 on 2023-07-27 15:50

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='cityservices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(blank=True, max_length=100)),
                ('name_ar', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(blank=True, choices=[('hotels', 'hotels'), ('Banks', 'Banks'), ('Coffee and Resturant', 'Coffee and Resturant'), ('Rent Car', 'Rent Car'), ('Historical Places', 'Historical Places'), ('Beach', 'Beach'), ('Malls', 'Malls'), ('Entertainment', 'Entertainment'), ('Category', 'Category')], max_length=100)),
                ('location', models.CharField(max_length=500)),
                ('email', models.EmailField(max_length=500)),
                ('num', models.IntegerField()),
                ('description', models.CharField(blank=True, max_length=500)),
                ('description_ar', models.CharField(blank=True, max_length=500)),
                ('picture', models.ImageField(max_length=500, null=True, upload_to='')),
                ('address', models.CharField(blank=True, max_length=100)),
                ('address_ar', models.CharField(blank=True, max_length=100)),
                ('like', models.IntegerField(default=0)),
                ('comment', models.TextField(blank=True, max_length=100)),
                ('name', models.CharField(max_length=100, null=True, verbose_name=django.contrib.auth.models.User)),
            ],
        ),
        migrations.CreateModel(
            name='Newsofcity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('title_ar', models.CharField(blank=True, max_length=100)),
                ('body', models.CharField(blank=True, max_length=500)),
                ('body_ar', models.CharField(blank=True, max_length=500)),
                ('date_publisher', models.DateTimeField(auto_now_add=True)),
                ('picture', models.ImageField(max_length=500, null=True, upload_to='')),
                ('user', models.CharField(max_length=100, null=True, verbose_name=django.contrib.auth.models.User)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=50, null=True)),
                ('username', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=12, null=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='customuser_set', related_query_name='user', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='customuser_set', related_query_name='user', to='auth.Permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user_comment', models.TextField()),
                ('nameservice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='traveller.cityservices')),
                ('username', models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servicelikes', models.IntegerField()),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='traveller.cityservices')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'service')},
            },
        ),
    ]
