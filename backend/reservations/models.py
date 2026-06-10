from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from resources.models import Resource


class Reservation(models.Model):

    STATUS_CHOICES = [
        ('pending',   'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservations',
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.PROTECT,
        related_name='reservations',
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['start_datetime']

    def clean(self):
        if self.start_datetime >= self.end_datetime:
            raise ValidationError(
                "La fecha/hora de fin debe ser posterior a la de inicio."
            )

        if self.resource and not self.resource.is_active:
            raise ValidationError(
                "Este recurso no está disponible para reservas."
            )

        self._check_overlap()

    def _check_overlap(self):
        qs = Reservation.objects.filter(
            resource=self.resource,
            status__in=['pending', 'confirmed'],
        )
        if self.pk:
            qs = qs.exclude(pk=self.pk)

        for other in qs:
            if self.start_datetime < other.end_datetime and self.end_datetime > other.start_datetime:
                raise ValidationError(
                    f"Conflicto con la reserva de {other.user.username} "
                    f"({other.start_datetime.strftime('%d/%m %H:%M')} - "
                    f"{other.end_datetime.strftime('%d/%m %H:%M')})"
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.resource} — "
            f"{self.start_datetime.strftime('%d/%m %H:%M')}-"
            f"{self.end_datetime.strftime('%d/%m %H:%M')}"
        )
