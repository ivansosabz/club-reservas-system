from django.contrib import admin
from .models import Reservation

# Register your models here.
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'resource',
        'start_datetime',
        'end_datetime',
        'status',
        'notes',
        'created_at',
        'updated_at'
    )
    list_filter = ('status', 'resource')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')