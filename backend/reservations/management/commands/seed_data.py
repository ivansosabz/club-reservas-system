from datetime import date, time

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

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


RESERVATIONS = [
    {"user": "admin", "resource": "Cancha de tenis 1", "date": date(2026, 6, 10), "start": time(9, 0), "end": time(10, 30), "status": "confirmed"},
    {"user": "juan", "resource": "Cancha de tenis 1", "date": date(2026, 6, 10), "start": time(11, 0), "end": time(12, 30), "status": "confirmed"},
    {"user": "maria", "resource": "Cancha de tenis 2", "date": date(2026, 6, 10), "start": time(9, 0), "end": time(10, 0), "status": "pending"},
    {"user": "carlos", "resource": "Cancha de futbol 1", "date": date(2026, 6, 11), "start": time(14, 0), "end": time(16, 0), "status": "confirmed"},
    {"user": "juan", "resource": "Cancha de futbol 1", "date": date(2026, 6, 11), "start": time(16, 0), "end": time(18, 0), "status": "pending"},
    {"user": "admin", "resource": "Salon A", "date": date(2026, 6, 12), "start": time(8, 0), "end": time(12, 0), "status": "confirmed"},
    {"user": "maria", "resource": "Salon A", "date": date(2026, 6, 12), "start": time(13, 0), "end": time(17, 0), "status": "cancelled"},
    {"user": "carlos", "resource": "Salon B", "date": date(2026, 6, 13), "start": time(10, 0), "end": time(12, 0), "status": "confirmed"},
    {"user": "juan", "resource": "Piscina climatizada", "date": date(2026, 6, 14), "start": time(7, 0), "end": time(9, 0), "status": "confirmed"},
    {"user": "maria", "resource": "Gimnasio principal", "date": date(2026, 6, 14), "start": time(10, 0), "end": time(11, 30), "status": "pending"},
    {"user": "carlos", "resource": "Gimnasio principal", "date": date(2026, 6, 14), "start": time(14, 0), "end": time(15, 30), "status": "confirmed"},
    {"user": "admin", "resource": "Sala de spinning", "date": date(2026, 6, 15), "start": time(8, 0), "end": time(9, 0), "status": "confirmed"},
    {"user": "juan", "resource": "Cancha de tenis 1", "date": date(2026, 6, 15), "start": time(14, 0), "end": time(15, 30), "status": "confirmed"},
    {"user": "maria", "resource": "Cancha de tenis 2", "date": date(2026, 6, 16), "start": time(10, 0), "end": time(11, 30), "status": "pending"},
    {"user": "carlos", "resource": "Salon A", "date": date(2026, 6, 17), "start": time(9, 0), "end": time(13, 0), "status": "confirmed"},
    {"user": "juan", "resource": "Piscina climatizada", "date": date(2026, 6, 18), "start": time(6, 0), "end": time(8, 0), "status": "confirmed"},
    {"user": "admin", "resource": "Cancha de futbol 1", "date": date(2026, 6, 20), "start": time(10, 0), "end": time(12, 0), "status": "confirmed"},
    {"user": "maria", "resource": "Cancha de futbol 1", "date": date(2026, 6, 20), "start": time(12, 0), "end": time(14, 0), "status": "pending"},
    {"user": "carlos", "resource": "Gimnasio principal", "date": date(2026, 6, 21), "start": time(9, 0), "end": time(10, 0), "status": "cancelled"},
    # Multi-day reservations
    {"user": "admin", "resource": "Salon A", "date": date(2026, 6, 22), "end_date": date(2026, 6, 24), "start": time(9, 0), "end": time(18, 0), "status": "confirmed", "notes": "Conferencia de fin de semana"},
    {"user": "juan", "resource": "Salon B", "date": date(2026, 6, 28), "end_date": date(2026, 6, 30), "start": time(10, 0), "end": time(17, 0), "status": "pending", "notes": "Taller de capacitacion"},
    {"user": "maria", "resource": "Cancha de futbol 1", "date": date(2026, 6, 25), "end_date": date(2026, 6, 26), "start": time(8, 0), "end": time(20, 0), "status": "confirmed", "notes": "Torneo interno"},
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
            end = r.get("end_date", r["date"])
            Reservation.objects.create(
                user=_u(r["user"]),
                resource=_r(r["resource"]),
                date=r["date"],
                end_date=end,
                start_time=r["start"],
                end_time=r["end"],
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
