<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';

const flights = ref([]);
const stats = ref({ count: 0, avg: 0, max: 0, min: 0 });
const filters = ref({
  flight_number: '',
  departure: '',
  destination: '',
});

const mostPopularDestination = computed(() => {
  if (!flights.value.length) return null;

  // Подсчет количества рейсов для каждого направления
  const destinationCount = flights.value.reduce((acc, flight) => {
    acc[flight.destination] = (acc[flight.destination] || 0) + 1;
    return acc;
  }, {});

  // Поиск направления с максимальным количеством рейсов
  const [mostPopular] = Object.entries(destinationCount).reduce(
    (max, curr) => (curr[1] > max[1] ? curr : max),
    ['', 0] 
  );

  return mostPopular;
});

const filteredFlights = computed(() => {
  return flights.value.filter(flight => {
    return (
      (filters.value.flight_number ? flight.flight_number.includes(filters.value.flight_number) : true) &&
      (filters.value.departure ? flight.departure.includes(filters.value.departure) : true) &&
      (filters.value.destination ? flight.destination.includes(filters.value.destination) : true)
    );
  });
});

async function fetchFlightsStats() {
  try {
    const response = await axios.get("/api/flights/stats/");
    stats.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении статистики:", error);
  }
}

async function fetchFlights() {
  const response = await axios.get('/api/flights/');
  flights.value = response.data;
}

onBeforeMount(async () => {
  await fetchFlights();
  await fetchFlightsStats();
});
</script>

<template>
    <div class="container-fluid">
    <div class="hero-section text-center py-5">
      <h1 class="display-4 text-white mb-3">Планирование путешествий и покупка билетов🛫</h1>
      <p class="lead text-white mb-4">Быстрый поиск рейсов и актуальная информация в реальном времени</p>
      <div class="row mb-5">
        <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="popular-card shadow-lg p-4 text-center">
            <h5 class="text-uppercase text-light">Самый популярный пункт назначения</h5>
            <p class="popular-destination text-white display-5 fw-bold">
              {{ mostPopularDestination || 'Нет данных' }}
            </p>
          </div>
        </div>
      </div>

      <div class="filters mt-4">
        <input 
          v-model="filters.departure" 
          class="form-control search-input" 
          type="text" 
          placeholder="Пункт отправления"
        />
        <input 
          v-model="filters.destination" 
          class="form-control search-input" 
          type="text" 
          placeholder="Пункт назначения"
        />
      </div>
    </div></div>
      <div class="row mb-5">
        <div class="col-md-4">
          <div class="card shadow-lg p-4 text-center">
            <h5>Всего рейсов</h5>
            <p class="fs-2 text-info">{{ stats.count }}</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-lg p-4 text-center">
            <h5>Средний ID рейса</h5>
            <p class="fs-2 text-warning">{{ stats.avg }}</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card shadow-lg p-4 text-center">
            <h5>Максимальный ID</h5>
            <p class="fs-2 text-danger">{{ stats.max }}</p>
          </div>
        </div>
      </div>
      <div class="mb-5">
      <img 
        src="C:\Users\geras\Desktop\web\самолет2.jpg" 
        alt="Карта рейсов" 
        class="img-fluid"
      />
    </div>
      <div class="row mb-5">
        <div class="col-12">
          <h3 class="text-center mb-4">Доступные рейсы</h3>
          <div class="list-group">
            <div
              v-if="filteredFlights.length > 0"
              v-for="flight in filteredFlights"
              :key="flight.id"
              class="list-group-item d-flex justify-content-between align-items-center shadow mb-3"
            >
              <div>
                <h5 class="text-dark">{{ flight.flight_number }}</h5>
                <p class="mb-1 text-secondary">{{ flight.departure }} - {{ flight.destination }}</p>
                <p class="mb-0">Отправление: <span class="fw-bold">{{ new Date(flight.departure_time).toLocaleString() }}</span></p>
                <p>Прибытие: <span class="fw-bold">{{ new Date(flight.arrival_time).toLocaleString() }}</span></p>
              </div>
              <div>
                <router-link :to="'/flights'" class="btn btn-outline-info">
                  Подробнее
                </router-link>
              </div>
            </div>
            <!-- Если рейсов нет -->
            <div v-else class="d-flex justify-content-center align-items-center py-5">
              <div class="not-found-card shadow-lg p-4 text-center">
                <h5 class="text-uppercase text-muted">Рейсы не найдены</h5>
                <p class="text-secondary">Попробуйте изменить параметры поиска</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

<style scoped>
.hero-section {
  background: linear-gradient(45deg, #4a90e2, #50e3c2);
  color: white;
  padding: 100px 0;
  border-bottom: 1px solid #ddd;
}

.search-bar, .filters {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.search-input {
  max-width: 600px;
  margin: 0 auto;
  padding: 10px;
  font-size: 1.2rem;
}

.map-container {
  width: 100%;
  height: 400px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  margin-bottom: 20px;
}

.card {
  border-radius: 8px;
}

.list-group-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-radius: 8px;
  background-color: #f8f9fa;
}

button.btn-info {
  background-color: #4a90e2;
  color: white;
}
.img-fluid {
  width: 100%;
  height: 60%;
}
.not-found-card {
  background-color: #f8f9fa; 
  border-radius: 8px;      
  max-width: 600px;        
  margin: 0 auto;          
  color: #6c757d;          
}
</style>
