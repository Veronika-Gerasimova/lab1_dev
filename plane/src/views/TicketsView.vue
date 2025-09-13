<script setup>
import { computed, onBeforeMount, ref , inject} from 'vue';
import axios from 'axios';

const tickets = ref([]);  // Массив для билетов
const clients = ref([]);  // Массив для клиентов
const flights = ref([]);  // Массив для рейсов
const newTicket = ref({
  client: null,  // Связанный клиент
  flight: null,  // Связанный рейс
  seat_number: '',
  purchase_date: ''  // Дата покупки (можно оставить пустым, будет задана автоматически)
});
const ticketToEdit = ref({});
const ticketToRemove = ref(null); 
const showDeleteConfirmModal = ref(false); 
const otpVerified = inject('otpVerified');
const checkOtpStatus = inject('checkOtpStatus');

const filters = ref({
  client: '',
  flight: '',
  seat_number: '',
  purchase_date: '',
});
const uniqueClients = computed(() => {
  return [...new Set(tickets.value.map(ticket => ticket.client_detail.name))];
});

const uniqueFlights = computed(() => {
  return [...new Set(tickets.value.map(ticket => ticket.flight_detail.flight_number))];
});

const uniqueSeatNumbers = computed(() => {
  return [...new Set(tickets.value.map(ticket => ticket.seat_number))];
});

const uniquePurchaseDates = computed(() => {
  return [...new Set(tickets.value.map(ticket => ticket.purchase_date))];
});

const filteredTickets = computed(() => {
  return tickets.value.filter(ticket => {
    return (
      (!filters.value.client || ticket.client_detail.name === filters.value.client) &&
      (!filters.value.flight || ticket.flight_detail.flight_number === filters.value.flight) &&
      (!filters.value.seat_number || ticket.seat_number === filters.value.seat_number) &&
      (!filters.value.purchase_date || ticket.purchase_date === filters.value.purchase_date)
    );
  });
});

const stats = ref({ count: 0, avg: 0, max: 0, min: 0 });

async function fetchTicketsStats() {
  try {
    const response = await axios.get("/api/tickets/stats/");
    stats.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении статистики:", error);
  }
}

// Получение всех клиентов
async function fetchClients() {
  const r = await axios.get("/api/clients/");
  clients.value = r.data;
}

// Получение всех рейсов
async function fetchFlights() {
  const r = await axios.get("/api/flights/");
  flights.value = r.data;
}
function onUpdateTicketAndClose() {
  onUpdateTicket();  // Обновление билета
  showModal.value = false;  // Закрытие модального окна
}

// Получение всех билетов
async function fetchTickets() {
  const r = await axios.get("/api/tickets/");
  console.log(r.data); // Логируем данные
  tickets.value = r.data;  
}

// Добавление нового билета
async function addTicket() {
  await axios.post('/api/tickets/', newTicket.value);
  newTicket.value = { client: null, flight: null, seat_number: '', purchase_date: '' };
  await fetchTickets();
}

// Удаление билета
async function removeTicket(id) {
  try {
    await axios.delete(`/api/tickets/${id}/`);
    await fetchTickets();
  } catch (error) {
    console.error("Ошибка при удалении билета:", error);
  }
}

// Открытие модального окна подтверждения удаления
function confirmRemoveTicket(ticket) {
  ticketToRemove.value = ticket;
  showDeleteConfirmModal.value = true; // Открываем модальное окно
}

// Подтверждение удаления 
async function onRemoveConfirmed() {
  if (ticketToRemove.value) {
    await removeTicket(ticketToRemove.value.id); 
    showDeleteConfirmModal.value = false; 
    ticketToRemove.value = null; 
  }
}
const showModal = ref(false); // Состояние для открытия/закрытия модального окна

