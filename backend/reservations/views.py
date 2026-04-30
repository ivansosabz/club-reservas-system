"""
Views de la app `reservations`.

Flujo de un POST:
    1. El front manda JSON a /api/reservations/
    2. DRF lo pasa al serializer — si falta algún campo responde 400.
    3. Si el serializer valida, llama a `serializer.save()`.
    4. `save()` del modelo ejecuta `full_clean()` (ver reservations/models.py)
       que chequea: end > start, recurso activo, y NO solape.
    5. Si alguna validación falla, el error se devuelve al front como 400.
"""

from rest_framework import generics

from .models import Reservation
from .serializers import ReservationSerializer, ReservationUpdateSerializer


class ReservationListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/reservations/   -> lista de reservas
    POST /api/reservations/   -> crea una reserva
    """
    serializer_class = ReservationSerializer

    def get_queryset(self):
        # select_related reduce queries: en vez de N+1, hace un solo JOIN
        # por cada FK que vamos a mostrar (resource y user).
        return (
            Reservation.objects
            .select_related("resource", "user")
            .all()
        )


class ReservationDetailUpdateView(generics.RetrieveUpdateAPIView):
    """
    GET   /api/reservations/<id>/  -> detalle de una reserva
    PATCH /api/reservations/<id>/  -> edición parcial (fecha, horario, status, notas)

    PUT no está habilitado — usamos PATCH para ediciones parciales.
    Para cancelar: PATCH con {"status": "cancelled"}.
    """
    http_method_names = ["get", "patch"]  # deshabilitamos PUT explícitamente

    def get_queryset(self):
        return (
            Reservation.objects
            .select_related("resource", "user")
            .all()
        )

    def get_serializer_class(self):
        # GET usa el serializer completo (incluye user y resource como IDs)
        # PATCH usa el restringido (user y resource no se pueden cambiar)
        if self.request.method == "PATCH":
            return ReservationUpdateSerializer
        return ReservationSerializer
