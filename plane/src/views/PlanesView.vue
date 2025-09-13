<script setup>
import { ref, onBeforeMount, inject } from 'vue';
import axios from 'axios';

const airplanes = ref([]); 
const flights = ref([]);

const newAirplane = ref({ tail_number: '', model: '', capacity: '', flight: null });
const airplaneToEdit = ref({}); 
const airplanePictureRef = ref(); 
const airplaneEditPictureRef = ref(); 
const airplaneAddPictureUrl = ref('');
const airplaneEditPictureUrl = ref(''); 
const showModal = ref(false); 
const showEditAirplaneModal = ref(false); 
const showDeleteConfirmModal = ref(false); 
const otpVerified = inject('otpVerified');
const checkOtpStatus = inject('checkOtpStatus');
const airplaneToRemove = ref(null); 
const stats = ref({ count: 0, avg: 0, max: 0, min: 0 });
const selectedPicture = ref(null);

async function fetchPlanesStats() {
  try {
    const response = await axios.get("/api/airplanes/stats/");
    stats.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении статистики:", error);
  }
}

async function fetchFlights() {
  try {
    const response = await axios.get("/api/flights/");
    flights.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении рейсов:", error);
  }
}

async function fetchAirplanes() {
  try {
    const response = await axios.get("/api/airplanes/");
    airplanes.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении самолетов:", error);
  }
}

async function addAirplane() {
  const formData = new FormData();
  const file = airplanePictureRef.value?.files[0];
  if (file) {
    formData.append('picture', file);
  }
  formData.set('tail_number', newAirplane.value.tail_number);
  formData.set('model', newAirplane.value.model);
  formData.set('capacity', newAirplane.value.capacity);
  formData.set('flight', newAirplane.value.flight);

  try {
    await axios.post("/api/airplanes/", formData, { headers: { 'Content-Type': 'multipart/form-data' } });
    newAirplane.value = { tail_number: '', model: '', capacity: '', flight: null };
    airplaneAddPictureUrl.value = '';
    airplanePictureRef.value.value = null; // Сброс input
    await fetchAirplanes();
  } catch (error) {
    console.error("Ошибка при добавлении самолета:", error);
  }
}

function airplaneAddPictureChange() {
  const file = airplanePictureRef.value?.files[0];
  airplaneAddPictureUrl.value = file ? URL.createObjectURL(file) : '';
}

async function onAirplaneEditClick(airplane) {
  if (!otpVerified || !otpVerified.value) {
    alert("Доступ запрещён. Выполните двойную аутентификацию.");
    return;
  }
  airplaneToEdit.value = { ...airplane };
  airplaneEditPictureUrl.value = airplane.picture || ''; 
  showEditAirplaneModal.value = true;
}