function onTicketEditClick(ticket) {
  // Проверка статуса двухфакторной аутентификации
  if (!otpVerified || !otpVerified.value) {
    alert("Доступ запрещён. Выполните двойную аутентификацию.");
    return;
  }
  
  // Присваиваем данные билета в переменную для редактирования
  ticketToEdit.value = {
    id: ticket.id,  
    client: ticket.client_detail.id, 
    flight: ticket.flight_detail.id,  
    seat_number: ticket.seat_number
  };

  // Меняем состояние, чтобы открыть модальное окно
  showModal.value = true;
}


async function onUpdateTicket() {
  if (!otpVerified || !otpVerified.value) {
    alert("Доступ запрещён. Выполните двойную аутентификацию.");
    return;
  }
  try {
    console.log("Обновляем билет с ID:", ticketToEdit.value.id);  
    const updateData = {
      client: ticketToEdit.value.client,
      flight: ticketToEdit.value.flight,
      seat_number: ticketToEdit.value.seat_number
    };
    await axios.put(`/api/tickets/${ticketToEdit.value.id}/`, updateData);
    await fetchTickets();
  } catch (error) {
    console.error("Ошибка при обновлении билета:", error.response ? error.response.data : error.message);
  }
}
onBeforeMount(async () => {
  await fetchClients();
  await fetchFlights();
  await fetchTickets();
  await fetchTicketsStats();
  await checkOtpStatus();
});

</script>

<template>
  <div class="container-fluid">
    <h1 class="my-4">Билеты</h1>
    <form @submit.prevent="addTicket" class="mb-4">
      <div class="row">
        <div class="col">
          <select class="form-select" v-model="newTicket.client" required>
            <option selected disabled>Выберите клиента</option>
            <option v-for="client in clients" :key="client.id" :value="client.id">
              {{ client.name }} ({{ client.email }})
            </option>
          </select>
        </div>
        <div class="col">
          <select class="form-select" v-model="newTicket.flight" required>
            <option disabled>Выберите рейс</option>
            <option v-for="flight in flights" :key="flight.id" :value="flight.id">
              {{ flight.flight_number }}: {{ flight.departure }} -> {{ flight.destination }}
            </option>
          </select>
        </div>
        <div class="col">
          <input type="text" class="form-control" v-model="newTicket.seat_number" placeholder="Номер места" required />
        </div>
        <div class="col-auto">
          <button class="btn btn-primary" type="submit">Добавить билет</button>
        </div>
      </div>
    </form>
  
    <!-- Вывод статистики -->
    <div class="p-2">
        <h3>Статистика</h3>
        <ul>
          <li>Всего билетов: {{ stats.count }}</li>
          <li>Средний ID: {{ stats.avg }}</li>
          <li>Максимальный ID: {{ stats.max }}</li>
          <li>Минимальный ID: {{ stats.min }}</li>
        </ul>
    </div>
    <div class="row mb-4">
      <div class="col">
        <label for="filter-client" class="form-label">Клиент</label>
        <select id="filter-client" class="form-select" v-model="filters.client">
          <option value="">Все</option>
          <option v-for="client in uniqueClients" :key="client" :value="client">
            {{ client }}
          </option>
        </select>
      </div>
      <div class="col">
        <label for="filter-flight" class="form-label">Рейс</label>
        <select id="filter-flight" class="form-select" v-model="filters.flight">
          <option value="">Все</option>
          <option v-for="flight in uniqueFlights" :key="flight" :value="flight">
            {{ flight }}
          </option>
        </select>
      </div>
      <div class="col">
        <label for="filter-seat" class="form-label">Номер места</label>
        <select id="filter-seat" class="form-select" v-model="filters.seat_number">
          <option value="">Все</option>
          <option v-for="seat in uniqueSeatNumbers" :key="seat" :value="seat">
            {{ seat }}
          </option>
        </select>
      </div>
      <div class="col">
        <label for="filter-date" class="form-label">Дата покупки</label>
        <select id="filter-date" class="form-select" v-model="filters.purchase_date">
          <option value="">Все</option>
          <option v-for="date in uniquePurchaseDates" :key="date" :value="date">
            {{ new Date(date).toLocaleDateString() }}
          </option>
        </select>
      </div>
    </div>
    <!-- Отображение списка билетов -->
    <div>
      <div v-for="ticket in filteredTickets" :key="ticket.id" class="ticket-item mb-3 p-3 border rounded shadow-sm d-flex justify-content-between align-items-center">
        <div class="ticket-details">
          <h5 class="ticket-title">Билет на рейс: {{ ticket.flight_detail.flight_number }}</h5>
          <p class="ticket-client">
            <strong>Клиент:</strong> {{ ticket.client_detail.name }} ({{ ticket.client_detail.email }})
          </p>
          <p class="ticket-seat">
            <strong>Номер места:</strong> {{ ticket.seat_number }}
          </p>
          <p class="ticket-date">
            <strong>Дата покупки:</strong> {{ new Date(ticket.purchase_date).toLocaleString() }}
          </p>
        </div>
        <div class="ticket-actions">
          <button class="btn btn-success" @click="onTicketEditClick(ticket)">
            <i class="bi bi-pen-fill"></i>
          </button>
          <button class="btn btn-danger" @click="confirmRemoveTicket(ticket)">
            <i class="bi bi-x"></i> 
          </button>
        </div>
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
                <p>Вы действительно хотите удалить билет ?</p>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="showDeleteConfirmModal = false">Отмена</button>
                <button type="button" class="btn btn-danger" @click="onRemoveConfirmed">Удалить</button>
              </div>
            </div>
          </div>
        </div>
    
    <!-- Модальное окно для редактирования билета -->
