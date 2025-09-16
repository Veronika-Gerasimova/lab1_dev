from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from model_bakery import baker
from django.urls import reverse
import json
from decimal import Decimal
from transportation.models import  Client, Flight, Ticket, Baggage, Airplane
from django.contrib.auth.models import User
# Create your tests here.
# Декоратор отключает 2FA для всех тестов в этом классе
@override_settings(TWO_FACTOR_AUTH_ENABLED=False)
class ClientViewSetTestCase(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        # Создаем обычного пользователя
        self.user = User.objects.create_user(username='testuser', password='password123')
        # Аутентифицируем пользователя в тестовом клиенте
        self.client_api.force_authenticate(user=self.user)

    def test_get_list(self):
    # Создаем одного клиента и связываем его с тестовым пользователем
        client_instance = baker.make(
            Client,
            name="Иван Иванов",
            email="ivanov@mail.com",
            phone="123456789",
            user=self.user  
        )

        response = self.client_api.get('/api/clients/')
        data = response.json()

        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(client_instance.name, data[0]['name'])

    def test_create_client(self):
        payload = {
            "name": "Петр Петров",
            "email": "petrov@mail.com",
            "phone": "987654321"
        }
        response = self.client_api.post('/api/clients/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Client.objects.first().name, "Петр Петров")
        
    def test_update_client(self):
    # Создаем клиента, привязанного к тестовому пользователю
        client_instance = baker.make(
            Client,
            name="Иван Иванов",
            email="ivanov@mail.com",
            phone="123456789",
            user=self.user  # привязка к тестовому пользователю
        )
        
        # Делаем PUT-запрос через авторизованный клиент
        response = self.client_api.put(
            f'/api/clients/{client_instance.id}/',
            data=json.dumps({
                'name': 'Обновленный Клиент',
                'email': 'updated@example.com',
                'phone': '111111111'
            }),
            content_type='application/json'
        )
        
        print(response.content)
        
        self.assertEqual(response.status_code, 200)
        
        updated_client = Client.objects.get(id=client_instance.id)
        self.assertEqual(updated_client.name, 'Обновленный Клиент')
        self.assertEqual(updated_client.email, 'updated@example.com')
        self.assertEqual(updated_client.phone, '111111111')


    def test_delete_client(self):
        
        client_instance = baker.make(
            Client,
            name="Иван Иванов",
            email="ivanov@mail.com",
            phone="123456789",
            user=self.user
        )
        
        # Делаем DELETE-запрос через авторизованный клиент
        response = self.client_api.delete(f'/api/clients/{client_instance.id}/')
        
        self.assertEqual(response.status_code, 204)
        
        # Проверяем, что клиент удален
        clients = Client.objects.filter(user=self.user)
        self.assertEqual(clients.count(), 0)

@override_settings(TWO_FACTOR_AUTH_ENABLED=False)        
class FlightsViewSetTestCase(TestCase):
    def setUp(self):
            self.client_api = APIClient()
            # Создаем обычного пользователя
            self.user = User.objects.create_user(username='testuser', password='password123')
            # Аутентифицируем пользователя в тестовом клиенте
            self.client_api.force_authenticate(user=self.user)

    def test_get_list(self):
        flight_instance = baker.make(Flight, user=self.user)
        
        r = self.client_api.get('/api/flights/')
        data = r.json()
        print(data)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(flight_instance.flight_number, data[0]['flight_number'])
        self.assertEqual(str(flight_instance.departure), data[0]['departure'])
        self.assertEqual(str(flight_instance.destination), data[0]['destination'])
    
    def test_create_flight(self):
        response = self.client_api.post('/api/flights/', {
            'flight_number': 'BA456',
            'departure': 'Лондон',
            'destination': 'Париж',
            'departure_time': '2024-12-12T09:00:00Z',
            'arrival_time': '2024-12-12T11:00:00Z'
        })

        self.assertEqual(response.status_code, 201)  # Проверка успешного создания

        new_flight_id = response.json()['id']
        flights = Flight.objects.filter(user=self.user)
        self.assertEqual(len(flights), 1)

        new_flight = Flight.objects.get(id=new_flight_id)
        self.assertEqual(new_flight.flight_number, 'BA456')
        self.assertEqual(new_flight.departure, 'Лондон')
        self.assertEqual(new_flight.destination, 'Париж')

    def test_update_flight(self):
        flight_instance = baker.make(Flight, user=self.user)
        
        response = self.client_api.put(f'/api/flights/{flight_instance.id}/', json.dumps({
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
        flight_instance = baker.make(Flight, user=self.user)
        
        response = self.client_api.delete(f'/api/flights/{flight_instance.id}/')

        self.assertEqual(response.status_code, 204)
        
        flights = Flight.objects.filter(user=self.user)
        self.assertEqual(len(flights), 0)
      
@override_settings(TWO_FACTOR_AUTH_ENABLED=False)
class BaggagesViewSetTestCase(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='password123')
        # Аутентифицируем пользователя
        self.client_api.force_authenticate(user=self.user)

    def test_create_baggage(self):
        client_instance = baker.make(Client, user=self.user)
        flight_instance = baker.make(Flight, user=self.user)
        ticket_instance = baker.make(Ticket, client=client_instance, flight=flight_instance)
       
        response = self.client_api.post('/api/baggage/', {
            'ticket': ticket_instance.id,
            'weight': 25.0,
            'baggage_type': 'Сумка'
        })

        self.assertEqual(response.status_code, 201)

        new_baggage_id = response.json()['id']
        baggages = Baggage.objects.all()
        self.assertEqual(len(baggages), 1)
        
        new_baggage = Baggage.objects.get(id=new_baggage_id)
        self.assertEqual(new_baggage.weight, 25.0)
        self.assertEqual(new_baggage.baggage_type, 'Сумка')
            
@override_settings(TWO_FACTOR_AUTH_ENABLED=False)
class TicketsViewSetTestCase(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        # Создаем пользователя и аутентифицируем
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client_api.force_authenticate(user=self.user)

    def test_create_ticket(self):
        client_instance = Client.objects.create(name="Петр Петров", email="petrov@example.com", phone="987654321", user=self.user)
        flight_instance = Flight.objects.create(
            flight_number="BA456",
            departure="Лондон",
            destination="Париж",
            departure_time="2024-12-12T09:00:00Z",
            arrival_time="2024-12-12T11:00:00Z",
            user=self.user
        )

        response = self.client_api.post('/api/tickets/', {
            'client': client_instance.id,
            'flight': flight_instance.id,
            'seat_number': '15B'
        })

        self.assertEqual(response.status_code, 201)

        new_ticket_id = response.json()['id']
        tickets = Ticket.objects.filter(client__user=self.user)
        self.assertEqual(len(tickets), 1)

        new_ticket = Ticket.objects.get(id=new_ticket_id)
        self.assertEqual(new_ticket.seat_number, '15B')
        self.assertEqual(new_ticket.client, client_instance)
        self.assertEqual(new_ticket.flight, flight_instance)

@override_settings(TWO_FACTOR_AUTH_ENABLED=False)
class AirplanesViewSetTestCase(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        # Создаем пользователя и аутентифицируем
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client_api.force_authenticate(user=self.user)

    def test_create_airplane(self):
        flight_instance = Flight.objects.create(
            flight_number="BA456",
            departure="Лондон",
            destination="Париж",
            departure_time="2024-12-12T09:00:00Z",
            arrival_time="2024-12-12T11:00:00Z",
            user=self.user
        )

        response = self.client_api.post('/api/airplanes/', json.dumps({
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