async function updateAirplane() {
  if (!otpVerified || !otpVerified.value) {
    alert("Доступ запрещён. Выполните двойную аутентификацию.");
    return;
  }
  const formData = new FormData();
  formData.set('tail_number', airplaneToEdit.value.tail_number);
  formData.set('model', airplaneToEdit.value.model);
  formData.set('capacity', airplaneToEdit.value.capacity);
  formData.set('flight', airplaneToEdit.value.flight);

  const file = airplaneEditPictureRef.value?.files[0];
  if (file) {
    formData.append('picture', file);
  }

  try {
    await axios.put(`/api/airplanes/${airplaneToEdit.value.id}/`, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
    await fetchAirplanes();
    closeEditModal(); 
  } catch (error) {
    console.error("Ошибка при обновлении самолета:", error);
  }
}

function closeEditModal() {
  airplaneToEdit.value = {};
  airplaneEditPictureUrl.value = '';
  airplaneEditPictureRef.value.value = null;
  showEditAirplaneModal.value = false;

  // Удаляем backdrop и класс modal-open
  document.body.classList.remove('modal-open');
  const backdrop = document.querySelector('.modal-backdrop');
  if (backdrop) {
    backdrop.remove();
  }
}
function openPictureModal(image) {
  selectedPicture.value = image;
  showModal.value = true; 
}


async function removeAirplane(id) {
  try {
    await axios.delete(`/api/airplanes/${id}/`);
    await fetchAirplanes();
  } catch (error) {
    console.error("Ошибка при удалении самолета:", error);
  }
}

function confirmRemovePlane(plane) {
  airplaneToRemove.value = plane;
  showDeleteConfirmModal.value = true;
}

async function onRemoveConfirmed() {
  if (airplaneToRemove.value) {
    await removeAirplane(airplaneToRemove.value.id);
    airplaneToRemove.value = null;
    showDeleteConfirmModal.value = false;
  }
}

function getFlightInfo(flightId) {
  const flight = flights.value.find(f => f.id === flightId);
  return flight ? `${flight.flight_number}: ${flight.departure} -> ${flight.destination}` : 'Нет рейса';
}

onBeforeMount(async () => {
  await fetchFlights();
  await fetchAirplanes();
  await fetchPlanesStats();
  await checkOtpStatus();
});
</script>

<template>
  <div class="container-fluid">
    <h1 class="my-4">Самолеты</h1>
  
    <form @submit.prevent="addAirplane" class="mb-4">
      <div class="row g-3">
        <div class="col">
          <input type="text" class="form-control" v-model="newAirplane.tail_number" placeholder="Бортовой номер" required />
        </div>
        <div class="col">
          <input type="text" class="form-control" v-model="newAirplane.model" placeholder="Модель самолета" required />
        </div>
        <div class="col">
          <input type="number" class="form-control" v-model="newAirplane.capacity" placeholder="Вместимость" required />
        </div>
        <div class="col">
          <select class="form-select" v-model="newAirplane.flight" required>
            <option value="" disabled selected>Выберите рейс</option>
            <option v-for="flight in flights" :key="flight.id" :value="flight.id">
              {{ flight.flight_number }}: {{ flight.departure }} -> {{ flight.destination }}
            </option>
          </select>
        </div>
        <div class="col-auto">
          <input class="form-control" type="file" ref="airplanePictureRef" @change="airplaneAddPictureChange">
        </div>
        <div class="col-auto">
          <img :src="airplaneAddPictureUrl" style="max-height: 60px;" alt="Превью">
        </div>
        <div class="col-auto">
          <button class="btn btn-primary" type="submit">Добавить самолет</button>
        </div>
      </div>
    </form>

    <div class="p-2">
        <h3>Статистика</h3>
        <ul>
          <li>Всего самолетов: {{ stats.count }}</li>
          <li>Средний ID: {{ stats.avg }}</li>
          <li>Максимальный ID: {{ stats.max }}</li>
          <li>Минимальный ID: {{ stats.min }}</li>
        </ul>
    </div>

    <div class="airplanes-grid">
      <div v-for="airplane in airplanes" :key="airplane.id" class="airplane-card">
        <img v-if="airplane.picture" :src="airplane.picture" alt="Airplane" class="airplane-image" @click="openPictureModal(airplane.picture)" />
        <div class="airplane-info">
          <h5>{{ airplane.tail_number }} ({{ airplane.model }})</h5>
          <p>Вместимость: {{ airplane.capacity }}</p>
          <p>Рейс: {{ getFlightInfo(airplane.flight) }}</p>
        </div>
        <div class="button-group">
          <button class="btn btn-success" @click="onAirplaneEditClick(airplane)"><i class="bi bi-pen-fill"></i> Редактировать</button>
          <button class="btn btn-danger" @click="confirmRemovePlane(airplane)">Удалить</button>
        </div>
      </div>
    </div>

    <div v-if="showDeleteConfirmModal" class="modal fade show" tabindex="-1" style="display: block;" @click="showDeleteConfirmModal = false">
              <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title">Подтверждение удаления</h5>
                    <button type="button" class="btn-close" @click="showDeleteConfirmModal = false"></button>
                  </div>
                  <div class="modal-body">
                    <p>Вы действительно хотите удалить самолет ?</p>
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="showDeleteConfirmModal = false">Отмена</button>
                    <button type="button" class="btn btn-danger" @click="onRemoveConfirmed">Удалить</button>
                  </div>
                </div>
              </div>
            </div>

    <!-- Модальное окно для редактирования самолета -->
    <div v-if="showEditAirplaneModal" class="modal fade show" tabindex="-1" style="display: block;">
      <div class="modal-dialog modal-lg"> 
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="editAirplaneModalLabel">Редактировать самолет</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="airplaneToEdit = {}"></button>
          </div>
          <div class="modal-body">
            <div class="row g-3">
              <div class="col-12 col-md-6"> 
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="airplaneToEdit.tail_number" required />
                  <label for="editAirplaneTailNumber">Бортовой номер</label>
                </div>
              </div>
              <div class="col-12 col-md-6">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="airplaneToEdit.model" required />
                  <label for="editAirplaneModel">Модель самолета</label>
                </div>
              </div>
              <div class="col-12 col-md-6">
                <div class="form-floating">
                  <input type="number" class="form-control" v-model="airplaneToEdit.capacity" required />
                  <label for="editAirplaneCapacity">Вместимость</label>
                </div>
              </div>
              <div class="col-12 col-md-6">
                <div class="form-floating">
                  <select class="form-select" v-model="airplaneToEdit.flight" required>
                    <option value="" disabled selected>Выберите рейс</option>
                    <option v-for="flight in flights" :key="flight.id" :value="flight.id">
                      {{ flight.flight_number }}: {{ flight.departure }} -> {{ flight.destination }}
                    </option>
                  </select>
                  <label for="editAirplaneFlight">Рейс</label>
                </div>
              </div>
              <div class="col-12 col-md-6">
                <input class="form-control" type="file" ref="airplaneEditPictureRef" @change="airplaneAddPictureChange">
              </div>
              <div class="col-12 col-md-6 d-flex align-items-center justify-content-center">
                <img :src="airplaneAddPictureUrl" style="max-height: 100px;" alt="Превью">
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="airplaneToEdit = {}">Закрыть</button>
            <button type="button" class="btn btn-primary" @click="updateAirplane">Сохранить изменения</button>
          </div>
        </div>
      </div>
    </div>

     <!-- Модальное окно для изображения -->
     <div v-if="showModal" class="modal fade show" tabindex="-1" style="display: block;" @click="showModal = false">
      <div class="modal-dialog modal-dialog-centered" @click.stop>
        <div class="modal-content">
          <div class="modal-body">
            <img :src="selectedPicture" class="img-fluid" alt="Изображение самолета" />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showModal = false">Закрыть</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container-fluid {
  max-width: 1200px;
  margin: 0 auto;
}

.airplanes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.airplane-card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: box-shadow 0.2s ease;
}

.airplane-card:hover {
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
}

.airplane-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.airplane-info {
  padding: 15px;
  text-align: center;
}

.airplane-info h5 {
  margin-bottom: 10px;
  font-size: 1.2rem;
  font-weight: bold;
}

.airplane-info p {
  margin-bottom: 5px;
  color: #666;
}

.button-group {
  display: flex;
  justify-content: space-between;
  padding: 15px;
  border-top: 1px solid #eee;
  background-color: #fafafa;
}

.button-group .btn {
  flex-grow: 1;
  margin-right: 10px;
}

.button-group .btn:last-child {
  margin-right: 0;
}

.modal-body img {
  max-width: 100%;
}
</style>