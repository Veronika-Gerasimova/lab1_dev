<script setup>
import { ref,computed,  onBeforeMount } from 'vue';
import axios from 'axios';
import { inject } from 'vue';
const flights = ref([]);
const newFlight = ref({
  flight_number: '',
  departure: '',
  destination: '',
  departure_time: '',
  arrival_time: '',
});
const filters = ref({
  flight_number: '',
  departure: '',
  destination: ''
});

const uniqueFlightNumbers = computed(() => [...new Set(flights.value.map(f => f.flight_number))]);
const uniqueDepartures = computed(() => [...new Set(flights.value.map(f => f.departure))]);
const uniqueDestinations = computed(() => [...new Set(flights.value.map(f => f.destination))]);

const filteredFlights = computed(() => {
  return flights.value.filter(flight => {
    return (!filters.value.flight_number || flight.flight_number === filters.value.flight_number) &&
           (!filters.value.departure || flight.departure === filters.value.departure) &&
           (!filters.value.destination || flight.destination === filters.value.destination);
  });
});

const flightToEdit = ref({
  id: null,
  flight_number: '',
  departure: '',
  destination: '',
  departure_time: '',
  arrival_time: '',
});
const flightToRemove = ref(null); 
const showDeleteConfirmModal = ref(false); 
const showEditModal = ref(false);
const stats = ref({ count: 0, avg: 0, max: 0, min: 0 });
const otpVerified = inject('otpVerified');
const checkOtpStatus = inject('checkOtpStatus');

async function fetchFlightsStats() {
  try {
    const response = await axios.get("/api/flights/stats/");
    stats.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении статистики:", error);
  }
}

async function fetchFlights() {
  try {
    const response = await axios.get('/api/flights/');
    flights.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении рейсов:", error);
  }
}

async function addFlight() {
  await axios.post('/api/flights/', newFlight.value);
  newFlight.value = { flight_number: '', departure: '', destination: '', departure_time: '', arrival_time: '' };
  await fetchFlights();
}

async function removeFlight(id) {
  await axios.delete(`/api/flights/${id}/`);
  await fetchFlights();
}

// Открытие модального окна подтверждения удаления
function confirmRemoveFlight(flight) {
  flightToRemove.value = flight;
  showDeleteConfirmModal.value = true; // Открываем модальное окно
}

// Подтверждение удаления 
async function onRemoveConfirmed() {
  if (flightToRemove.value) {
    await removeFlight(flightToRemove.value.id); 
    showDeleteConfirmModal.value = false; 
    flightToRemove.value = null; 
  }
}

function openEditModal(flight) {
  console.log("OTP Verified:", otpVerified?.value); // Проверка статуса аутентификации
  if (!otpVerified || !otpVerified.value) {
    alert("Доступ запрещён. Выполните двойную аутентификацию.");
    return;
  }

  flightToEdit.value = { ...flight }; // Установка данных для редактирования
  showEditModal.value = true; // Установка видимости модального окна
  console.log("showEditModal:", showEditModal.value); // Логируем значение
}


// Обновление данных рейса
async function updateFlight() {
  if (!otpVerified || !otpVerified.value) {
    alert("Доступ запрещён. Выполните двойную аутентификацию.");
    return;
  }

  try {
    const formData = {
      flight_number: flightToEdit.value.flight_number,
      departure: flightToEdit.value.departure,
      destination: flightToEdit.value.destination,
      departure_time: flightToEdit.value.departure_time,
      arrival_time: flightToEdit.value.arrival_time
    };

    console.log("Form Data to update:", formData); // Логирование данных
    console.log("Flight ID:", flightToEdit.value.id); // Логирование ID рейса

    // Отправляем PUT запрос для обновления рейса
    await axios.put(`/api/flights/${flightToEdit.value.id}/`, formData);
    await fetchFlights(); // Обновляем список рейсов после сохранения
  } catch (error) {
    console.error("Ошибка при обновлении рейса:", error.response ? error.response.data : error);
  }

  showEditModal.value = false; // Закрытие модального окна после обновления
}

onBeforeMount(async () => {
  await fetchFlights();
  await fetchFlightsStats();
  await checkOtpStatus();
});
</script>

