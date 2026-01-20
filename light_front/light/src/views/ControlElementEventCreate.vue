<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание события</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">

        <div class="form-field">
          <label class="form-label">Управляющий элемент:</label>
          <multiselect
            v-model="form.control_element"
            :options="control_elements"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите управляющий элемент"
            label="str"
            track-by="id"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
            :disabled="!!control_elementId"
          >
            <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
          <span v-if="errors.control_element" class="error">{{ errors.control_element }}</span>
        </div>

        <div class="form-field">
          <label class="form-label">Событие:</label>
          <multiselect
            v-model="form.event_type"
            :options="event_types"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите тип задачи"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.event_type" class="error">{{ errors.event_type }}</span>
        </div>

        <div v-if="
          form.event_type.value == 'task_created' || 
          form.event_type.value == 'child_task_status_changed' || 
          form.event_type.value == 'task_deadline' || 
          form.event_type.value == 'task_status_changed' || 
          form.event_type.value == 'task_outcome_changed' ||
          form.event_type.value == 'periodic_event'
        " class="form-field">
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

        <div v-if="form.event_type.value == 'trigger_fired'" class="form-field">
          <label class="form-label">Сработавший триггер:</label>
          <multiselect
            v-model="form.fired_trigger"
            :options="control_elements"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите управляющий элемент"
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
          <span v-if="errors.fired_trigger" class="error">{{ errors.fired_trigger }}</span>
        </div>

        <div v-if="form.event_type.value == 'periodic_event'" class="form-field">
          <label class="form-label">Период:</label>
          <multiselect
            v-model="form.period"
            :options="periods"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите период"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.period" class="error">{{ errors.period }}</span>
        </div>

        <div v-if="form.event_type.value == 'periodic_event'" class="form-field">
          <label for="start_time" class="form-label">Начало по плану:</label>
          <input 
            v-model="form.start_time" 
            id="start_time" 
            type="datetime-local" 
            class="form-input"
          />
          <span v-if="errors.start_time" class="error">{{ errors.start_time }}</span>
        </div>

      </form>

      <div class="form-menu button-group">
        <button type="submit" class="button" form="form">Сохранить</button>
        <button type="button" @click="cancelEdit" class="button">Отмена</button>
      </div>
    </div>

  </div>

</template>

<script setup>
import { reactive, onMounted, ref, watch, computed  } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid } from '../utils/utils';

const router = useRouter();
const route = useRoute();

const loading = ref(false);

const event_types = [
  //{ label: 'Клиент создан', value: 'client_created' },
  //{ label: 'Аккаунт создан', value: 'account_created' },
  //{ label: 'Задача создана', value: 'task_created' },
  { label: 'Изменился статус дочерней задачи', value: 'child_task_status_changed' },
  { label: 'Истек срок задачи', value: 'task_deadline' },
  { label: 'Изменился статус задачи', value: 'task_status_changed' },
  { label: 'Изменился итог задачи', value: 'task_outcome_changed' },
  { label: 'Сработал триггер', value: 'trigger_fired' },
  { label: 'Периодическое событие', value: 'periodic_event' },
];

const periods = [
  { label: 'Ежедневно', value: 'daily' },
  { label: 'Еженедельно', value: 'weekly' },
  { label: 'Ежемесячно', value: 'monthly' },
];

const form = reactive({
  control_element: null,
  event_type: '',
  task_template: null,
  fired_trigger: null,
  period: '',
  start_time: null,
});
const errors = reactive({});

const control_elements = ref([]);
const loadControlElements = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/control_elements/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    control_elements.value = response.data.results || [];
    console.log('Управлябщие элементы загружены:', control_elements.value);
  } catch (error) {
    console.error('Ошибка при загрузке управлябщих элементов:', error.response ? error.response.data : error.message);
  }
};

const control_elementId = route.query.control_elementId || '';

const loadControlElementById = () => {
  if (control_elementId) {
    console.log('ControlElement ID:', control_elementId);
    const control_element = control_elements.value.find(control_element => control_element.id === parseInt(control_elementId, 10));
    if (control_element) {
      form.control_element = control_element;
    } else {
      console.error('ControlElement не найден.');
    }
  } else {
    console.log('ControlElement ID не найден.');
  }
};

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
    });
    task_templates.value = response.data.results || [];
    console.log('Шаблоны задач загружены:', task_templates.value);
  } catch (error) {
    console.error('Ошибка при загрузке шаблонов задач:', error.response ? error.response.data : error.message);
  }
};

watch(
  () => form.event_type,
  (newValue) => {
    if (
    newValue.value != 'task_created'
    && newValue.value != 'child_task_status_changed'
    && newValue.value != 'task_deadline'
    && newValue.value != 'task_status_changed'
    && newValue.value != 'task_outcome_changed'
    && newValue.value != 'periodic_event'
    ) {
      form.task_template = null;
    }
    if (newValue.value != 'trigger_fired') {
      form.fired_trigger = null;
    }
    if (newValue.value != 'periodic_event') {
      form.period = '';
      form.start_time = null;
    }
  }
);

const validateForm = () => {
  errors.control_element = form.control_element ? '' : 'Управляющий элемент обязателен';
  errors.event_type = form.event_type.value ? '' : 'Cобытие обязательно!';
  if (
    form.event_type == 'task_created' || 
    form.event_type == 'child_task_status_changed' ||
    form.event_type == 'task_deadline' ||
    form.event_type == 'task_status_changed' ||
    form.event_type == 'task_outcome_changed' ||
    form.event_type == 'periodic_event'
  ) {
    errors.task_template = form.task_template ? '' : 'Шаблон задачи обязателен!';
  }
  if (form.event_type == 'trigger_fired') {
    errors.fired_trigger = form.fired_trigger ? '' : 'Управляющий элемент обязателен!';
  }
  if (form.event_type == 'periodic_event') {
    errors.period = form.period.value ? '' : 'Период обязателен!';
    errors.start_time = form.start_time ? '' : 'Выбор начала обязателен';
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
      control_element: form.control_element.id,
      event_type: form.event_type.value,
      task_template: form.task_template?.id || null,
      fired_trigger: form.fired_trigger?.id || null,
      period: form.period?.value || '',
      start_time: form.start_time,
    };
    const control_elementId = form.control_element.id

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/control_element_events/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);
    router.push({ name: 'ControlElementDetail', params: { id: control_elementId }  });
  } catch (error) {
    if (error.response && error.response.data) {
      Object.assign(errors, error.response.data);
      console.error('Ошибка при создании объекта:', error.response.data);
    } else {
      console.error('Ошибка при создании объекта:', error.message);
    }
  }
};

const cancelEdit = () => {
  const control_elementId = form.control_element.id
  router.push({ name: 'ControlElementDetail', params: { id: control_elementId } });
};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await loadControlElements();
    await loadControlElementById();
    await loadTaskTemplate();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>
/* Добавьте стили при необходимости */
</style>
