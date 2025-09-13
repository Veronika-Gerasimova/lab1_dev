<script setup>
import { onBeforeMount, ref, inject } from 'vue';
import axios from 'axios';

const baggages = ref([]);
const clients = ref([]);
const tickets = ref([]);
const newBaggage = ref({
  ticket: null,
  weight: '',
  baggage_type: ''
});
const baggageToEdit = ref({});
const baggageToRemove = ref(null); 
const showDeleteConfirmModal = ref(false); 

const stats = ref({ count: 0, avg: 0, max: 0, min: 0 });
const otpVerified = inject('otpVerified');
const checkOtpStatus = inject('checkOtpStatus');

// Функции для получения данных
async function fetchBaggagesStats() {
  try {
    const response = await axios.get("/api/baggage/stats/");
    stats.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении статистики:", error);
  }
}

async function fetchClients() {
  const r = await axios.get('/api/clients/');
  clients.value = r.data;
}

async function fetchTickets() {
  const r = await axios.get('/api/tickets/');
  tickets.value = r.data;
}

async function fetchBaggages() {
  const r = await axios.get('/api/baggage/');
  baggages.value = r.data;
}

// Добавление багажа
async function addBaggage() {
  try {
    await axios.post('/api/baggage/', newBaggage.value);
    newBaggage.value = { ticket: null, weight: '', baggage_type: '' };
    await fetchBaggages();
  } catch (error) {
    console.error("Ошибка при добавлении багажа:", error.response ? error.response.data : error.message);
  }
}

// Удаление багажа
async function removeBaggage(id) {
  try {
    await axios.delete(`/api/baggage/${id}/`);
    await fetchBaggages();
  } catch (error) {
    console.error("Ошибка при удалении багажа:", error);
  }
}

// Открытие модального окна подтверждения удаления
function confirmRemoveBaggage(baggage) {
  baggageToRemove.value = baggage;
  showDeleteConfirmModal.value = true;
}

// Подтверждение удаления багажа
async function onRemoveConfirmed() {
  if (baggageToRemove.value) {
    await removeBaggage(baggageToRemove.value.id); 
    showDeleteConfirmModal.value = false; 
    baggageToRemove.value = null; 
  }
}

const showEditModal = ref(false); // Переменная для открытия модального окна редактирования

// Открытие модального окна редактирования
async function onBaggageEditClick(baggage) {
  if (!otpVerified || !otpVerified.value) {
    alert("Доступ запрещён. Выполните двойную аутентификацию.");
    return;
  }

  // Устанавливаем данные для редактирования багажа
  baggageToEdit.value = {
    ...baggage,
    ticket: baggage.ticket_detail.id // Передаем только ID билета
  };

  // Открываем модальное окно
  showEditModal.value = true; 
}

// Обновление багажа
async function updateBaggage() {
  if (!otpVerified || !otpVerified.value) {
    alert("Доступ запрещён. Выполните двойную аутентификацию.");
    return;
  }
  try {
    const formData = {
      weight: baggageToEdit.value.weight,
      baggage_type: baggageToEdit.value.baggage_type,
      ticket: baggageToEdit.value.ticket 
    };

    console.log("Form Data to update:", formData); // Логирование данных
    console.log("Baggage ID:", baggageToEdit.value.id); // Логирование ID багажа

    await axios.put(`/api/baggage/${baggageToEdit.value.id}/`, formData);
    await fetchBaggages(); // Обновляем список багажа после сохранения
  } catch (error) {
    console.error("Ошибка при обновлении багажа:", error.response ? error.response.data : error);
  }
  showEditModal.value = false; // Закрытие модального окна после обновления
}

onBeforeMount(async () => {
  await fetchClients();
  await fetchTickets();
  await fetchBaggages();
  await fetchBaggagesStats();
  await checkOtpStatus();
});
</script>

<template>
  <div class="container">
    <h1 class="my-4">Багаж</h1>
    <form @submit.prevent="addBaggage" class="mb-4">
      <div class="row">
        <div class="col">
          <select v-model="newBaggage.ticket" class="form-select" required>
            <option value="" disabled>Выберите билет</option>
            <option v-for="ticket in tickets" :key="ticket.id" :value="ticket.id">
              {{ ticket.seat_number }} ({{ ticket.client_detail.name }})
            </option>
          </select>
        </div>
        <div class="col">
          <input v-model="newBaggage.weight" type="number" class="form-control" placeholder="Вес (кг)" required />
        </div>
        <div class="col">
          <input v-model="newBaggage.baggage_type" type="text" class="form-control" placeholder="Тип багажа" required />
        </div>
        <div class="col-auto">
          <button class="btn btn-primary" type="submit">Добавить багаж</button>
        </div>
      </div>
    </form>

    <!-- Вывод статистики -->
    <div class="p-2">
            <h3>Статистика</h3>
            <ul>
              <li>Всего багажа: {{ stats.count }}</li>
              <li>Средний ID: {{ stats.avg }}</li>
              <li>Максимальный ID: {{ stats.max }}</li>
              <li>Минимальный ID: {{ stats.min }}</li>
            </ul>
      </div>

    <div v-for="baggage in baggages" :key="baggage.id" class="baggage-item mb-3 p-3 border rounded">
      <div class="col-8">
        <h5>{{ baggage.baggage_type }} - Вес: {{ baggage.weight }} кг</h5>
        <p><strong>Билет:</strong> {{ baggage.ticket_detail.seat_number }} ({{ baggage.ticket_detail.client_detail.name }})</p>
      </div>
      <button class="btn btn-success" @click="onBaggageEditClick(baggage)">
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="confirmRemoveBaggage(baggage)">
        <i class="bi bi-x"></i>
      </button>
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
            <p>Вы действительно хотите удалить багаж ?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showDeleteConfirmModal = false">Отмена</button>
            <button type="button" class="btn btn-danger" @click="onRemoveConfirmed">Удалить</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно для редактирования багажа -->
    <div v-if="showEditModal" class="modal fade show" tabindex="-1" style="display: block;">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать багаж</h1>
            <button type="button" class="btn-close" @click="showEditModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="row g-3">
              <div class="col-12">
                <div class="form-floating">
                  <input type="text" class="form-control" id="editBaggageType" v-model="baggageToEdit.baggage_type" required />
                  <label for="editBaggageType">Тип багажа</label>
                </div>
              </div>
              <div class="col-12">
                <div class="form-floating">
                  <input type="number" class="form-control" id="editBaggageWeight" v-model="baggageToEdit.weight" required />
                  <label for="editBaggageWeight">Вес (кг)</label>
                </div>
              </div>
              <div class="col-12">
                <select class="form-select" v-model="baggageToEdit.ticket" required>
                  <option value="" disabled>Выберите билет</option>
                  <option v-for="ticket in tickets" :key="ticket.id" :value="ticket.id">
                    {{ ticket.seat_number }} ({{ ticket.client_detail.name }})
                  </option>
                </select>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showEditModal = false">Закрыть</button>
            <button type="button" class="btn btn-primary" @click="updateBaggage">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
.baggage-item {
  padding: 0.5rem;
  border: 1px solid silver;
  margin: 1rem 0;
  box-shadow: 0 0 4px silver;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr auto auto auto;
  gap: 16px;
  align-items: center;
}
</style>
