<template>

  <div v-if="loading">

    <div v-if="object" class="form-page">

      <div class="form-header">
        <h1>Редактирование страницы</h1>
      </div>

      <form @submit.prevent="saveChanges" class="form" id="edit-form">

        <div class="form-field">
          <label for="title" class="form-label">Заголовок:</label>
          <input v-model="form.title" id="title" type="text" class="form-input" placeholder="Введите заголовок" required />
          <span v-if="errors.title" class="error">{{ errors.title }}</span>
        </div>

        <div lass="form-field form-field-full_width">
          <label for="content" class="form-label">Содержание:</label>
          
          <EditorComponent v-model="form.content" />

          <span v-if="errors.content" class="error">{{ errors.content }}</span>
        </div>

      </form>

      <div class="form-menu button-group">
        <button type="submit" class="button" form="edit-form">Сохранить</button>
        <button type="button" @click="cancelEdit" class="button">Отмена</button>
      </div>
    </div>

    <div v-else class="none-card">
      <div>Объект не найден</div>
    </div>

  </div>

  <div v-else class="loading">
    <div>Загрузка данных...</div>
  </div>

</template>

<script setup>

import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid , goBackSmart } from '../utils/utils';
import EditorComponent from '../components/EditorComponent.vue';

const route = useRoute();
const router = useRouter();

const object = ref(null);
const form = reactive({
  title: '',
  content: '',
});

const loading = ref(false);

const fetchObject = async () => {
  const id = route.params.id;
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/legal_page/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    object.value = response.data;
    console.log(`Объект успешно загружен:`, object.value);
    Object.assign(form, object.value);

  } catch (error) {
    console.error('Ошибка загрузки объекта:', error.response?.data || error.message);
  }
};

const errors = reactive({});
const validateForm = () => {
  errors.title = form.title ? '' : 'Название обязательно!';
  errors.content = form.content.trim() ? '' : 'Содержание обязательно!';
  return Object.values(errors).every((err) => !err);
};

const saveChanges = async () => {
  if (!validateForm()) {
    console.error('Форма содержит ошибки:', errors);
    return;
  }

  try {
    const id = route.params.id;
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonData = {
      title: form.title,
      content: form.content || "",
    };

    console.log('JSON данные перед отправкой:', jsonData);

    await axios.patch(`${baseUrl}/legal_page/${id}/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Данные обновлены');

    router.push({ name: 'LegalPage' });
  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при сохранении изменений:', error.response.data);
    } else {
      console.error('Ошибка при сохранении изменений:', error.message);
    }
  }
};

const cancelEdit = () => {
  goBackSmart(router);
};


onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await fetchObject();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>
