from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from reservations.models import Reservation
from resources.models import Resource, ResourceType


USERS = [
    {"username": "admin", "password": "test123", "is_staff": True},
    {"username": "juan", "password": "test123"},
    {"username": "maria", "password": "test123"},
    {"username": "carlos", "password": "test123"},
]

RESOURCE_TYPES = [
    {"name": "Cancha de tenis"},
    {"name": "Cancha de futbol"},
    {"name": "Salon de eventos"},
    {"name": "Piscina"},
    {"name": "Gimnasio"},
]

RESOURCES = [
    {"name": "Cancha de tenis 1", "type_name": "Cancha de tenis", "active": True},
    {"name": "Cancha de tenis 2", "type_name": "Cancha de tenis", "active": True},
    {"name": "Cancha de futbol 1", "type_name": "Cancha de futbol", "active": True},
    {"name": "Cancha de futbol 2", "type_name": "Cancha de futbol", "active": False},
    {"name": "Salon A", "type_name": "Salon de eventos", "active": True},
    {"name": "Salon B", "type_name": "Salon de eventos", "active": True},
    {"name": "Piscina climatizada", "type_name": "Piscina", "active": True},
    {"name": "Piscina descubierta", "type_name": "Piscina", "active": False},
    {"name": "Gimnasio principal", "type_name": "Gimnasio", "active": True},
    {"name": "Sala de spinning", "type_name": "Gimnasio", "active": True},
]


def _u(username):
    return User.objects.get(username=username)


def _r(name):
    return Resource.objects.get(name=name)


def _dt(*args):
    return timezone.make_aware(datetime(*args))


RESERVATIONS = [
    {"user": "admin", "resource": "Cancha de tenis 1", "start_dt": _dt(2026, 6, 10, 9, 0), "end_dt": _dt(2026, 6, 10, 10, 30), "status": "confirmed"},
    {"user": "juan", "resource": "Cancha de tenis 1", "start_dt": _dt(2026, 6, 10, 11, 0), "end_dt": _dt(2026, 6, 10, 12, 30), "status": "confirmed"},
    {"user": "maria", "resource": "Cancha de tenis 2", "start_dt": _dt(2026, 6, 10, 9, 0), "end_dt": _dt(2026, 6, 10, 10, 0), "status": "pending"},
    {"user": "carlos", "resource": "Cancha de futbol 1", "start_dt": _dt(2026, 6, 11, 14, 0), "end_dt": _dt(2026, 6, 11, 16, 0), "status": "confirmed"},
    {"user": "juan", "resource": "Cancha de futbol 1", "start_dt": _dt(2026, 6, 11, 16, 0), "end_dt": _dt(2026, 6, 11, 18, 0), "status": "pending"},
    {"user": "admin", "resource": "Salon A", "start_dt": _dt(2026, 6, 12, 8, 0), "end_dt": _dt(2026, 6, 12, 12, 0), "status": "confirmed"},
    {"user": "maria", "resource": "Salon A", "start_dt": _dt(2026, 6, 12, 13, 0), "end_dt": _dt(2026, 6, 12, 17, 0), "status": "cancelled"},
    {"user": "carlos", "resource": "Salon B", "start_dt": _dt(2026, 6, 13, 10, 0), "end_dt": _dt(2026, 6, 13, 12, 0), "status": "confirmed"},
    {"user": "juan", "resource": "Piscina climatizada", "start_dt": _dt(2026, 6, 14, 7, 0), "end_dt": _dt(2026, 6, 14, 9, 0), "status": "confirmed"},
    {"user": "maria", "resource": "Gimnasio principal", "start_dt": _dt(2026, 6, 14, 10, 0), "end_dt": _dt(2026, 6, 14, 11, 30), "status": "pending"},
    {"user": "carlos", "resource": "Gimnasio principal", "start_dt": _dt(2026, 6, 14, 14, 0), "end_dt": _dt(2026, 6, 14, 15, 30), "status": "confirmed"},
    {"user": "admin", "resource": "Sala de spinning", "start_dt": _dt(2026, 6, 15, 8, 0), "end_dt": _dt(2026, 6, 15, 9, 0), "status": "confirmed"},
    {"user": "juan", "resource": "Cancha de tenis 1", "start_dt": _dt(2026, 6, 15, 14, 0), "end_dt": _dt(2026, 6, 15, 15, 30), "status": "confirmed"},
    {"user": "maria", "resource": "Cancha de tenis 2", "start_dt": _dt(2026, 6, 16, 10, 0), "end_dt": _dt(2026, 6, 16, 11, 30), "status": "pending"},
    {"user": "carlos", "resource": "Salon A", "start_dt": _dt(2026, 6, 17, 9, 0), "end_dt": _dt(2026, 6, 17, 13, 0), "status": "confirmed"},
    {"user": "juan", "resource": "Piscina climatizada", "start_dt": _dt(2026, 6, 18, 6, 0), "end_dt": _dt(2026, 6, 18, 8, 0), "status": "confirmed"},
    {"user": "admin", "resource": "Cancha de futbol 1", "start_dt": _dt(2026, 6, 20, 10, 0), "end_dt": _dt(2026, 6, 20, 12, 0), "status": "confirmed"},
    {"user": "maria", "resource": "Cancha de futbol 1", "start_dt": _dt(2026, 6, 20, 12, 0), "end_dt": _dt(2026, 6, 20, 14, 0), "status": "pending"},
    {"user": "carlos", "resource": "Gimnasio principal", "start_dt": _dt(2026, 6, 21, 9, 0), "end_dt": _dt(2026, 6, 21, 10, 0), "status": "cancelled"},
    {"user": "admin", "resource": "Salon A", "start_dt": _dt(2026, 6, 22, 9, 0), "end_dt": _dt(2026, 6, 24, 18, 0), "status": "confirmed", "notes": "Conferencia de fin de semana"},
    {"user": "juan", "resource": "Salon B", "start_dt": _dt(2026, 6, 28, 10, 0), "end_dt": _dt(2026, 6, 30, 17, 0), "status": "pending", "notes": "Taller de capacitacion"},
    {"user": "maria", "resource": "Cancha de futbol 1", "start_dt": _dt(2026, 6, 25, 8, 0), "end_dt": _dt(2026, 6, 26, 20, 0), "status": "confirmed", "notes": "Torneo interno"},
]


