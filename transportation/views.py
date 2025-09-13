import base64
import logging
from typing import Any
from django.views.generic import TemplateView

from transportation.models import Client, Flight, Ticket, Baggage, Airplane

# Create your views here.
class ShowClientsView(TemplateView):
    template_name = "clients/show_clients.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.all()
       
        return context
      
class ShowFlightsView(TemplateView):
    template_name = "clients/show_flights.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['flights'] = Flight.objects.all()
        return context
 
class ShowBaggagesView(TemplateView):
    template_name = "clients/show_baggages.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['baggage'] = Baggage.objects.all()
        return context

class ShowTicketsView(TemplateView):
    template_name = "clients/show_tickets.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tickets'] = Ticket.objects.all()
        return context   
    
class ShowAirplanesView(TemplateView):
    template_name = "clients/show_airplanes.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['airplanes'] = Airplane.objects.all()
        return context     

