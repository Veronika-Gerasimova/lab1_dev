from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker
from django.urls import reverse
import json
from decimal import Decimal
from transportation.models import  Client, Flight, Ticket, Baggage, Airplane

# Create your tests here.
class ClientViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_get_list(self):
        client_instance = baker.make(Client, name="Иван Иванов", email="ivanov@mail.com", phone="123456789")
        response = self.client.get('/api/clients/')
        data = response.json()
        print(data)
        

        assert len(data) == 1
        assert client_instance.name == data[0]['name']
        assert client_instance.email == data[0]['email']
        assert client_instance.phone == data[0]['phone']
        
    def test_create_client(self):
        response = self.client.post('/api/clients/', {
            'name': 'Новый Клиент',
            'email': 'new@example.com',
            'phone': '987654321'
        })

        new_client_id = response.json()['id']
        
        clients = Client.objects.all()
        assert len(clients) == 1
        
        new_client = Client.objects.filter(id=new_client_id).first()
        assert new_client.name == 'Новый Клиент'
        assert new_client.email == 'new@example.com'
        assert new_client.phone == '987654321'
        
    def test_update_client(self):
        client_instance = baker.make(Client, name="Иван Иванов", email="ivanov@mail.com", phone="123456789")
        
        response = self.client.put(f'/api/clients/{client_instance.id}/', json.dumps({
            'name': 'Обновленный Клиент',
            'email': 'updated@example.com',
            'phone': '111111111'
        }), content_type='application/json')
        
        print(response.content)
        
        self.assertEqual(response.status_code, 200)
       
        updated_client = Client.objects.get(id=client_instance.id)
        self.assertEqual(updated_client.name, 'Обновленный Клиент')
        self.assertEqual(updated_client.email, 'updated@example.com')
        self.assertEqual(updated_client.phone, '111111111')

    def test_delete_client(self):
        client_instance = baker.make(Client, name="Иван Иванов", email="ivanov@mail.com", phone="123456789")
       
        response = self.client.delete(f'/api/clients/{client_instance.id}/')
        
        self.assertEqual(response.status_code, 204)
        
        clients = Client.objects.all()
        self.assertEqual(clients.count(), 0)
        
class FlightsViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        flight_instance = baker.make(Flight)
        
        r = self.client.get('/api/flights/')
        data = r.json()
        print(data)
        
        assert len(data) == 1
        assert flight_instance.flight_number == data[0]['flight_number']
        assert flight_instance.departure == data[0]['departure']
        assert flight_instance.destination == data[0]['destination']
    
    def test_create_flight(self):
        response = self.client.post('/api/flights/', {
            'flight_number': 'BA456',
            'departure': 'Лондон',
            'destination': 'Париж',
            'departure_time': '2024-12-12T09:00:00Z',
            'arrival_time': '2024-12-12T11:00:00Z'
        })

        new_flight_id = response.json()['id']
        flights = Flight.objects.all()
        assert len(flights) == 1

        new_flight = Flight.objects.filter(id=new_flight_id).first()
        assert new_flight.flight_number == 'BA456'
        assert new_flight.departure == 'Лондон'
        assert new_flight.destination == 'Париж'
    
    def test_update_flight(self):
        flight_instance = baker.make(Flight)
        
        response = self.client.put(f'/api/flights/{flight_instance.id}/', json.dumps({
            'flight_number': 'SU124',
            'departure': 'Москва',
            'destination': 'Санкт-Петербург',
            'departure_time': '2024-09-16T08:00:00Z',
            'arrival_time': '2024-09-16T10:00:00Z'
        }), content_type='application/json')
        
        print(response.content)
        
        self.assertEqual(response.status_code, 200)
        
        updated_flight = Flight.objects.get(id=flight_instance.id)
        self.assertEqual(updated_flight.flight_number, 'SU124')
        self.assertEqual(updated_flight.destination, 'Санкт-Петербург')

    def test_delete_flight(self):
        flight_instance = baker.make(Flight)
        
        response = self.client.delete(f'/api/flights/{flight_instance.id}/')

        self.assertEqual(response.status_code, 204)
        
        flights = Flight.objects.all()
        self.assertEqual(len(flights), 0)
      
class BaggagesViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        baggage_instance = baker.make(Baggage)
    
        r = self.client.get('/api/baggage/')
        self.assertEqual(r.status_code, 200)
    
        data = r.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(baggage_instance.baggage_type, data[0]['baggage_type'])
        
        self.assertEqual(f"{baggage_instance.weight:.2f}", f"{float(data[0]['weight']):.2f}") 
    
    def test_create_baggage(self):
        client_instance = Client.objects.create(name="Петр Петров", email="petrov@mail.com", phone="987654321")
        flight_instance = Flight.objects.create(
            flight_number="SU456",
            departure="Санкт-Петербург",
            destination="Казань",
            departure_time="2024-10-01T08:00:00Z",
            arrival_time="2024-10-01T10:00:00Z"
        )
        ticket_instance = Ticket.objects.create(client=client_instance, flight=flight_instance, seat_number="10B")
       
        response = self.client.post('/api/baggage/', {
            'ticket': ticket_instance.id,
            'weight': 25.0,
            'baggage_type': 'Сумка'
        })
        
        new_baggage_id = response.json()['id']
        baggages = Baggage.objects.all()
        self.assertEqual(len(baggages), 1)
        
        new_baggage = Baggage.objects.filter(id=new_baggage_id).first()
        self.assertEqual(new_baggage.weight, 25.0)
        self.assertEqual(new_baggage.baggage_type, 'Сумка')

    def test_update_baggage(self):
        client_instance = baker.make(Client)
        flight_instance = baker.make(Flight)
        ticket_instance = baker.make(Ticket, client=client_instance, flight=flight_instance)
        baggage_instance = baker.make(Baggage, ticket=ticket_instance, weight=20.0, baggage_type="Чемодан")
        
        response = self.client.put(f'/api/baggage/{baggage_instance.id}/', json.dumps({
            'ticket': ticket_instance.id,
            'weight': '23.50', 
            'baggage_type': 'Рюкзак'
        }), content_type='application/json')
       
        print(response.content)
        
        self.assertEqual(response.status_code, 200)
        
        updated_baggage = Baggage.objects.get(id=baggage_instance.id)
        self.assertEqual(updated_baggage.weight, Decimal('23.50'))
        self.assertEqual(updated_baggage.baggage_type, 'Рюкзак')

    def test_delete_baggage(self):
        baggage_instance = baker.make(Baggage)
        
        response = self.client.delete(f'/api/baggage/{baggage_instance.id}/')
        self.assertEqual(response.status_code, 204)
       
        baggages = Baggage.objects.all()
        self.assertEqual(len(baggages), 0)
            
class TicketsViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        ticket_instance = baker.make(Ticket)

        r = self.client.get('/api/tickets/')
        self.assertEqual(r.status_code, 200)
       
        data = r.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(ticket_instance.seat_number, data[0]['seat_number'])
        
        self.assertEqual(ticket_instance.client.id, data[0]['client_detail']['id'])
    
    def test_create_ticket(self):
        client_instance = Client.objects.create(
            name="Петр Петров", email="petrov@example.com", phone="987654321"
        )
        flight_instance = Flight.objects.create(
            flight_number="BA456", departure="Лондон", destination="Париж",
            departure_time="2024-12-12T09:00:00Z", arrival_time="2024-12-12T11:00:00Z"
        )
    
        response = self.client.post('/api/tickets/', {
            'client': client_instance.id,
            'flight': flight_instance.id,
            'seat_number': '15B'
        })

        print(response.data)  
        assert response.status_code == 201  

    def test_update_ticket(self):
        ticket_instance = baker.make(Ticket)
        
        response = self.client.put(f'/api/tickets/{ticket_instance.id}/', json.dumps({
            'client': ticket_instance.client.id,
            'flight': ticket_instance.flight.id,
            'seat_number': '14C'
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)  

        updated_ticket = Ticket.objects.get(id=ticket_instance.id)
        self.assertEqual(updated_ticket.seat_number, '14C')

    def test_delete_ticket(self):
        ticket_instance = baker.make(Ticket)

        response = self.client.delete(f'/api/tickets/{ticket_instance.id}/')

        self.assertEqual(response.status_code, 204) 

        tickets = Ticket.objects.filter(id=ticket_instance.id)
        self.assertEqual(len(tickets), 0)
      
class AirplanesViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        flight_instance = baker.make(Flight)
        airplane_instance = baker.make(Airplane, flight=flight_instance)
       
        r = self.client.get('/api/airplanes/')
        data = r.json()
        print(data)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(airplane_instance.tail_number, data[0]['tail_number'])
        self.assertEqual(airplane_instance.model, data[0]['model'])
        self.assertEqual(airplane_instance.capacity, data[0]['capacity'])
    
    def test_create_airplane(self):
        flight_instance = Flight.objects.create(
            flight_number="BA456", departure="Лондон", destination="Париж",
            departure_time="2024-12-12T09:00:00Z", arrival_time="2024-12-12T11:00:00Z"
        )
        
        response = self.client.post('/api/airplanes/', json.dumps({
            'tail_number': 'G-BOAC',
            'model': 'Concorde',
            'capacity': 120,
            'flight': flight_instance.id
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        
        data = response.json()
        self.assertEqual(data['tail_number'], 'G-BOAC')
        self.assertEqual(data['model'], 'Concorde')
        self.assertEqual(data['capacity'], 120)
        self.assertEqual(data['flight'], flight_instance.id)  

    def test_update_airplane(self):
        flight_instance = baker.make(Flight)
        airplane_instance = baker.make(Airplane, flight=flight_instance)

        updated_data = {
            'tail_number': 'UPDATED123',
            'model': 'Updated Model',
            'capacity': 150,
            'flight': flight_instance.id
        }

        response = self.client.put(
            f'/api/airplanes/{airplane_instance.id}/',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
       
        updated_airplane = Airplane.objects.get(id=airplane_instance.id)
        self.assertEqual(updated_airplane.tail_number, updated_data['tail_number'])
        self.assertEqual(updated_airplane.model, updated_data['model'])
        self.assertEqual(updated_airplane.capacity, updated_data['capacity'])

    def test_delete_airplane(self):
        flight_instance = baker.make(Flight)
        airplane_instance = baker.make(Airplane, flight=flight_instance)

        response = self.client.delete(f'/api/airplanes/{airplane_instance.id}/')
        self.assertEqual(response.status_code, 204)
        
        airplanes = Airplane.objects.all()
        self.assertEqual(len(airplanes), 0)    