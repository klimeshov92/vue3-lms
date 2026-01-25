<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание управляющих элементов</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">

        <div class="form-field">
          <label class="form-label">Тип работы:</label>
          <multiselect
            v-model="form.type_of_work"
            :options="type_of_works"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите тип работы"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
            :disabled="!!taskId"
          />
          <span v-if="errors.type_of_work" class="error">{{ errors.type_of_work }}</span>
        </div>

        <div class="form-field">
          <label for="repeat" class="form-label">Многократное срабатывание:</label>
          <input v-model="form.repeat" id="repeat" type="checkbox" class="form-input" />
        </div>

        <div v-if="form.type_of_work.value == 'task_outcome'" class="form-field">
          <label class="form-label">Шаблон задачи:</label>
          <multiselect
            v-model="form.task_template"
            :options="filteredTaskTemplates"
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
            :disabled="!!taskId"
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
import { reactive, onMounted, ref, watch, computed } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const form = reactive({
  type_of_work: '',
  repeat: false,
  task_template: null,
  name: '',
  categories: [],
  desc: '',
});

const loading = ref(false);

const type_of_works = [
  { label: 'Итог задачи', value: 'task_outcome' },
  { label: 'Триггер', value: 'trigger' },
];

const task_templates = ref([]);
const loadTaskTemplates = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/task_templates/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    task_templates.value = response.data.results || [];
    console.log('Шаблоны задач загружены:', task_templates.value);
  } catch (error) {
    console.error('Ошибка при загрузке шаблонов задач:', error.response ? error.response.data : error.message);
  }
};

const taskId = route.query.taskId || '';
const loadTaskById = () => {
  if (taskId) {
    console.log('Task ID:', taskId);
    const task = task_templates.value.find(task => task.id === parseInt(taskId, 10));
    if (task) {
      form.type_of_work = type_of_works.find(option => option.value === 'task_outcome');
      form.task_template = task;
    } else {
      console.error('Task не найден.');
    }
  } else {
    console.log('Task ID не найден.');
  }
};

const filteredTaskTemplates = computed(() => {
  if (form.type_of_work?.value === 'task_outcome') {
    return task_templates.value.filter(
      task_template => task_template.task_outcome == true
    );
  }
  return task_templates.value;
});

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

watch(
  () => form.type_of_work,
  (newValue) => {
    if (newValue.value != 'task_outcome') {
      form.task_outcome = null;
    }
  }
);

const cancelEdit = () => {
  const taskId = route.query.taskId || '';
    if (taskId){
      router.push({ name: 'TaskTemplateDetail', params: { id: taskId }  });
    } else {
      router.push({ name: 'ControlElementList' });
    }
};

const errors = reactive({});
const validateForm = () => {
  errors.type_of_work = form.type_of_work.value ? '' : 'Тип работы обязателен!';
  if (form.type_of_work.value == 'task_outcome') {
    errors.task_template = form.task_template ? '' : 'Выбор шаблона задачи обязателен!';
  }
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
      type_of_work: form.type_of_work.value,
      repeat: form.repeat,
      task_template: form.task_template?.id,
      name: form.name,
      categories: form.categories.map(item => item.id),
      desc: form.desc,
    };

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/control_elements/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);

    localStorage.removeItem('userPermissions');

    const taskId = route.query.taskId || '';
    if (taskId){
      router.push({ name: 'TaskTemplateDetail', params: { id: taskId }  });
    } else {
      router.push({ name: 'ControlElementDetail', params: { id: jsonResponse.data.id }  });
    }
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
    await loadTaskTemplates();
    await loadTaskById();
    await loadCategories();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
