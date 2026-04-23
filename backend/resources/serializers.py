"""
Serializers de la app `resources`.

Truco útil:
- En `ResourceSerializer` declaramos `resource_type_name` como campo
  derivado (source="resource_type.name"). Así el front recibe el nombre
  legible del tipo sin tener que hacer una segunda consulta.
- `resource_type` (el ID) se mantiene para poder crear/editar recursos.
"""

from rest_framework import serializers

from .models import Resource, ResourceType


class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = ["id", "name", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ResourceSerializer(serializers.ModelSerializer):
    # Campo "plano" para mostrar el nombre del tipo en el front.
    # read_only: no se usa para crear, solo se devuelve en GET.
    resource_type_name = serializers.CharField(
        source="resource_type.name",
        read_only=True,
    )

    class Meta:
        model = Resource
        fields = [
            "id",
            "name",
            "resource_type",        # ID — requerido al crear
            "resource_type_name",   # nombre — solo lectura
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
