"""
Views de la app `resources`.

Usamos las "generic views" de DRF — clases prefabricadas que ya saben
hacer operaciones típicas sobre un modelo. Cada clase elige qué verbos
HTTP acepta:

    ListAPIView        -> GET (lista)
    CreateAPIView      -> POST
    ListCreateAPIView  -> GET + POST  (la que usamos casi siempre)
    RetrieveAPIView    -> GET por id
    UpdateAPIView      -> PUT/PATCH
    DestroyAPIView     -> DELETE
    RetrieveUpdateDestroyAPIView -> GET/PUT/PATCH/DELETE por id

Para arrancar simple, en esta Etapa 3 exponemos solo listado.
El CRUD completo lo armamos después (ViewSets o agregando más generics).
"""

from rest_framework import generics

from .models import Resource, ResourceType
from .serializers import ResourceSerializer, ResourceTypeSerializer


class ResourceTypeListView(generics.ListAPIView):
    """
    GET /api/resource-types/
    Devuelve todos los tipos de recurso (cancha sintética, tenis, etc.).
    """
    queryset = ResourceType.objects.all().order_by("name")
    serializer_class = ResourceTypeSerializer


class ResourceListView(generics.ListAPIView):
    """
    GET /api/resources/
    Devuelve todos los recursos activos.
    Filtramos `is_active=True` porque al front solo le interesa lo reservable.
    """
    serializer_class = ResourceSerializer

    def get_queryset(self):
        # `get_queryset()` se ejecuta en cada request — ideal si
        # querés filtrar por querystring más adelante
        # (ej: ?type=1 para traer solo canchas).
        return (
            Resource.objects
            .filter(is_active=True)
            .select_related("resource_type")    # evita queries extra
            .order_by("name")
        )
