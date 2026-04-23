"""
Serializers de la app `users`.

Un Serializer en DRF es el puente entre el modelo (Python) y JSON.
- Cuando el front hace GET, el serializer convierte modelo -> JSON.
- Cuando el front hace POST/PUT, convierte JSON -> modelo y valida.

Para la Etapa 3 solo exponemos lectura de usuarios (no registro aún,
eso viene en la Etapa 5 con autenticación).
"""

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Perfil extendido del usuario — solo teléfono por ahora."""

    class Meta:
        model = UserProfile
        fields = ["id", "phone", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    """
    Representación pública del usuario.
    Ojo: NO exponemos password (nunca se devuelve al front).
    Incluimos `profile` anidado como solo-lectura para que el front
    pueda mostrar el teléfono sin hacer una segunda llamada.
    """

    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "profile"]
        read_only_fields = ["id"]
