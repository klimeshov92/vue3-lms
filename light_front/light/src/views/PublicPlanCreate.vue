<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание плана</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">
        
        <div class="form-field">
          <label for="avatar" class="form-label">Аватар:</label>
          <input type="file" id="avatar" @change="onFileChange" class="form-input" />
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
          <label class="form-label">Шаблон задачи:</label>
          <multiselect
            v-model="form.task_template"
            :options="task_templates"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите шаблон задачи"
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
          <span v-if="errors.task_template" class="error">{{ errors.task_template }}</span>
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
import EditorComponent from '../components/EditorComponent.vue';

const route = useRoute();
const router = useRouter();

const form = reactive({
  task_template: null,
  name: '',
  desc: '',
  categories: [],
});

const loading = ref(false);

const task_templates = ref([]);
const loadTaskTemplate = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/task_templates/`, {
      headers: { Authorization: `Bearer ${token}` },
      params: {
        task_type: 'plan_implementation',
      },
    });
    task_templates.value = response.data.results || [];
    console.log('Шаблоны задач загружены:', task_templates.value);
  } catch (error) {
    console.error('Ошибка при загрузке шаблонов задач:', error.response ? error.response.data : error.message);
  }
};

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

const avatarFile = ref(null);
const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    avatarFile.value = file;
  }
};

const cancelEdit = () => {
  router.push({ name: 'PublicPlanList' });
};

const errors = reactive({});
const validateForm = () => {
  errors.task_template = form.task_template ? '' : 'Выбор шаблона задачи обязателен!';
  errors.name = form.name ? '' : 'Название обязательно!';
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
      task_template: form.task_template?.id,
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

    const jsonResponse = await axios.post(`${baseUrl}/public_plans/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);

    if (avatarFile.value) {
      const avatarFormData = new FormData();
      avatarFormData.append('avatar', avatarFile.value);

      const avatarPatchUrl = `${baseUrl}/public_plans/${jsonResponse.data.id}/`;
      const avatarPatchResponse = await axios.patch(avatarPatchUrl, avatarFormData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Аватар успешно обновлен:', avatarPatchResponse.data);
    }

    router.push({ name: 'PublicPlanDetail', params: { id: jsonResponse.data.id }  });
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
    await loadTaskTemplate();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
