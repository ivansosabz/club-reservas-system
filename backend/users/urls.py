"""
URLs de la app `users`.

Ruta final (con el prefijo /api/):
    /api/users/
"""

from django.urls import path

from .views import UserListView

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
]
