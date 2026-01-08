<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание файла</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">
        
        <div class="form-field">
          <label for="upload_file" class="form-label">Загружаемый файл:</label>
          <input type="file" id="upload_file" @change="onFileChange" class="form-input" />
          <span v-if="errors.upload_file" class="error">{{ errors.upload_file }}</span>
        </div>

        <div class="form-field">
          <label class="form-label">Тип файла:</label>
          <multiselect
            v-model="form.file_type"
            :options="file_types"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите тип файла"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.file_type" class="error">{{ errors.file_type }}</span>
        </div>
        
        <div class="form-field">
          <label class="form-label">Категории:</label>
          <multiselect
            v-model="form.categories"
            :options="categories"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите категории"
            label="name"
            track-by="id"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          >
            <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
        </div>

        <div class="form-field">
          <label for="name" class="form-label">Название:</label>
          <input v-model="form.name" id="name" type="text" class="form-input" placeholder="Введите название" required />
          <span v-if="errors.name" class="error">{{ errors.name }}</span>
        </div>

        <div class="form-field">
          <label for="desc" class="form-label">Описание:</label>
          <textarea v-model="form.desc" id="desc" class="form-input" rows="3" placeholder="Введите описание" ></textarea>
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

const route = useRoute();
const router = useRouter();

const form = reactive({
  file_type: '',
  name: '',
  desc: '',
  categories: [],
});

const loading = ref(false);

const file_types = [
  { label: 'Картинка', value: 'image' },
  { label: 'Видео', value: 'video' },
  { label: 'Аудио', value: 'audio' },
  { label: 'Документ', value: 'document' },
];

const categories = ref([]);
const loadCategories = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/categories/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    categories.value = response.data.results || [];
    console.log('Категории загружены:', categories.value);
  } catch (error) {
    console.error('Ошибка при загрузке категорий:', error.response ? error.response.data : error.message);
  }
};

const uploadFile = ref(null);
const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    uploadFile.value = file;
    console.log('Проверка файла:', uploadFile.value);
  }
};

const cancelEdit = () => {
  router.push({ name: 'FileList' });
};

const errors = reactive({});
const validateForm = () => {
  errors.file_type = form.file_type.value ? '' : 'Тип файла обязателен!';
  errors.name = form.name ? '' : 'Название обязательно!';
  errors.upload_file = uploadFile.value ? '' : 'Загружаемый файл обязателен!';
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
      file_type: form.file_type.value,
      name: form.name,
      desc: form.desc,
      categories: form.categories.map(item => item.id),
    };

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/files/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);
    
    if (uploadFile.value) {
      const fileFormData = new FormData();
      fileFormData.append('upload_file', uploadFile.value);

      const filePatchUrl = `${baseUrl}/files/${jsonResponse.data.id}/`;
      const filePatchResponse = await axios.patch(filePatchUrl, fileFormData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Файл успешно обновлен:', filePatchResponse.data);
    }

    router.push({ name: 'FileDetail', params: { id: jsonResponse.data.id }  });
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
    await loadCategories();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
