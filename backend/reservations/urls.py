"""
URLs de la app `reservations`.

Rutas (con el prefijo /api/):
    /api/reservations/        -> lista y creación
    /api/reservations/<id>/   -> detalle y edición parcial
"""

from django.urls import path

from .views import ReservationListCreateView, ReservationDetailUpdateView

urlpatterns = [
    path(
        "reservations/",
        ReservationListCreateView.as_view(),
        name="reservation-list-create",
    ),
    path(
        "reservations/<int:pk>/",
        ReservationDetailUpdateView.as_view(),
        name="reservation-detail-update",
    ),
]
