"""
URL configuration del proyecto.

Convención elegida:
    Todas las rutas de la API viven bajo /api/.
    Cada app expone sus propias URLs en su urls.py, y acá las incluimos.

Rutas resultantes:
    /admin/
    /api/users/
    /api/resource-types/
    /api/resources/
    /api/reservations/
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # API
    path("api/", include("users.urls")),
    path("api/", include("resources.urls")),
    path("api/", include("reservations.urls")),
]
