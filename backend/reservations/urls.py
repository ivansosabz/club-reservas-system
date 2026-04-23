"""
URLs de la app `reservations`.

Ruta final (con el prefijo /api/):
    /api/reservations/
"""

from django.urls import path

from .views import ReservationListCreateView

urlpatterns = [
    path(
        "reservations/",
        ReservationListCreateView.as_view(),
        name="reservation-list-create",
    ),
]
