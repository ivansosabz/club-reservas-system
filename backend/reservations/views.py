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

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Reservation
from .serializers import ReservationSerializer, ReservationUpdateSerializer


@api_view(["GET", "POST"])
def reservation_list_create(request):
    """
    GET  /api/reservations/   -> lista de reservas
    POST /api/reservations/   -> crea una reserva
    """
    if request.method == "GET":
        # select_related reduce queries: en vez de N+1, hace un solo JOIN
        # por cada FK que vamos a mostrar (resource y user).
        reservations = Reservation.objects.select_related("resource", "user").all()
        # sin many=True, el serializer espera un solo objeto, no una lista.
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    else:  # POST
        serializer = ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
def reservation_detail_update(request, pk):
    """
    GET    /api/reservations/<id>/  -> detalle de una reserva
    PATCH  /api/reservations/<id>/  -> edición parcial (fecha, horario, status, notas)
    DELETE /api/reservations/<id>/  -> elimina una reserva
    """
    reservation = get_object_or_404(
        Reservation.objects.select_related("resource", "user"),
        pk=pk,
    )

    if request.method == "GET":
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    if request.method == "DELETE":
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ReservationUpdateSerializer(
        reservation,
        data=request.data,
        partial=True,
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
