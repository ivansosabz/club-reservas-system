"""
URLs de la app `resources`.

El proyecto las incluye bajo el prefijo /api/ (ver config/urls.py),
así que las rutas finales quedan:

    /api/resource-types/
    /api/resources/
"""

from django.urls import path

from .views import resource_list, resource_type_list

urlpatterns = [
    path("resource-types/", resource_type_list, name="resource-type-list"),
    path("resources/", resource_list, name="resource-list"),
]
