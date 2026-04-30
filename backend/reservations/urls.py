"""
URLs de la app `reservations`.

Rutas (con el prefijo /api/):
    /api/reservations/        -> lista y creación
    /api/reservations/<id>/   -> detalle y edición parcial
"""

from django.urls import path

from .views import reservation_list_create, reservation_detail_update

urlpatterns = [
    path(
        "reservations/",
        reservation_list_create,
        name="reservation-list-create",
    ),
    path(
        "reservations/<int:pk>/",
        reservation_detail_update,
        name="reservation-detail-update",
    ),
]
