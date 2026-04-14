from django.db import models

# Create your models here.
from django.db import models

class ResourceTypes(models.Model):
    name =models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Resource(models.Model):
    name = models.CharField(max_length=100)
    resource_types = models.ForeignKey(
        ResourceTypes,
        on_delete=models.PROTECT, #si un tipo se esta usando no se eliminará
        related_name='resources',
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name