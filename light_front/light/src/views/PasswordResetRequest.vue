<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Смена пароля</h1>
      </div>

      <form @submit.prevent="createRequest" class="form" id="form">
        <div class="form-field">
          <label for="username" class="form-label">Имя пользователя:</label>
          <input v-model="form.username" id="username" type="text" class="form-input" placeholder="Введите имя пользоваетля" required />
          <span v-if="errors.username" class="error">{{ errors.username }}</span>
        </div>

        <div class="form-field">
          <label for="email" class="form-label">Электронная почта:</label>
          <input v-model="form.email" id="email" type="email" class="form-input" placeholder="Введите электронную почту" required />
          <span v-if="errors.email" class="error">{{ errors.email }}</span>
        </div>

      </form>

      <div class="form-menu button-group">
        <button type="submit" class="button" form="form">Отправить письмо</button>
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
  username: '',
  email: '',
});

const loading = ref(false);

const cancelEdit = () => {
  router.back();
};

const errors = reactive({});
const validateForm = () => {
  errors.username = form.username ? '' : 'Имя пользователя обязательно!';
  errors.email = form.email ? '' : 'Электронная почта обязательна!';
  return Object.values(errors).every((error) => !error);
};

const createRequest = async () => {
  if (!validateForm()) {
    console.error('Форма содержит ошибки:', errors);
    return;
  }

  try {
    console.log('Отправляем данные для создания запроса:', form);

    const jsonData = {
      username: form.username,
      email: form.email,
      frontend_url: frontendUrl,
    };

    console.log('JSON данные перед отправкой:', jsonData);

    const jsonResponse = await axios.post(`${baseUrl}/password_reset_request/`, jsonData, {
      headers: { Authorization: '' },
    });

    console.log('Запрос создан:', jsonResponse.data);

    router.push({ 
      name: 'PostPasswordResetRequest',
      query: { username: form.username, email: form.email } 
    });
  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при создании запроса:', error.response.data);
    } else {
      console.error('Ошибка при создании запроса:', error.message);
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
