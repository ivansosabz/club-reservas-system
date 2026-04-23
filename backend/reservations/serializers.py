"""
Serializer de la app `reservations`.

Notas importantes:
- El modelo `Reservation` ya tiene validaciones en `clean()` (end > start,
  recurso activo, no solape). Django las ejecuta dentro de `save()` porque
  llamamos a `full_clean()`. DRF las respeta: si un `clean()` falla con
  ValidationError, el serializer responde 400 con el mensaje.
- `user` es requerido por el modelo. Mientras no tengamos auth (Etapa 5),
  el front tiene que mandar el id del usuario. Cuando agreguemos auth,
  vamos a hacer `user = request.user` en la view y sacarlo del payload.
- `resource_name` y `user_username` son campos "de apoyo" para el front,
  así la lista de reservas se muestra sin lookups extra.
"""

from rest_framework import serializers

from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    # Campos derivados — solo lectura, para que el front pinte la UI.
    resource_name = serializers.CharField(source="resource.name", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",             # ID del usuario (requerido al crear)
            "user_username",    # solo lectura
            "resource",         # ID del recurso (requerido al crear)
            "resource_name",    # solo lectura
            "date",
            "start_time",
            "end_time",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
