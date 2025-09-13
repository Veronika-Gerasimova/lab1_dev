<script setup>
import { ref, onBeforeMount, provide } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import useUserStore from './stores/userStore';
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
const { isAuthenticated, username, userId } = storeToRefs(userStore);

// Стейты для OTP
const otpKey = ref('');
const otpVerified = ref(false);
const otpLoading = ref(false);
const qrCodeUrl = ref(null);

// Установка CSRF-токена
onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
});
// Проверить статус OTP
const checkOtpStatus = async () => {
  try {
    const response = await axios.get('/api/auth/otp-status/');
    otpVerified.value = response.data.otp_good;
  } catch (error) {
    console.error('Ошибка проверки OTP:', error);
    otpVerified.value = false;
  }
};

// Функция для получения QR-кода
const fetchQrCode = async () => {
  try {
    const response = await axios.get('/api/auth/otp-qr-code/', {
      responseType: 'blob', // Важно для получения изображения
    });
    qrCodeUrl.value = URL.createObjectURL(response.data);
  } catch (error) {
    console.error('Ошибка загрузки QR-кода:', error);
  }
};

// Функция для отправки OTP
const submitOtp = async () => {
  otpLoading.value = true;
  try {
    const response = await axios.post('/api/auth/otp-login/', { key: otpKey.value });
    otpVerified.value = response.data.success;
    if (!otpVerified.value) {
      alert("Неверный OTP-код. Попробуйте снова.");
    } else {
      alert("Двойная аутентификация успешно выполнена!");
    }
  } catch (error) {
    console.error("Ошибка отправки OTP:", error);
  } finally {
    otpLoading.value = false;
  }
};
provide('otpVerified', otpVerified);
provide('submitOtp', submitOtp);
provide('checkOtpStatus', checkOtpStatus);
</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-lg">
      <div class="container-fluid">
        <a class="navbar-brand text-uppercase fw-bold" href="/">Travel</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/clients" active-class="active-page">Клиенты</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/tickets" active-class="active-page">Билеты</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/baggages" active-class="active-page">Багаж</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/flights" active-class="active-page">Рейсы</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/airplanes" active-class="active-page">Самолеты</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <!-- Кнопка для отображения QR-кода -->
            <li class="nav-item">
              <button 
                class="btn btn-outline-light me-2" 
                @click="fetchQrCode" 
                data-bs-toggle="modal" 
                data-bs-target="#qrModal"
              >
                QR-код для 2FA
              </button>
            </li>
            <!-- Поле ввода и кнопка для OTP -->
            <li class="nav-item dropdown">
              <button 
                class="btn btn-outline-light me-2 dropdown-toggle" 
                type="button" 
                data-bs-toggle="dropdown" 
                aria-expanded="false"
              >
                Ввести OTP
              </button>
              <ul class="dropdown-menu p-3">
                <li>
                  <input
                    type="text"
                    class="form-control form-control-sm"
                    v-model="otpKey"
                    placeholder="Введите OTP-код"
                  />
                </li>
                <li class="mt-2">
                  <button 
                    class="btn btn-sm btn-primary w-100" 
                    @click="submitOtp" 
                    :disabled="otpLoading.value"
                  >
                    {{ otpLoading.value ? 'Загрузка...' : 'Подтвердить OTP' }}
                  </button>
                </li>
              </ul>
            </li>
          </ul>
          <ul class="navbar-nav">
            <!-- Кнопка пользователя -->
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Пользователь
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="/admin">Админка</a></li>
                <li><a class="dropdown-item" href="/login">Вход</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Модальное окно для QR-кода -->
    <div class="modal fade" id="qrModal" tabindex="-1" aria-labelledby="qrModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="qrModalLabel">QR-код для OTP</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
          </div>
          <div class="modal-body text-center">
            <img v-if="qrCodeUrl" :src="qrCodeUrl" alt="QR-код для OTP" class="img-fluid" />
            <p v-else>QR-код загружается...</p>
          </div>
        </div>
      </div>
    </div>

    <div class="container mt-4">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.navbar {
  font-family: 'Roboto', sans-serif;
  border-radius: 0.5rem;
}

.navbar-brand {
  font-size: 1.25rem;
  letter-spacing: 0.05rem;
}

.nav-link {
  color: white !important;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #ffdd57 !important; /* Золотистый цвет при наведении */
}

.btn-light {
  color: #007bff;
  font-weight: bold;
  border-radius: 0.25rem;
  padding: 0.25rem 0.75rem;
}

.navbar-toggler {
  border: none;
}

.navbar-toggler-icon {
  filter: invert(1);
}

/* Подсветка активного элемента */
.nav-link.active-page {
  background-color: #57bfff;
  color: #eaedf4 !important;
  border-radius: 0.5rem;
  font-weight: bold;
}

/* Плавный переход */
.nav-link {
  transition: background-color 0.3s, color 0.3s;
}

.otp-auth-section {
  background-color: #f8f9fa;
}
</style>
