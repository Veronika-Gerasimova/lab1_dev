from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from transportation.api import ClientViewSet, FlightViewSet, SecuredModelViewSet, TicketViewSet, BaggageViewSet, AirplaneViewSet, UserViewSet

from transportation import views 

router = DefaultRouter()
router.register("clients", ClientViewSet, basename="clients")
router.register("flights", FlightViewSet, basename="flights")
router.register("tickets", TicketViewSet, basename="tickets")
router.register("baggage", BaggageViewSet, basename="baggage")
router.register("airplanes", AirplaneViewSet, basename="airplanes")
router.register("user", UserViewSet, basename="user")
router.register("auth", SecuredModelViewSet, basename="auth") 

urlpatterns = [
    path('clients/', views.ShowClientsView.as_view(), name='show_clients'),
    path('flight/', views.ShowFlightsView.as_view(), name='show_flights'),
    path('ticket/', views.ShowTicketsView.as_view(), name='show_tickets'),
    path('baggage/', views.ShowBaggagesView.as_view(), name='show_baggages'),
    path('airplane/', views.ShowAirplanesView.as_view(), name='show_airplanes'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
