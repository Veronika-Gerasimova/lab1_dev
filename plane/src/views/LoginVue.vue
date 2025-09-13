<template>
  <div class="login-container">
    <div class="login-box shadow-lg">
      <h2 class="login-title">Добро пожаловать ✈️</h2>
      <p class="login-subtitle">Пожалуйста, войдите в свой аккаунт</p>
      
      <input 
        v-model="username" 
        placeholder="Имя пользователя" 
        required 
        class="form-control login-input"
      />
      <input 
        type="password" 
        v-model="password" 
        placeholder="Пароль" 
        required 
        class="form-control login-input"
      />
      
      <button @click="login" class="btn btn-primary w-100 login-btn">Войти</button>
      
      <div v-if="error" class="error mt-3">{{ error }}</div>
    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import useUserStore from '../stores/userStore';
import Cookies from 'js-cookie';

const router = useRouter();
const username = ref("");
const password = ref("");
const userStore = useUserStore();
const error = ref(""); 
async function login() {
  try {
    const csrfToken = Cookies.get('csrftoken');

    const passwordResponse = await axios.post('/api/user/login/', {
      username: username.value,
      password: password.value,
    }, {
      headers: {
        'X-CSRFToken': csrfToken,
      }
    });

    if (passwordResponse.status === 200) {
      await userStore.fetchUser(); 
      router.push("/"); 
    } else {
      error.value = 'Неверные учетные данные.';
    }
  } catch (err) {
    console.error("Login error:", err);
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = err.response.data.detail;
    } else {
      error.value = 'Произошла ошибка. Попробуйте снова.';
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(45deg, #4a90e2, #50e3c2);
  padding: 1rem;
}

.login-box {
  background-color: #fff;
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.login-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
}

.login-subtitle {
  font-size: 1rem;
  color: #666;
  margin-bottom: 1.5rem;
}

.login-input {
  margin-bottom: 1rem;
  padding: 0.8rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  box-sizing: border-box;
}

.login-input:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 8px rgba(74, 144, 226, 0.2);
}

.login-btn {
  padding: 0.8rem;
  font-size: 1.1rem;
  background-color: #4a90e2;
  border: none;
  border-radius: 6px;
  color: #fff;
  transition: background-color 0.3s ease;
}

.login-btn:hover {
  background-color: #3d7fc1;
}

.error {
  font-size: 0.9rem;
  color: #d9534f;
}
</style>
