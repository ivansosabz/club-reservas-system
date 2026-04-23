"""
URLs de la app `resources`.

El proyecto las incluye bajo el prefijo /api/ (ver config/urls.py),
así que las rutas finales quedan:

    /api/resource-types/
    /api/resources/
"""

from django.urls import path

from .views import ResourceListView, ResourceTypeListView

urlpatterns = [
    path("resource-types/", ResourceTypeListView.as_view(), name="resource-type-list"),
    path("resources/", ResourceListView.as_view(), name="resource-list"),
]
