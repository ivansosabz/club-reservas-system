from django.contrib import admin

# Register your models here.
from django.contrib import admin
from resources.models import Resource, ResourceTypes

admin.site.register(Resource)
admin.site.register(ResourceTypes)