class Command(BaseCommand):
    help = "Limpia y repuebla la base de datos con datos de prueba."

    def handle(self, *args, **options):
        self.stdout.write("Eliminando datos existentes...")
        Reservation.objects.all().delete()
        Resource.objects.all().delete()
        ResourceType.objects.all().delete()

        self.stdout.write("Creando tipos de recurso...")
        type_map = {}
        for rt in RESOURCE_TYPES:
            obj, _ = ResourceType.objects.get_or_create(
                name=rt["name"],
                defaults={"description": ""},
            )
            type_map[rt["name"]] = obj

        self.stdout.write("Creando recursos...")
        for r in RESOURCES:
            Resource.objects.get_or_create(
                name=r["name"],
                defaults={
                    "resource_type": type_map[r["type_name"]],
                    "is_active": r["active"],
                },
            )

        self.stdout.write("Creando usuarios...")
        for u in USERS:
            User.objects.get_or_create(
                username=u["username"],
                defaults={
                    "password": "pbkdf2_sha256$...",
                    "is_staff": u.get("is_staff", False),
                },
            )
            user = User.objects.get(username=u["username"])
            user.set_password(u["password"])
            user.is_staff = u.get("is_staff", False)
            user.save()

        self.stdout.write("Creando reservas...")
        for r in RESERVATIONS:
            Reservation.objects.create(
                user=_u(r["user"]),
                resource=_r(r["resource"]),
                start_datetime=r["start_dt"],
                end_datetime=r["end_dt"],
                status=r["status"],
                notes=r.get("notes", ""),
            )

        counts = {
            "usuarios": User.objects.count(),
            "tipos de recurso": ResourceType.objects.count(),
            "recursos": Resource.objects.count(),
            "reservas": Reservation.objects.count(),
        }
        self.stdout.write(self.style.SUCCESS("Datos creados correctamente:"))
        for label, count in counts.items():
            self.stdout.write(f"  {label}: {count}")