<div v-if="showModal" class="modal fade show" id="editTicketModal" tabindex="-1" aria-labelledby="editTicketModalLabel" aria-hidden="true" style="display: block;">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="editTicketModalLabel">Редактировать билет</h1>
        <button type="button" class="btn-close" @click="showModal = false"></button>
      </div>
      <div class="modal-body">
        <div class="row g-3">
          <div class="col-12">
            <div class="form-floating">
              <input type="text" class="form-control" id="editSeatNumber" v-model="ticketToEdit.seat_number" required />
              <label for="editSeatNumber">Номер места</label>
            </div>
          </div>
          <div class="col-12">
            <div class="form-floating">
              <select class="form-select" v-model="ticketToEdit.client" required>
                <option value="" disabled>Выберите клиента</option>
                <option v-for="client in clients" :key="client.id" :value="client.id">
                  {{ client.name }} ({{ client.email }})
                </option>
              </select>
              <label for="editClientSelect">Клиент</label>
            </div>
          </div>
          <div class="col-12">
            <div class="form-floating">
              <select class="form-select" v-model="ticketToEdit.flight" required>
                <option value="" disabled>Выберите рейс</option>
                <option v-for="flight in flights" :key="flight.id" :value="flight.id">
                  {{ flight.flight_number }}: {{ flight.departure }} -> {{ flight.destination }}
                </option>
              </select>
              <label for="editFlightSelect">Рейс</label>
            </div>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" @click="showModal = false">Закрыть</button>
        <button type="button" class="btn btn-primary" @click="onUpdateTicketAndClose">Сохранить изменения</button>

      </div>
    </div>
  </div>
</div>

  </div>
</template>


<style scoped>
.ticket-item {
  background-color: #f8f9fa; /* Светлый фон для карточки */
  border: 1px solid #dee2e6; /* Цвет границы */
  border-radius: 0.5rem; /* Закругление углов */
  transition: transform 0.2s; /* Плавное увеличение при наведении */
}
.ticket-title {
  font-size: 1.25rem; /* Размер заголовка */
  color: #343a40; /* Цвет заголовка */
}

.ticket-client,
.ticket-seat,
.ticket-date {
  margin: 0.5rem 0; /* Отступы для абзацев */
  color: #6c757d; /* Цвет текста */
}

.ticket-actions {
  display: flex;
  gap: 0.5rem; /* Отступ между кнопками */
}
</style>