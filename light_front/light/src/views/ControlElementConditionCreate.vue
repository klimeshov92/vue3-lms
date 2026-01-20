<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание условия</h1>
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
          <label for="item" class="form-label">Пункт:</label>
          <input v-model="form.item" id="item" type="number" class="form-input" placeholder="Введите пункт" />
          <span v-if="errors.item" class="error">{{ errors.item }}</span>
        </div>

        <div class="form-field">
          <label class="form-label">Логический оператор:</label>
          <multiselect
            v-model="form.logic_operator"
            :options="logic_operators"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите логический оператор"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
            :disabled="form.item == 1" 
          />
          <span v-if="errors.logic_operator" class="error">{{ errors.logic_operator }}</span>
        </div>

        <div class="form-field">
          <label class="form-label">Условие:</label>
          <multiselect
            v-model="form.condition_type"
            :options="condition_types"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите условие"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.condition_type" class="error">{{ errors.condition_type }}</span>
        </div>

        <div class="form-field" v-if="form.condition_type?.value == 'task_exists' || form.condition_type?.value == 'child_tasks_status' || form.condition_type?.value == 'task_status' || form.condition_type?.value == 'task_outcome'">
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

        <div class="form-field" v-if="form.condition_type?.value == 'task_exists' || form.condition_type?.value == 'child_tasks_status' || form.condition_type?.value == 'task_status' || form.condition_type?.value == 'task_outcome'">
          <label class="form-label">Целевая задача:</label>
          <multiselect
            v-model="form.target_task"
            :options="target_tasks"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите целевую задачу"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.target_task" class="error">{{ errors.target_task }}</span>
        </div>

        <div class="form-field"  v-if="form.condition_type?.value == 'task_exists'">
          <label for="boolean_operator" class="form-label">Оператор сравнения:</label>
          <input v-model="form.boolean_operator" id="boolean_operator" type="checkbox" class="form-input" />
        </div>

        <div class="form-field" v-if="form.condition_type?.value == 'child_tasks_status' || form.condition_type?.value == 'task_status' || form.condition_type?.value == 'task_outcome'">
          <label class="form-label">Оператор сравнения:</label>
          <multiselect
            v-model="form.comparison_operator"
            :options="comparison_operators"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите оператор сравнения"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.comparison_operator" class="error">{{ errors.comparison_operator }}</span>
        </div>

        <div v-if="form.condition_type?.value == 'child_tasks_status' || form.condition_type?.value == 'task_status'" class="form-field">
          <label class="form-label">Статус задачи:</label>
          <multiselect
            v-model="form.task_status"
            :options="task_statuses"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите статус задачи"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.task_status" class="error">{{ errors.task_status }}</span>
        </div>

        <div v-if="form.condition_type?.value == 'task_outcome'" class="form-field">
          <label class="form-label">Итог задачи:</label>
          <multiselect
            v-model="form.task_outcome"
            :options="task_outcomes"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите итог задачи"
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
          <span v-if="errors.task_outcome" class="error">{{ errors.task_outcome }}</span>
        </div>

        <div class="form-field" v-if="form.condition_type?.value == 'days_worked'">
          <label class="form-label">Оператор сравнения:</label>
          <multiselect
            v-model="form.order_operator"
            :options="order_operators"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите оператор сравнения"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.order_operator" class="error">{{ errors.order_operator }}</span>
        </div>

        <div v-if="form.condition_type?.value == 'days_worked'" class="form-field">
          <label for="days_worked" class="form-label">Дни стажа:</label>
          <input v-model="form.days_worked" id="days_worked" type="number" class="form-input" placeholder="Введите пункт" />
          <span v-if="errors.days_worked" class="error">{{ errors.days_worked }}</span>
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

const logic_operators = [
  { label: 'И', value: 'and' },
  { label: 'ИЛИ', value: 'or' },
];

const condition_types = [
  { label: 'Задача назначалась', value: 'task_exists' },
  { label: 'Статус дочерних задач', value: 'child_tasks_status' },
  { label: 'Статус задачи', value: 'task_status' },
  { label: 'Итог задачи', value: 'task_outcome' },
  { label: 'Стаж аккаунта взаимодействия', value: 'days_worked' },
];

const comparison_operators = [
  { label: 'Равно', value: 'equal' },
  { label: 'Не равно', value: 'not_equal' },
];

const order_operators = [
  { label: 'Больше или равно', value: 'gte' },
  { label: 'Меньше или равно', value: 'lte' },
];

