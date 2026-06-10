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
"""
quiero que empezemos de nuevo este proyecto y que lo hagamos bien desde el inicio para que cualquier usuario pueda registrarse, iniciar sesion y que pueda 
registrar nombres de personas con los que va hacer los turnos rotativos tal cual como lo hace este sistema con mi tio y con mi padre para cuidarle a 
abuela, quiero que me sugieras cambios pero no quiero que te divagues en cada por favor, ademas dame una guia cortta de donde empezar para entender bien 
este proyecto
"""