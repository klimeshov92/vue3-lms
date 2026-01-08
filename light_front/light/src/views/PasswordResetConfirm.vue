<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Смена пароля:</h1>
      </div>

      <form @submit.prevent="updateObject" class="form" id="form">

        <div class="form-field">
          <label for="password" class="form-label">Новый пароль:</label>
          <div class="password-wrapper">
            <input 
              v-model="form.password" 
              :type="isPasswordVisible.password ? 'text' : 'password'"
              id="password" 
              class="form-input password-input"
              placeholder="Введите пароль"
              required 
            />
            <span class="toggle-password" @click="togglePasswordVisibility('password')">
              {{ isPasswordVisible.password ? '👁️' : '👁️‍🗨️' }}
            </span>
          </div>
          <span v-if="errors.password" class="error">{{ errors.password }}</span>
        </div>

        <div class="form-field">
          <label for="password_confirm" class="form-label">Повторите новый пароль:</label>
          <div class="password-wrapper">
            <input 
              v-model="form.password_confirm" 
              :type="isPasswordVisible.password_confirm ? 'text' : 'password'"
              id="password_confirm" 
              class="form-input password-input"
              placeholder="Повторите пароль"
              required 
            />
            <span class="toggle-password" @click="togglePasswordVisibility('password_confirm')">
              {{ isPasswordVisible.password_confirm ? '👁️' : '👁️‍🗨️' }}
            </span>
          </div>
          <span v-if="errors.password_confirm" class="error">{{ errors.password_confirm }}</span>
        </div>

      </form>

      <div class="form-menu button-group">
        <button type="submit" class="button" form="form">Сменить пароль</button>
        <button type="button" @click="cancelEdit" class="button">Отмена</button>
      </div>
    </div>

  </div>

  <div v-else class="loading">
    <div>Загрузка данных...</div>
  </div>

</template>

<script setup>
import { reactive, onMounted, ref } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, frontendUrl, isTokenValid } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const form = reactive({
  password: '',
  password_confirm: '',
});

const loading = ref(false);


const isPasswordVisible = reactive({
  password: false,
  password_confirm: false,
});

const togglePasswordVisibility = (field) => {
  isPasswordVisible[field] = !isPasswordVisible[field];
};

const cancelEdit = () => {
  router.back();
};

const errors = reactive({});
const validateForm = () => {
  errors.password = form.password ? '' : 'Пароль обязателен!';
  errors.password_confirm = form.password_confirm ? '' : 'Повтор пароля обязателен!';
  if (form.password && form.password_confirm && form.password !== form.password_confirm) {
    errors.password_confirm = 'Пароли не совпадают!';
  }
  return Object.values(errors).every((error) => !error);
};

const uid = route.params.uid;
const token = route.params.token;

const updateObject = async () => {
  if (!validateForm()) {
    console.error('Форма содержит ошибки:', errors);
    return;
  }

  try {
    console.log('Отправляем данные для обнавления объекта:', form);

    const jsonData = {
      password: form.password,
    };

    console.log('JSON данные перед отправкой:', jsonData);

    const jsonResponse = await axios.post(`${baseUrl}/password_reset_confirm/${uid}/${token}/`, jsonData, {
      headers: { Authorization: '' },
    });

    console.log('Объект обновлен:', jsonResponse.data);
    router.push({ 
      name: 'PostPasswordResetConfirm',
      query: {done: true } 
    });

  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при обнавлении объекта:', error.response.data);
      router.push({ 
        name: 'PostPasswordResetConfirm',
        query: {done: false } 
      });
    } else {
      console.error('Ошибка при обнавлении объекта:', error.message);
    }
  }
};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
