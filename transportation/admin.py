from django.contrib import admin
from transportation.models import Client, Flight, Ticket, Baggage, Airplane

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ['flight_number', 'departure', 'destination', 'departure_time', 'arrival_time']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['client', 'flight', 'seat_number', 'purchase_date']
    list_filter = ['flight', 'purchase_date']
    search_fields = ['client__name', 'flight__flight_number']

@admin.register(Baggage)
class BaggageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'weight', 'baggage_type']
    list_filter = ['baggage_type']

@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ['tail_number', 'model', 'capacity', 'flight']
    search_fields = ['tail_number', 'model']