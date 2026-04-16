from django.contrib import admin
from .models import Resource, ResourceType
@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    #columnas que se ven en la lista
    list_display = ('name','description','created_at','updated_at')
    #barra de busqueda
    search_fields = ('name',)
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name','resource_type','description','is_active','created_at','updated_at')
    #filtros laterales
    list_filter = ('is_active','resource_type')
    search_fields = ('name','description')