from rest_framework import serializers
from transportation.models import Client, Ticket, Flight, Baggage, Airplane

class FlightSerializer(serializers.ModelSerializer):
    airplane = serializers.StringRelatedField()
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    class Meta:
        model = Flight
        fields = "__all__"

class ClientSerializer(serializers.ModelSerializer):
    tickets = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='ticket_set')
    baggage = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='ticket__baggage_set')
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user  
        return super().create(validated_data)
    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'phone', 'tickets', 'baggage', 'picture', "user"]


class TicketSerializer(serializers.ModelSerializer):
    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all(), write_only=True)
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), write_only=True)
    flight_detail = FlightSerializer(source='flight', read_only=True)
    client_detail = ClientSerializer(source='client', read_only=True)
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
   
    class Meta:
        model = Ticket
        fields = ['id', 'flight', 'client', 'seat_number', 'purchase_date', 'flight_detail', 'client_detail', "user"]

class BaggageSerializer(serializers.ModelSerializer):
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), write_only=True)
    ticket_detail = TicketSerializer(source='ticket', read_only=True)
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    class Meta:
        model = Baggage
        fields = ['id', 'ticket', 'weight', 'baggage_type', 'ticket_detail', "user"]
        

class AirplaneSerializer(serializers.ModelSerializer):
    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all())
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    class Meta:
        model = Airplane
        fields = "__all__"


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
