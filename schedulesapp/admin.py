from django.contrib import admin
from .models import Schedule, ClientRegistration

# Admin display configuration for Schedule model
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'day', 'start_time', 'end_time', 'instructor', 'max_participants')
    list_filter = ('day',)  # Permet de filtrer par jour dans l'admin
    search_fields = ('name', 'instructor')  # Permet de rechercher par nom de cours ou d'instructeur
    ordering = ('day', 'start_time')  # Trie par jour et heure de début

# Enregistrement du modèle Schedule avec l'administration personnalisée

# Admin display configuration for ClientRegistration model
@admin.register(ClientRegistration)
class ClientRegistrationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'contact', 'schedule', 'payment_on_day', 'registration_date')
    list_filter = ('schedule__day', 'payment_on_day')  # Filters for schedule day and payment type
    search_fields = ('first_name', 'last_name', 'email', 'schedule__class_name')  # Search by client and class name
    ordering = ('-registration_date',)  # Order by registration date, descending
    readonly_fields = ('registration_date',)  # Make registration date read-only

