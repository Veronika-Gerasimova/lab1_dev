<script setup>
import { computed, onBeforeMount,  watch, ref, inject } from 'vue';
import axios from 'axios';

const clients = ref([]);
const tickets = ref([]);
const loading = ref(false);
const clientToAdd = ref({});
const clientToEdit = ref({});
const clientPictureRef = ref();
const clientAddPictureUrl = ref(null);
const clientEditPictureRef = ref();
const clientEditPictureUrl = ref(null);
const selectedPicture = ref(null);
const showModal = ref(false);
const clientToRemove = ref(null); 
const showDeleteConfirmModal = ref(false);
const animationState = ref(""); 
const otpVerified = inject('otpVerified');
const checkOtpStatus = inject('checkOtpStatus');

const updatePlaneState = () => {
  if (clientToAdd.value.name && clientToAdd.value.email && clientToAdd.value.phone) {
    animationState.value = "landing"; // Самолет приземляется
  } else if (clientToAdd.value.name && clientToAdd.value.email) {
    animationState.value = "flying"; // Самолет в полете
  } else if (clientToAdd.value.name) {
    animationState.value = "taking-off"; // Самолет взлетает
  } else {
    animationState.value = ""; // Самолет на месте
  }
};

watch(
  () => clientToAdd.value,
  updatePlaneState,
  { deep: true }
);

const uniqueNames = computed(() => {
  return [...new Set(clients.value.map(client => client.name))];
});

const uniqueEmails = computed(() => {
  return [...new Set(clients.value.map(client => client.email))];
});

const uniquePhones = computed(() => {
  return [...new Set(clients.value.map(client => client.phone))];
});

const selectedName = ref(null);
const selectedEmail = ref(null);
const selectedPhone = ref(null);

const filteredClients = computed(() => {
  return clients.value.filter(client => {
    const matchesName = selectedName.value
      ? client.name === selectedName.value
      : true;
    const matchesEmail = selectedEmail.value
      ? client.email === selectedEmail.value
      : true;
    const matchesPhone = selectedPhone.value
      ? client.phone === selectedPhone.value
      : true;

    return matchesName && matchesEmail && matchesPhone;
  });
});

const stats = ref({ count: 0, avg: 0, max: 0, min: 0 });

async function fetchClientStats() {
  try {
    const response = await axios.get("/api/clients/stats/");
    stats.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении статистики:", error);
  }
}

function openPictureModal(image) {
  selectedPicture.value = image;
  showModal.value = true; 
}

async function fetchClients() {
  loading.value = true;
  try {
    const response = await axios.get("/api/clients/");
    clients.value = response.data;
  } finally {
    loading.value = false;
  }
}

async function fetchTickets() {
  const response = await axios.get("/api/tickets/");
  tickets.value = response.data;
}

