"""
Views de la app `reservations`.

Acá sí exponemos GET y POST (ListCreateAPIView) porque el front
necesita crear reservas desde el formulario "Nueva reserva".

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
from .serializers import ReservationSerializer


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
