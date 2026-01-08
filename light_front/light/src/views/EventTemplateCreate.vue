<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание мероприятия</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">
        
        <div class="form-field">
          <label for="avatar" class="form-label">Аватар:</label>
          <input type="file" id="avatar" @change="onFileChange" class="form-input" />
        </div>

        <div class="form-field">
          <label class="form-label">Формат:</label>
          <multiselect
            v-model="form.format"
            :options="formats"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите формат"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.format" class="error">{{ errors.format }}</span>
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

        <div v-if="form.format?.value == 'face_to_face' || form.format?.value == 'mixed'" class="form-field">
          <label for="location" class="form-label">Локация:</label>
          <textarea v-model="form.location" id="location" class="form-input" rows="3" placeholder="Введите описание" ></textarea>
          <span v-if="errors.location" class="error">{{ errors.location }}</span>
        </div>

        <div v-if="form.format?.value == 'webinar' || form.format?.value == 'mixed'" class="form-field">
          <label for="link" class="form-label">Ссылка:</label>
          <textarea v-model="form.link" id="link" class="form-input" rows="3" placeholder="Введите описание" ></textarea>
          <span v-if="errors.link" class="error">{{ errors.link }}</span>
        </div>

        <div class="form-field">
          <label class="form-label">Ведущие:</label>
          <multiselect
            v-model="form.admins"
            :options="accounts"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите админов"
            label="str"
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
          <span v-if="errors.admins" class="error">{{ errors.admins }}</span>
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
import { reactive, onMounted, ref, watch } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid } from '../utils/utils';
import EditorComponent from '../components/EditorComponent.vue';

const route = useRoute();
const router = useRouter();

const form = reactive({
  format: '',
  categories: [],
  name: '',
  link: '',
  location: '',
  admins: [],
  desc: '',
});

const loading = ref(false);

const formats = [
  { label: 'Очное мероприятие', value: 'face_to_face' },
  { label: 'Вебинар', value: 'webinar' },
  { label: 'Смешанный формат', value: 'mixed' },
];

const term_types = [
  { label: 'Минуты', value: 'minutes' },
  { label: 'Часы', value: 'hours' },
  { label: 'Дни', value: 'days' },
  { label: 'Без срока', value: 'none' },
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

const accounts = ref([]);
const loadAccounts = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/accounts/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    accounts.value = response.data.results || [];
    console.log('Аккаунты загружены:', accounts.value);
  } catch (error) {
    console.error('Ошибка при загрузке сотрудников:', error.response ? error.response.data : error.message);
  }
};

const avatarFile = ref(null);
const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    avatarFile.value = file;
  }
};

const cancelEdit = () => {
  router.push({ name: 'EventTemplateList' });
};

watch(
  () => form.format,
  (newValue) => {
    if (newValue.value != 'face_to_face' && newValue.value != 'mixed') {
      form.location = null;
    }
    if (newValue.value != 'webinar' && newValue.value != 'mixed') {
      form.link = null;
    }
  }
);

const errors = reactive({});
const validateForm = () => {
  errors.format = form.format.value ? '' : 'Формат обязателен!';
  if (form.format.value == 'face_to_face') {
    errors.location = form.location ? '' : 'Локация обязательна!';
  }
  if (form.format.value == 'webinar') {
    errors.link = form.link ? '' : 'Ссылка обязательна!';
  }
  if (form.format.value == 'mixed') {
    errors.link = form.link ? '' : 'Ссылка обязательна!';
    errors.location = form.location ? '' : 'Локация обязательна!';
  }
  errors.name = form.name ? '' : 'Название обязательно!';
  errors.admins = form.admins && form.admins.length > 0 ? '' : 'Ведущие обязательны!';
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
      format: form.format.value,
      categories: form.categories.map(item => item.id),
      name: form.name,
      link: form.link,
      location: form.location,
      admins: form.admins.map(item => item.id),
      desc: form.desc,
    };

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/event_templates/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);

    if (avatarFile.value) {
      const avatarFormData = new FormData();
      avatarFormData.append('avatar', avatarFile.value);

      const avatarPatchUrl = `${baseUrl}/event_templates/${jsonResponse.data.id}/`;
      const avatarPatchResponse = await axios.patch(avatarPatchUrl, avatarFormData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Аватар успешно обновлен:', avatarPatchResponse.data);
    }

    router.push({ name: 'EventTemplateDetail', params: { id: jsonResponse.data.id }  });
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
    await loadAccounts();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