async function onClientAdd() {
  const formData = new FormData();
  formData.append('picture', clientPictureRef.value.files[0]);
  formData.set('name', clientToAdd.value.name);
  formData.set('email', clientToAdd.value.email);
  formData.set('phone', clientToAdd.value.phone);

  await axios.post("/api/clients/", formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  await fetchClients();
  clientToAdd.value = {}; 
}

function clientAddPictureChange() {
  if (clientPictureRef.value.files[0]) {
    clientAddPictureUrl.value = URL.createObjectURL(clientPictureRef.value.files[0]);
  } else {
    clientAddPictureUrl.value = null; 
  }
}

function confirmRemoveClient(client) {
  clientToRemove.value = client;
  showDeleteConfirmModal.value = true; 
}

async function onRemoveConfirmed() {
  if (clientToRemove.value) {
    await axios.delete(`/api/clients/${clientToRemove.value.id}/`);
    await fetchClients();
    showDeleteConfirmModal.value = false; 
    clientToRemove.value = null; 
  }
}

async function onClientEditClick(client) {
  if (!otpVerified || !otpVerified.value) {
    alert("Доступ запрещён. Выполните двойную аутентификацию.");
    return;
  }
  clientToEdit.value = { ...client };

  if (client.picture) {
    clientEditPictureUrl.value = client.picture;
  } else {
    clientEditPictureUrl.value = null;
  }

  showEditModal.value = true;
}


const showEditModal = ref(false);

async function onUpdateClient() {
  if (!otpVerified.value) {
    alert("Доступ запрещён. Выполните двойную аутентификацию.");
    return;
  }
  const formData = new FormData();
  if (clientEditPictureRef.value?.files[0]) {
    formData.append('picture', clientEditPictureRef.value.files[0]);
  }
  formData.set('name', clientToEdit.value.name);
  formData.set('email', clientToEdit.value.email);
  formData.set('phone', clientToEdit.value.phone);

  await axios.put(`/api/clients/${clientToEdit.value.id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  await fetchClients();
  showEditModal.value = false;
}

async function downloadFile(type) {
  try {
    const response = await axios.get(`/api/clients/export?type=${type}`, {
      responseType: 'blob',
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `clients.${type === 'word' ? 'docx' : 'xlsx'}`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (error) {
    console.error("Ошибка при скачивании файла:", error);
  }
}

onBeforeMount(async () => {
  await fetchClients();
  await fetchTickets();
  await fetchClientStats();
  await checkOtpStatus();
});
</script>

<template>
  <div class="container-fluid">
    <h1 class="my-4">Клиенты</h1>
    <div class="p-2">
      <div class="plane-container">
      <div :class="['plane', animationState]"></div>
      </div>
      <form @submit.prevent="onClientAdd" class="mb-4">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="clientToAdd.name" required />
              <label for="clientNameInput">ФИО</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="email" class="form-control" v-model="clientToAdd.email" required />
              <label for="clientEmailInput">Электронная почта</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="clientToAdd.phone" required />
              <label for="clientPhoneInput">Номер телефона</label>
            </div>
          </div>
          <div class="col-auto">
            <input class="form-control" type="file" ref="clientPictureRef" @change="clientAddPictureChange">
          </div>
          <div class="col-auto">
            <img :src="clientAddPictureUrl" style="max-height: 60px;" alt="Предпросмотр">
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

    <div class="p-2">
        <h3>Статистика</h3>
        <ul>
          <li>Всего клиентов: {{ stats.count }}</li>
          <li>Средний ID: {{ stats.avg }}</li>
          <li>Максимальный ID: {{ stats.max }}</li>
          <li>Минимальный ID: {{ stats.min }}</li>
        </ul>
      </div>
    <div class="filters d-flex gap-2 mb-4">
      <div>
        <label for="filterName" class="form-label">ФИО</label>
        <select
          id="filterName"
          class="form-select"
          v-model="selectedName"
        >
          <option :value="null">Все</option>
          <option v-for="name in uniqueNames" :key="name" :value="name">
            {{ name }}
          </option>
        </select>
      </div>
      <div>
        <label for="filterEmail" class="form-label">Электронная почта</label>
        <select
          id="filterEmail"
          class="form-select"
          v-model="selectedEmail"
        >
          <option :value="null">Все</option>
          <option v-for="email in uniqueEmails" :key="email" :value="email">
            {{ email }}
          </option>
        </select>
      </div>
      <div>
        <label for="filterPhone" class="form-label">Телефон</label>
        <select
          id="filterPhone"
          class="form-select"
          v-model="selectedPhone"
        >
          <option :value="null">Все</option>
          <option v-for="phone in uniquePhones" :key="phone" :value="phone">
            {{ phone }}
          </option>
        </select>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-info" @click="downloadFile('excel')">Скачать Excel</button>
        <button class="btn btn-info" @click="downloadFile('word')">Скачать Word</button>
      </div>
    </div>
    <div class="client-cards-container">
    <div 
      v-for="item in filteredClients" 
      :key="item.id" 
      class="client-card shadow-sm p-3 mb-4 bg-white rounded"
    >
      <div class="row align-items-center">
        <!-- Изображение клиента -->
        <div class="col-md-3 text-center">
          <img
            v-if="item.picture"
            :src="item.picture"
            alt="Client"
            @click="openPictureModal(item.picture)"
            class="client-image rounded-circle img-thumbnail"
          />
        </div>

        <div class="col-md-6">
          <h5 class="client-name text-primary">{{ item.name }}</h5>
          <p class="client-info text-secondary mb-2">
            <i class="bi bi-envelope-fill me-2"></i>{{ item.email }}
          </p>
          <p class="client-info text-secondary">
            <i class="bi bi-telephone-fill me-2"></i>{{ item.phone }}
          </p>
        </div>
        <div class="col-md-3 text-center">
          <button class="btn btn-outline-success me-2" @click="onClientEditClick(item)">
            <i class="bi bi-pen-fill"></i> Изменить
          </button>
          <button class="btn btn-outline-danger" @click="confirmRemoveClient(item)">
            <i class="bi bi-trash-fill"></i> Удалить
          </button>
        </div>
      </div>
    </div>
  </div>
    </div>

    <!-- Модальное окно для редактирования клиента -->
<div v-if="showEditModal" class="modal fade show" tabindex="-1" style="display: block; background-color: rgba(0, 0, 0, 0.5);">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <!-- Заголовок -->
      <div class="modal-header">
        <h5 class="modal-title">Редактировать данные клиента</h5>
        <button type="button" class="btn-close" @click="showEditModal = false"></button>
      </div>
      
      <!-- Тело модального окна -->
      <div class="modal-body">
        <div class="row g-4">
          <!-- Имя клиента -->
          <div class="col-12">
            <div class="form-floating">
              <input 
                type="text" 
                class="form-control" 
                id="editClientName" 
                v-model="clientToEdit.name" 
                placeholder="Введите ФИО" 
                required />
              <label for="editClientName">ФИО</label>
            </div>
          </div>

          <!-- Электронная почта -->
          <div class="col-12">
            <div class="form-floating">
              <input 
                type="email" 
                class="form-control" 
                id="editClientEmail" 
                v-model="clientToEdit.email" 
                placeholder="Введите адрес электронной почты" 
                required />
              <label for="editClientEmail">Электронная почта</label>
            </div>
          </div>

          <!-- Телефон -->
          <div class="col-12">
            <div class="form-floating">
              <input 
                type="text" 
                class="form-control" 
                id="editClientPhone" 
                v-model="clientToEdit.phone" 
                placeholder="Введите номер телефона" 
                required />
              <label for="editClientPhone">Телефон</label>
            </div>
          </div>

          <!-- Фото -->
          <div class="col-12 col-md-auto">
            <label class="form-label">Загрузить фото</label>
            <input 
              class="form-control" 
              type="file" 
              ref="clientEditPictureRef" 
              @change="clientEditPictureChange">
          </div>
          <div class="col-12 col-md-auto">
            <img 
              v-if="clientEditPictureUrl" 
              :src="clientEditPictureUrl" 
              class="img-thumbnail" 
              style="max-height: 100px;" 
              alt="Предпросмотр">
          </div>
        </div>
      </div>
      
      <!-- Футер -->
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" @click="showEditModal = false">Закрыть</button>
        <button type="button" class="btn btn-success" @click="onUpdateClient">Сохранить изменения</button>
      </div>
    </div>
  </div>
</div>


    <!-- Модальное окно для подтверждения удаления клиента -->
    <div v-if="showDeleteConfirmModal" class="modal fade show" tabindex="-1" style="display: block;" @click="showDeleteConfirmModal = false">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Подтверждение удаления</h5>
            <button type="button" class="btn-close" @click="showDeleteConfirmModal = false"></button>
          </div>
          <div class="modal-body">
            <p>Вы действительно хотите удалить клиента {{ clientToRemove?.name }}?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showDeleteConfirmModal = false">Отмена</button>
            <button type="button" class="btn btn-danger" @click="onRemoveConfirmed">Удалить</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно для показа картинки -->
    <div v-if="showModal" class="modal fade show" tabindex="-1" style="display: block;" @click="showModal = false">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-body">
            <img :src="selectedPicture" class="img-fluid" alt="Изображение клиента" @click.stop>
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
.client-cards-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.client-card {
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.client-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.client-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  cursor: pointer;
}

.client-name {
  font-size: 1.25rem;
  font-weight: bold;
}

.client-info {
  font-size: 0.9rem;
}

button {
  width: 100%;
  margin-top: 0.5rem;
}

button i {
  margin-right: 0.3rem;
}

button.btn-outline-success:hover {
  background-color: #28a745;
  color: #fff;
}

button.btn-outline-danger:hover {
  background-color: #dc3545;
  color: #fff;
}

.plane-container {
  position: relative;
  height: 150px;
  margin-top: 20px;
  overflow: hidden;
  border-radius: 10px;
}

.plane {
  position: absolute;
  width: 150px;
  height: 50px;
  background: url('@/assets/plane22.jpg') no-repeat center center / contain;
  bottom: 0;
  left: 0;
  transform: translateX(0) rotate(0deg);
  transition: all 5s ease-in-out;
}

.taking-off {
  bottom: 40%;
  left: 20%;
  transform: rotate(-10deg);
}

.flying {
  bottom: 70%;
  left: 50%;
  transform: rotate(0deg);
}

.landing {
  bottom: 0;
  left: 90%;
  transform: rotate(10deg);
}
</style>

