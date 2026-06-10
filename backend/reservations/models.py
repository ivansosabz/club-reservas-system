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
    date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
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
        ordering = ['date', 'start_time']

    def clean(self):
        if self.end_date is None:
            self.end_date = self.date

        if self.end_date < self.date:
            raise ValidationError(
                "La fecha de fin no puede ser anterior a la fecha de inicio."
            )

        if self.end_date == self.date and self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError(
                    "La hora de fin debe ser posterior a la hora de inicio."
                )

        if self.resource and not self.resource.is_active:
            raise ValidationError(
                "Este recurso no está disponible para reservas."
            )

        self._check_overlap()

    def _check_overlap(self):
        self_start = datetime.combine(self.date, self.start_time)
        self_end = datetime.combine(self.end_date, self.end_time)

        qs = Reservation.objects.filter(
            resource=self.resource,
            status__in=['pending', 'confirmed'],
        )
        if self.pk:
            qs = qs.exclude(pk=self.pk)

        for other in qs:
            other_start = datetime.combine(other.date, other.start_time)
            other_end = datetime.combine(other.end_date or other.date, other.end_time)
            if self_start < other_end and self_end > other_start:
                raise ValidationError(
                    "Ya existe una reserva para este recurso en ese horario."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.resource} — {self.date} {self.start_time}-{self.end_time}"