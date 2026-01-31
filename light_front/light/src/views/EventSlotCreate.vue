<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание слота мероприятия</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">
        
        <div class="form-field">
          <label class="form-label">Мероприятие:</label>
          <multiselect
            v-model="form.event_template"
            :options="event_templates"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите мероприятие"
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
          <span v-if="errors.event_template" class="error">{{ errors.event_template }}</span>
        </div>

        <div class="form-field">
          <label for="number_of_participants" class="form-label">Количество участников:</label>
          <input v-model="form.number_of_participants" id="number_of_participants" type="number" class="form-input" placeholder="Введите количество участников" />
          <span v-if="errors.number_of_participants" class="error">{{ errors.number_of_participants }}</span>
        </div>

        <div class="form-field">
          <label for="registration" class="form-label">Регистрация открыта:</label>
          <input v-model="form.registration" id="registration" type="checkbox" class="form-input" />
        </div>

        <div class="form-field">
          <label for="planned_start" class="form-label">Начало по плану:</label>
          <input v-model="form.planned_start" id="planned_start" type="datetime-local" class="form-input" />
          <span v-if="errors.planned_start" class="error">{{ errors.planned_start }}</span>
        </div>

        <div class="form-field">
          <label for="deadline" class="form-label">Сроки:</label>
          <input v-model="form.deadline" id="deadline" type="checkbox" class="form-input" />
        </div>
        
        <div v-if="form.deadline" class="form-field">
          <label for="planned_end" class="form-label">Завершение по плану:</label>
          <input v-model="form.planned_end" id="planned_end" type="datetime-local" class="form-input" />
          <span v-if="errors.planned_end" class="error">{{ errors.planned_end }}</span>
        </div>

        <div class="form-field">
          <label for="desc" class="form-label">Описание:</label>
          <textarea v-model="form.desc" id="desc" class="form-input" rows="3" placeholder="Введите описание" ></textarea>
        </div>

        <div class="form-field">
          <label class="form-label">Статус:</label>
          <multiselect
            v-model="form.status"
            :options="statuses"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите статус"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.status" class="error">{{ errors.status }}</span>
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
import { baseUrl, isTokenValid , goBackSmart } from '../utils/utils';
import EditorComponent from '../components/EditorComponent.vue';

const route = useRoute();
const router = useRouter();

const form = reactive({
  event_template: null,
  number_of_participants: null,
  registration: false,
  deadline: false,
  planned_start: null,
  planned_end: null,
  desc: '',
  status: '',
});

const loading = ref(false);

const statuses = [
  { label: 'Планируется', value: 'planned' },
  { label: 'В процессе', value: 'in_progress' },
  { label: 'Отменено', value: 'canceled' },
  { label: 'Завершено', value: 'completed' },
];

const event_templates = ref([]);
const loadEventTemplates = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/event_templates/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    event_templates.value = response.data.results || [];
    console.log('Мероприятия загружены:', event_templates.value);
  } catch (error) {
    console.error('Ошибка при загрузке мероприятий:', error.response ? error.response.data : error.message);
  }
};

const cancelEdit = () => {
  goBackSmart(router);
};

watch(
  () => form.deadline,
  (newValue) => {
    if (newValue == false) {
      form.planned_end = null;
    }
  }
);

const errors = reactive({});
const validateForm = () => {
  errors.event_template = form.event_template ? '' : 'Мероприятие обязательно!';
  errors.number_of_participants = form.number_of_participants ? null : 'Название обязательно!';
  errors.planned_start = form.planned_start ? '' : 'Выбор начала обязателен';
  if (form.deadline) {
    errors.planned_end = form.planned_end ? '' : 'Выбор завершения обязателен';
  }
  errors.status = form.status.value ? '' : 'Статус задачи обязателен!';
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
      event_template: form.event_template.id,
      number_of_participants: form.number_of_participants,
      registration: form.registration,
      deadline: form.deadline,
      planned_start: form.planned_start,
      planned_end: form.planned_end,
      desc: form.desc,
      status: form.status.value,
    };

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/event_slots/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);

    localStorage.removeItem('userPermissions');

    router.push({ name: 'EventSlotDetail', params: { id: jsonResponse.data.id }  });
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
    await loadEventTemplates();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
