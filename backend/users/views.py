"""
Views de la app `users`.

Por ahora solo un listado de usuarios, útil durante desarrollo para ver
qué usuarios existen (y sacar el id que manda el front como `user`
al crear una reserva — hasta que armemos auth en la Etapa 5).
"""

from django.contrib.auth.models import User
from rest_framework import generics

from .serializers import UserSerializer


class UserListView(generics.ListAPIView):
    """
    GET /api/users/   -> lista de usuarios registrados.
    """
    queryset = User.objects.all().order_by("username")
    serializer_class = UserSerializer
