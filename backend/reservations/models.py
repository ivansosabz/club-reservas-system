from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
        """Validaciones de negocio — se ejecutan antes de guardar."""

        # 1. end_time debe ser mayor que start_time
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError(
                    "La hora de fin debe ser posterior a la hora de inicio."
                )

        # 2. El recurso debe estar activo
        if self.resource and not self.resource.is_active:
            raise ValidationError(
                "Este recurso no está disponible para reservas."
            )

        # 3. Verificar solapamiento con reservas existentes
        self._check_overlap()

    def _check_overlap(self):
        """
        Detecta si existe otra reserva activa que se solape con este horario.
        Una reserva B solapa con A si:
            B.start_time < A.end_time  AND  B.end_time > A.start_time
        """
        overlapping = Reservation.objects.filter(
            resource=self.resource,
            date=self.date,
            status__in=['pending', 'confirmed'],
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        )

        # Excluir la reserva actual al editar (no conflicto consigo misma)
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError(
                f"Ya existe una reserva para este recurso en ese horario."
            )

    def save(self, *args, **kwargs):
        """Fuerza la validación antes de cada guardado."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.resource} — {self.date} {self.start_time}-{self.end_time}"