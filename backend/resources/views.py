"""
Views de la app `resources`.

Para arrancar simple, en esta Etapa 3 exponemos solo listados.
El CRUD completo lo armamos después.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Resource, ResourceType
from .serializers import ResourceSerializer, ResourceTypeSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def resource_type_list(request):
    resource_types = ResourceType.objects.all().order_by("name")
    serializer = ResourceTypeSerializer(resource_types, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def resource_list(request):
    resources = (
        Resource.objects
        .filter(is_active=True)
        .select_related("resource_type")
        .order_by("name")
    )
    serializer = ResourceSerializer(resources, many=True)
    return Response(serializer.data)
