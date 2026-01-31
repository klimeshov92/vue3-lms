<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание организации</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">
        <div class="form-field">
          <label for="legal_name" class="form-label">Юридическое название:</label>
          <input v-model="form.legal_name" id="legal_name" type="text" class="form-input" placeholder="Введите юридическое название" required />
          <span v-if="errors.legal_name" class="error">{{ errors.legal_name }}</span>
        </div>

        <div class="form-field">
          <label for="tin" class="form-label">ИНН:</label>
          <input v-model="form.tin" id="tin" type="number" class="form-input" placeholder="Введите ИНН" required/>
          <span v-if="errors.tin" class="error">{{ errors.tin }}</span>
        </div>
      </form>

      <div class="form-menu button-group">
        <button type="submit" class="button" form="form">Сохранить</button>
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
import { baseUrl, isTokenValid , goBackSmart } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const form = reactive({
  legal_name: '',
  tin: '',
});

const loading = ref(false);

const cancelEdit = () => {
  goBackSmart(router);
};

const errors = reactive({});
const validateForm = () => {
  errors.legal_name = form.legal_name ? '' : 'Юридическое название обязательно!';
  errors.tin = form.tin ? '' : 'ИНН обязателен!';
  return Object.values(errors).every((error) => !error);
};

const createObject = async () => {
  if (!validateForm()) {
    console.error('Форма содержит ошибки:', errors);
    return;
  }

  try {
    console.log('Отправляем данные для создания объекта:', form);

    const jsonData = {
      legal_name: form.legal_name,
      tin: form.tin,
    };

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/organizations/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);

    localStorage.removeItem('userPermissions');

    router.push({ name: 'OrganizationDetail', params: { id: jsonResponse.data.id }  });
  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при создании объекта:', error.response.data);
    } else {
      console.error('Ошибка при создании объекта:', error.message);
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
