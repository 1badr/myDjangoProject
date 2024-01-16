from django.contrib import admin
from django.contrib import admin
from . models import *
#@admin.register(news)
class userAdmin(admin.ModelAdmin):
    list_display: ('name')
admin.site.register(Newsofcity)
admin.site.register(Like)
admin.site.register(comment)
admin.site.register(cityservices)