const task_statuses = [
  { label: 'В ожидании', value: 'waiting' },
  { label: 'Назначена', value: 'assigned' },
  { label: 'В процессе', value: 'in_progress' },
  { label: 'На проверке', value: 'under_review' },
  { label: 'Выполнена', value: 'completed' },
  { label: 'Провалена', value: 'failed' },
  { label: 'Отменена', value: 'canceled' },
];

const target_tasks = [
  { label: 'В рамках текущего взаимодействия', value: 'current' },
  { label: 'В рамках всех взаимодействий', value: 'all' },
];

const form = reactive({
  control_element: null,
  item: null,
  logic_operator: '',
  condition_type: '',
  task_template: null,
  boolean_operator: false,
  comparison_operator: '',
  order_operator: '',
  task_status: '',
  task_outcome: null,
  target_task: '',
  days_worked: null,
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

const task_outcomes = computed(() => {
  if (control_elements) {
    return control_elements.value.filter(
      control_element => control_element.type_of_work === 'task_outcome'
    );
  }
});

watch(
  () => form.condition_type,
  (newValue) => {
    if (newValue.value != 'task_exists') {
      form.task_template = null;
      form.target_task = '';
      form.boolean_operator =  false;
    }
    if (newValue.value != 'child_tasks_status' && newValue.value != 'task_status' && newValue.value != 'task_outcome') {
      form.task_template = null;
      form.comparison_operator = '';
      form.target_task = '';
    }
    if (newValue.value != 'child_tasks_status' && newValue.value != 'task_status') {
      form.task_status = '';
    }
    if (newValue.value != 'task_outcome') {
      form.task_outcome = null;
    }
    if (newValue.value != 'days_worked') {
      form.order_operator = null;
      form.days_worked = null;
    }
  }
);

watch(
  () => form.item,
  (newValue) => {
    if (newValue == 1) {
      form.logic_operator = null;
    }
  }
);

const validateForm = () => {
  errors.control_element = form.control_element ? '' : 'Управляющий элемент обязателен';
  errors.condition_type = form.condition_type.value ? '' : 'Условие обязательно!';
  errors.item = form.item && form.item > 0 ? '' : 'Пункт обязателен и должен быть больше 0!';
  if (form.item != 1) {
    errors.logic_operator = form.logic_operator.value ? '' : 'Логический оператор обязателен!';
  }
  if (form.condition_type == 'task_exists') {
    errors.task_template = form.task_template ? '' : 'Шаблон задачи обязателен!';
    errors.target_task = form.target_task.value ? '' : 'Целевая задача обязательна!';
  }
  if (form.condition_type == 'child_tasks_status' || form.condition_type == 'task_status') {
    errors.task_template = form.task_template ? '' : 'Шаблон задачи обязателен!';
    errors.task_status = form.task_status.value ? '' : 'Статус задачи обязателен!';
    errors.comparison_operator = form.comparison_operator.value ? '' : 'Оператор сравнения обязателен!';
    errors.target_task = form.target_task.value ? '' : 'Целевая задача обязательна!';
  }
  if (form.condition_type == 'task_outcome') {
    errors.task_template = form.task_template ? '' : 'Шаблон задачи обязателен!';
    errors.task_outcome = form.task_outcome ? '' : 'Итог задачи обязателен!';
    errors.comparison_operator = form.comparison_operator.value ? '' : 'Оператор сравнения обязателен!';
    errors.target_task = form.target_task.value ? '' : 'Целевая задача обязательна!';
  }
  if (form.condition_type == 'days_worked') {
    errors.order_operator = form.order_operator.value ? '' : 'Оператор сравнения обязателен!';
    errors.days_worked = form.days_worked ? '' : 'Дни стажа обязательны!';
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
      item: form.item,
      logic_operator: form.logic_operator?.value || '',
      boolean_operator: form.boolean_operator,
      condition_type: form.condition_type.value,
      task_template: form.task_template?.id || null,
      comparison_operator: form.comparison_operator?.value || '',
      order_operator: form.order_operator?.value || '',
      task_status: form.task_status?.value || '',
      task_outcome: form.task_outcome?.id || null,
      target_task: form.target_task?.value || '',
      days_worked: form.days_worked,  
    };
    const control_elementId = form.control_element.id

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/control_element_conditions/`, jsonData, {
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
    await loadTaskTemplates();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>
/* Добавьте стили при необходимости */
</style>
