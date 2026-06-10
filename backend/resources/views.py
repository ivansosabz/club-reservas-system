from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Resource, ResourceType
from .serializers import ResourceSerializer, ResourceTypeSerializer


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def resource_type_list_create(request):
    if request.method == "GET":
        resource_types = ResourceType.objects.all().order_by("name")
        serializer = ResourceTypeSerializer(resource_types, many=True)
        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response(
            {"detail": "Autenticación requerida."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    serializer = ResourceTypeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([AllowAny])
def resource_type_detail(request, pk):
    resource_type = get_object_or_404(ResourceType, pk=pk)

    if request.method == "GET":
        serializer = ResourceTypeSerializer(resource_type)
        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response(
            {"detail": "Autenticación requerida."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "DELETE":
        try:
            resource_type.delete()
        except ProtectedError:
            return Response(
                {
                    "detail": (
                        "No se puede eliminar este tipo porque tiene "
                        "recursos asociados."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ResourceTypeSerializer(
        resource_type, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def resource_list_create(request):
    if request.method == "GET":
        resources = Resource.objects.filter(is_active=True)
        if request.query_params.get("todas") and request.user.is_authenticated:
            resources = Resource.objects.all()
        resources = resources.select_related("resource_type").order_by("name")
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response(
            {"detail": "Autenticación requerida."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    serializer = ResourceSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([AllowAny])
def resource_detail(request, pk):
    resource = get_object_or_404(
        Resource.objects.select_related("resource_type"), pk=pk
    )

    if request.method == "GET":
        serializer = ResourceSerializer(resource)
        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response(
            {"detail": "Autenticación requerida."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "DELETE":
        resource.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ResourceSerializer(
        resource, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
