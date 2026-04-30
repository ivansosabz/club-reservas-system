"""
Views de la app `resources`.

Para arrancar simple, en esta Etapa 3 exponemos solo listados.
El CRUD completo lo armamos después.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Resource, ResourceType
from .serializers import ResourceSerializer, ResourceTypeSerializer


@api_view(["GET"])
def resource_type_list(request):
    """
    GET /api/resource-types/
    Devuelve todos los tipos de recurso (cancha sintética, tenis, etc.).
    """
    resource_types = ResourceType.objects.all().order_by("name")
    serializer = ResourceTypeSerializer(resource_types, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def resource_list(request):
    """
    GET /api/resources/
    Devuelve todos los recursos activos.
    Filtramos `is_active=True` porque al front solo le interesa lo reservable.
    """
    resources = (
        Resource.objects
        .filter(is_active=True)
        .select_related("resource_type")    # evita queries extra
        .order_by("name")
    )
    serializer = ResourceSerializer(resources, many=True)
    return Response(serializer.data)
