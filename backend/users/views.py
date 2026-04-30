"""
Views de la app `users`.

Por ahora solo un listado de usuarios, útil durante desarrollo para ver
qué usuarios existen (y sacar el id que manda el front como `user`
al crear una reserva — hasta que armemos auth en la Etapa 5).
"""

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer


@api_view(["GET"])
def user_list(request):
    """
    GET /api/users/   -> lista de usuarios registrados.
    """
    users = User.objects.all().order_by("username")
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
