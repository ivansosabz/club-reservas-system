"""
URLs de la app `users`.

Ruta final (con el prefijo /api/):
    /api/users/
"""

from django.urls import path

from .views import user_list

urlpatterns = [
    path("users/", user_list, name="user-list"),
]
