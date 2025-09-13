from django.core.management.base import BaseCommand
from faker import Faker
from transportation.models import Client, Flight, Ticket, Baggage, Airplane
import random
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        
        # Генерация данных для клиентов (Client)
        clients = []
        for _ in range(1000):  # Генерируем 1000 записей
            client = Client.objects.create(
                name=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                picture=None,  # Для простоты пропускаем изображения
                user=random.choice(users)  # Присваиваем случайного пользователя
            )
            clients.append(client)

        # Генерация данных для рейсов (Flight)
        flights = []
        for _ in range(100):  # Генерируем 100 рейсов
            flight = Flight.objects.create(
                flight_number=f"FL-{fake.unique.random_number(digits=5)}",
                departure=fake.city(),
                destination=fake.city(),
                departure_time=fake.date_time_this_year(),
                arrival_time=fake.date_time_this_year()
            )
            flights.append(flight)

        # Генерация данных для самолетов (Airplane)
        airplanes = []
        for _ in range(50):  # Генерируем 50 самолетов
            airplane = Airplane.objects.create(
                tail_number=f"TN-{fake.unique.random_number(digits=6)}",
                model=fake.word(),
                capacity=random.randint(50, 300),
                flight=random.choice(flights),
                picture=None  # Пропускаем изображения
            )
            airplanes.append(airplane)

        # Генерация данных для билетов (Ticket)
        tickets = []
        for _ in range(1000):  # Генерируем 1000 билетов
            ticket = Ticket.objects.create(
                client=random.choice(clients),
                flight=random.choice(flights),
                seat_number=f"{random.randint(1, 50)}A",
                purchase_date=fake.date_time_this_year()
            )
            tickets.append(ticket)

        # Генерация данных для багажа (Baggage)
        baggage_types = ["Ручная кладь", "Чемодан", "Спортинвентарь", "Музыкальный инструмент", "Сумка", "Рюкзак", "Спортивная сумка"]
        baggages = []
        for _ in range(100):  # Генерируем 100 багажей
            baggage = Baggage.objects.create(
            ticket=random.choice(tickets),
            weight=round(random.uniform(5.0, 30.0), 2),
            baggage_type=random.choice(baggage_types)  # Выбираем тип из заданного списка
        )
        baggages.append(baggage)
        
        self.stdout.write(self.style.SUCCESS('Данные сгенерированы!'))
