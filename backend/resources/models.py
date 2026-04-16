from django.db import models


class ResourceType(models.Model):
    """Tipo de recurso: cancha sintética, tenis, salón, etc."""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tipo de recurso"
        verbose_name_plural = "Tipos de recurso"

    def __str__(self):
        return self.name


class Resource(models.Model):
    """Recurso reservable del club: cancha 1, salón principal, etc."""
    name = models.CharField(max_length=100)
    resource_type = models.ForeignKey(   # ← singular, no "resource_types"
        ResourceType,
        on_delete=models.PROTECT,
        related_name='resources',
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Recurso"
        verbose_name_plural = "Recursos"

    def __str__(self):
        return self.name