<template>
  <div class="container-fluid">
    <h1 class="my-4">Рейсы</h1>
    
    <form @submit.prevent="addFlight" class="mb-4">
      <div class="row g-3">
        <div class="col-md-2">
          <input type="text" class="form-control" v-model="newFlight.flight_number" placeholder="Номер рейса" required />
        </div>
        <div class="col-md-2">
          <input type="text" class="form-control" v-model="newFlight.departure" placeholder="Пункт отправления" required />
        </div>
        <div class="col-md-2">
          <input type="text" class="form-control" v-model="newFlight.destination" placeholder="Пункт назначения" required />
        </div>
        <div class="col-md-2">
          <input type="datetime-local" class="form-control" v-model="newFlight.departure_time" required />
        </div>
        <div class="col-md-2">
          <input type="datetime-local" class="form-control" v-model="newFlight.arrival_time" required />
        </div>
        <div class="col-auto d-flex align-items-end">
          <button class="btn btn-primary" type="submit">Добавить рейс</button>
        </div>
      </div>
    </form>

    <!-- Вывод статистики -->
    <div class="p-2">
            <h3>Статистика</h3>
            <ul>
              <li>Всего рейсов: {{ stats.count }}</li>
              <li>Средний ID: {{ stats.avg }}</li>
              <li>Максимальный ID: {{ stats.max }}</li>
              <li>Минимальный ID: {{ stats.min }}</li>
            </ul>
    </div>
    <div class="mb-3">
      <div class="row g-3">
        <div class="col-md-4">
          <label for="filter-seat" class="form-label">Номер рейса</label>
          <select v-model="filters.flight_number" class="form-select">
            <option value="">Все</option>
            <option v-for="number in uniqueFlightNumbers" :key="number" :value="number">
              {{ number }}
            </option>
          </select>
        </div>
        <div class="col-md-4">
          <label for="filter-seat" class="form-label">Пункт отправления</label>
          <select v-model="filters.departure" class="form-select">
            <option value="">Все</option>
            <option v-for="departure in uniqueDepartures" :key="departure" :value="departure">
              {{ departure }}
            </option>
          </select>
        </div>
        <div class="col-md-4">
          <label for="filter-seat" class="form-label">Пункт назначения</label>
          <select v-model="filters.destination" class="form-select">
            <option value="">Все</option>
            <option v-for="destination in uniqueDestinations" :key="destination" :value="destination">
              {{ destination }}
            </option>
          </select>
        </div>
      </div>
    </div>
    <div>
      <div v-for="flight in filteredFlights" :key="flight.id" class="flight-item mb-3 p-3 border rounded shadow-sm">
        <div class="col">
          <h5>{{ flight.flight_number }}</h5>
          <p>{{ flight.departure }} - {{ flight.destination }}</p>
          <p>Время отправления: {{ new Date(flight.departure_time).toLocaleString() }}</p>
          <p>Время прибытия: {{ new Date(flight.arrival_time).toLocaleString() }}</p>
        </div>  
        <button class="btn btn-success" @click="openEditModal(flight)">
          <i class="bi bi-pen-fill"></i>
        </button>
        <button class="btn btn-danger" @click="confirmRemoveFlight(flight)">
          <i class="bi bi-x"></i> 
        </button>
      </div>
    </div>

    <!-- Модальное окно для подтверждения удаления  -->
    <div v-if="showDeleteConfirmModal" class="modal fade show" tabindex="-1" style="display: block;" @click="showDeleteConfirmModal = false">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Подтверждение удаления</h5>
                <button type="button" class="btn-close" @click="showDeleteConfirmModal = false"></button>
              </div>
              <div class="modal-body">
                <p>Вы действительно хотите удалить рейс ?</p>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="showDeleteConfirmModal = false">Отмена</button>
                <button type="button" class="btn btn-danger" @click="onRemoveConfirmed">Удалить</button>
              </div>
            </div>
          </div>
        </div>

    <!-- Модальное окно для редактирования рейса -->
    <div v-if="showEditModal" class="modal fade show" tabindex="-1" style="display: block;">
      <div class="modal-dialog modal-lg"> 
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editFlightModalLabel">Редактировать рейс</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="row g-3">
                <div class="col-12">
                  <div class="form-floating">
                    <input type="text" class="form-control" id="editFlightNumber" v-model="flightToEdit.flight_number" required>
                    <label for="editFlightNumber">Номер рейса</label>
                  </div>
                </div>
                <div class="col-12">
                  <div class="form-floating">
                    <input type="text" class="form-control" id="editDeparture" v-model="flightToEdit.departure" required>
                    <label for="editDeparture">Пункт отправления</label>
                  </div>
                </div>
                <div class="col-12">
                  <div class="form-floating">
                    <input type="text" class="form-control" id="editDestination" v-model="flightToEdit.destination" required>
                    <label for="editDestination">Пункт назначения</label>
                  </div>
                </div>
                <div class="col-12">
                  <div class="form-floating">
                    <input type="datetime-local" class="form-control" id="editDepartureTime" v-model="flightToEdit.departure_time" required>
                    <label for="editDepartureTime">Время отправления</label>
                  </div>
                </div>
                <div class="col-12">
                  <div class="form-floating">
                    <input type="datetime-local" class="form-control" id="editArrivalTime" v-model="flightToEdit.arrival_time" required>
                    <label for="editArrivalTime">Время прибытия</label>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeEditModal">Закрыть</button>
            <button type="button" class="btn btn-primary" @click="updateFlight">Сохранить изменения</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.flight-item {
  padding: 0.5rem;
  border: 1px solid silver;
  margin: 1rem 0;
  box-shadow: 0 0 4px silver;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 16px;
  align-items: center;
}

</style>
