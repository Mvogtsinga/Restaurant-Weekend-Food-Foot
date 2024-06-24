from django.contrib import admin
from .models import TableType, Reservation

class TableTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'seats', 'price', 'description')
    list_filter = ('name', 'seats')
    search_fields = ('name', 'description')
    ordering = ('name',)
    fields = ('name', 'seats', 'description', 'price', 'image_path')
    readonly_fields = ('price',)

    # Mettre le prix par défaut
    actions = ['set_default_price']

    def set_default_price(self, request, queryset):
        queryset.update(price=0.0)
    set_default_price.short_description = "Mettre le prix par défaut"

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'table_type', 'date', 'time', 'duration')
    list_filter = ('date', 'table_type')
    search_fields = ('user__username', 'table_type__name')
    raw_id_fields = ('user', 'table_type')
    ordering = ('-date', 'time')
    fields = ('user', 'table_type', 'date', 'time', 'duration')
    readonly_fields = ('date',)

    # Marquer comme réservé par défaut
    actions = ['mark_as_checked_in']

    def mark_as_checked_in(self, request, queryset):
        queryset.update(status='checked_in')
    mark_as_checked_in.short_description = "Marquer les réservations sélectionnées comme enregistrées"

admin.site.register(TableType, TableTypeAdmin)
admin.site.register(Reservation, ReservationAdmin)
