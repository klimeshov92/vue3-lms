<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание назначения шаблона задачи</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">

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
          <label class="form-label">Тип взаимодействия:</label>
          <multiselect
            v-model="form.interaction_type"
            :options="interaction_types"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите тип взаимодействия"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.interaction_type" class="error">{{ errors.interaction_type }}</span>
        </div>

        <div v-if="form.task_template && form.interaction_type?.value == 'selected'" class="form-field">
          <label class="form-label">Взаимодействие:</label>
          <multiselect
            v-model="form.interaction"
            :options="interactions"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите взаимодействие"
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
          <span v-if="errors.interaction" class="error">{{ errors.interaction }}</span>
        </div>

        <div class="form-field">
          <label for="planned_start" class="form-label">Начало по плану:</label>
          <input v-model="form.planned_start" id="planned_start" type="datetime-local" class="form-input" />
          <span v-if="errors.planned_start" class="error">{{ errors.planned_start }}</span>
        </div>

        <div class="form-field">
          <label class="form-label">Тип исполнителя:</label>
          <multiselect
            v-model="form.executor_type"
            :options="executor_types"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите тип исполнителя"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.executor_type" class="error">{{ errors.executor_type }}</span>
        </div>

        <div v-if="form.executor_type?.value == 'selected'" class="form-field">
          <label class="form-label">Исполнитель:</label>
          <multiselect
            v-model="form.executor"
            :options="accounts"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите исполнителя"
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
          <span v-if="errors.executor" class="error">{{ errors.executor }}</span>
        </div>

        <div v-if="form.executor_type?.value == 'group'" class="form-field">
          <label class="form-label">Группа исполнителей:</label>
          <multiselect
            v-model="form.executor_group"
            :options="groups"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите группу исполнителей"
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
          <span v-if="errors.executor_group" class="error">{{ errors.executor_group }}</span>
        </div>

        <div class="form-field">
          <label for="manager_control" class="form-label">Контроль руководителей:</label>
          <input v-model="form.manager_control" id="manager_control" type="checkbox" class="form-input" />
        </div>

        <div class="form-field">
          <label class="form-label">Группа контролеров:</label>
          <multiselect
            v-model="form.controller_group"
            :options="groups"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите группу контролеров"
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
        </div>

        <div class="form-field">
          <label class="form-label">Группа наблюдателей:</label>
          <multiselect
            v-model="form.observer_group"
            :options="groups"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите группу наблюдателей"
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
import { reactive, onMounted, ref, watch, computed } from 'vue';
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
  interaction_type: '',
  interaction: null,
  executor_type: '',
  executor: null,
  executor_group: null,
  manager_control: false,
  controller_group: null,
  observer_group: null,
  planned_start: null,
  name: '',
  desc: '',
  categories: [],
});

const loading = ref(false);

const executor_types = [
  { label: 'Выбранному исполнителю', value: 'selected' },
  { label: 'Группе исполнителей', value: 'group' },
  { label: 'Без исполнителей', value: 'none' },
];

const interaction_types = [
  { label: 'Выбранное взаимодействие', value: 'selected' },
  { label: 'Последнее взаимодействие исполнителя', value: 'last' },
  { label: 'Новое взаимодействие исполнителя', value: 'new' },
];

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
    task_templates.value = (response.data.results || []).filter(
      task_template => !task_template.is_child
    );
    console.log('Шаблоны задач загружены:', task_templates.value);
  } catch (error) {
    console.error('Ошибка при загрузке шаблонов задач:', error.response ? error.response.data : error.message);
  }
};

const interactions = ref([]);
const loadInteractions = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/interactions/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    interactions.value = response.data.results || [];
    console.log('Взаимодействия загружены:', interactions.value);
  } catch (error) {
    console.error('Ошибка при загрузке взимодействий:', error.response ? error.response.data : error.message);
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

const groups = ref([]);
const loadGroups = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/account_groups/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    groups.value = response.data.results || [];
    console.log('Группы загружены:', groups.value);
  } catch (error) {
    console.error('Ошибка при загрузке групп:', error.response ? error.response.data : error.message);
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

watch(
  () => form.task_template,
  (newValue, oldValue) => {
    if (newValue && oldValue) {
      form.interaction = null;
    }
    if (newValue == null) {
      form.interaction = null;
    }
  }
);

watch(
  () => form.interaction_type,
  (newValue) => {
    if (newValue.value != 'selected') {
      form.interaction = null;
    }
  }
);

const cancelEdit = () => {
  router.push({ name: 'TaskTemplateAssignmentList' });
};

const errors = reactive({});
const validateForm = () => {
  errors.task_template = form.task_template ? '' : 'Выбор шаблона задачи обязателен!';
  errors.interaction_type = form.interaction_type.value ? '' : 'Тип взаимодействий обязателен!';
  if (form.interaction_type?.value == 'selected') {
      errors.interaction = form.interaction ? '' : 'Выбор взаимодейтсвия обязателен!';
  }
  if (form.task_template?.term_type != 'none') {
    errors.planned_start = form.planned_start ? '' : 'Выбор начала обязателен';
  }
  errors.executor_type = form.executor_type.value ? '' : 'Тип исполнителя обязателен!';
  if (form.executor_type?.value == 'selected') {
    errors.executor = form.executor ? '' : 'Выбор исполнителя обязателен!';
  }
  if (form.executor_type?.value == 'group') {
    errors.executor = form.executor_group ? '' : 'Выбор исполнителя обязателен!';
  }
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
      interaction_type: form.interaction_type.value,
      interaction: form.interaction?.id,
      executor_type: form.executor_type.value,
      executor: form.executor?.id,
      executor_group: form.executor_group?.id,
      manager_control: form.manager_control,
      controller_group: form.controller_group?.id,
      observer_group: form.observer_group?.id,
      planned_start: form.planned_start,
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

    const jsonResponse = await axios.post(`${baseUrl}/task_template_assignments/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);

    localStorage.removeItem('userPermissions');

    router.push({ name: 'TaskTemplateAssignmentDetail', params: { id: jsonResponse.data.id }  });
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
    await loadInteractions();
    await loadTaskTemplate();
    await loadAccounts();
    await loadGroups();
    await loadCategories();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
