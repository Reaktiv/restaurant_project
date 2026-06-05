from django.contrib import admin
from reservations.models import Reservations, Table



@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'is_active')
    # search_fields = ('number', )
    list_filter = ('is_active', 'capacity')
    list_editable = ('is_active', )


@admin.register(Reservations)
class ReservationsAdmin(admin.ModelAdmin):
    list_display = ('customer', 'name', 'table', 'email', 'phone', 'date', 'time', 'number_of_guests', 'status', 'created_at')
    list_editable = ('status', 'table',)
    list_filter = ('status', 'date', 'table')
    # search_fields = ('customer__username', 'customer__email', 'special_requests')
    date_hierarchy = 'date'
    ordering = ('-created_at',)

