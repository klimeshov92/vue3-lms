<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание страницы</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">

        <div class="form-field">
          <label for="title" class="form-label">Заголовок:</label>
          <input v-model="form.title" id="title" type="text" class="form-input" placeholder="Введите заголовок" required />
          <span v-if="errors.title" class="error">{{ errors.title }}</span>
        </div>

        <div lass="form-field form-field-full_width">
          <label for="desc" class="form-label">Содержание:</label>
          
          <EditorComponent v-model="form.content" />

          <span v-if="errors.content" class="error">{{ errors.content }}</span>
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
import { baseUrl, isTokenValid } from '../utils/utils';
import EditorComponent from '../components/EditorComponent.vue';

const route = useRoute();
const router = useRouter();

const form = reactive({
  title: '',
  content: '',
});

const loading = ref(false);

const cancelEdit = () => {
  router.back();
};

const errors = reactive({});
const validateForm = () => {
  errors.title = form.title ? '' : 'Название обязательно!';
  errors.content = form.content.trim() ? '' : 'Содержание обязательно!';
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
      title: form.title,
      content: form.content || "",
    };

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/home_page/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);

    router.push({ name: 'HomePage' });
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
