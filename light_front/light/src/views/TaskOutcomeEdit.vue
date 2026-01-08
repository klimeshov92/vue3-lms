<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Редактирование итога этапа</h1>
      </div>

      <form v-if="object" @submit.prevent="saveChanges" class="form" id="edit-form">

        <div class="form-field">
          <label class="form-label">Этап:</label>
          <multiselect
            v-model="form.stage"
            :options="stages"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите этап"
            label="name"
            track-by="id"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
            :disabled="!!stageId"
          >
            <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
          <span v-if="errors.stage" class="error">{{ errors.stage }}</span>
        </div>

        <div class="form-field">
          <label for="order" class="form-label">Порядок в этапе':</label>
          <input v-model="form.order" id="order" type="number" class="form-input" placeholder="Введите порядок в этапе" />
          <span v-if="errors.order" class="error">{{ errors.order }}</span>
        </div>

        <div class="form-field">
          <label for="name" class="form-label">Название:</label>
          <input v-model="form.name" id="name" type="text" class="form-input" placeholder="Введите название" required />
          <span v-if="errors.name" class="error">{{ errors.name }}</span>
        </div>

        <div class="form-field">
          <label class="form-label">Условие:</label>
          <multiselect
            v-model="form.condition"
            :options="conditions"
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
          <span v-if="errors.condition" class="error">{{ errors.condition }}</span>
        </div>

        <div v-if="form.condition?.value == 'tasks_success' || form.condition?.value == 'tasks_success_or_under_review' || form.condition?.value == 'tasks_failed' " class="form-field">
          <label class="form-label">Связаныне задачи:</label>
          <multiselect
            v-model="form.related_tasks"
            :options="tasks"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите задачи"
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
          <span v-if="errors.related_tasks" class="error">{{ errors.related_tasks }}</span>
        </div>

        <div class="form-field">
          <label class="form-label">Рамки результатов:</label>
          <multiselect
            v-model="form.result_framework"
            :options="result_frameworks"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите рамки"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.result_framework" class="error">{{ errors.result_framework }}</span>
        </div>

        <div class="form-field">
          <label for="completes_stage" class="form-label">Завершает этап:</label>
          <input v-model="form.completes_stage" id="completes_stage" type="checkbox" class="form-input" />
        </div>

        <div class="form-field">
          <label for="completes_process" class="form-label">Завершает процесс:</label>
          <input v-model="form.completes_process" id="completes_process" type="checkbox" class="form-input" />
        </div>

        <div class="form-field">
          <label class="form-label">Активируемые этапы:</label>
          <multiselect
            v-model="form.activated_stage"
            :options="stages"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите этапы"
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
          <label class="form-label">Активируемае задачи:</label>
          <multiselect
            v-model="form.activated_tasks"
            :options="tasks"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите задачи"
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
        <button type="submit" class="button" form="edit-form">Сохранить</button>
        <button type="button" @click="cancelEdit" class="button">Отмена</button>
      </div>
    </div>

  </div>

</template>

<script setup>
import { ref, reactive, onMounted, watch, computed   } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const loading = ref(false);

const object = ref(null);
const form = reactive({
  stage: null,
  order: null,
  name: '',
  condition: null,
  related_tasks: [],
  result_framework: null,
  completes_stage: false,
  completes_process: false,
  activated_stages: [],
  activated_tasks: [],
  desc: '',
});
const errors = reactive({});

const stages = ref([]);
const loadStages = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/stages/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    stages.value = response.data.results || [];
    console.log('Этапы загружены:', stages.value);
  } catch (error) {
    console.error('Ошибка при загрузке этапов:', error.response ? error.response.data : error.message);
  }
};

const stageId = route.query.stageId || '';


const conditions = [
  { label: 'Все задачи выполнены', value: 'all_tasks_success' },
  { label: 'Все задачи выполнены или на проверке', value: 'all_tasks_success_or_under_review' },
  { label: 'Любая задача провалена', value: 'any_task_failed' },
  { label: 'Указанные задачи выполнены', value: 'tasks_success' },
  { label: 'Указанные задачи выполнены или на проверке', value: 'tasks_success_or_under_review' },
  { label: 'Указанные задачи провалены', value: 'tasks_failed' },
  { label: 'Только триггеры', value: 'only_triggers' },
];

const tasks = ref([]);
const loadTasks = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/tasks/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    tasks.value = response.data.results || [];
    console.log('Задачи загружены:', tasks.value);
  } catch (error) {
    console.error('Ошибка при загрузке задач:', error.response ? error.response.data : error.message);
  }
};

const result_frameworks = [
  { label: 'Назначение', value: 'assignment' },
  { label: 'Взаимодействие', value: 'interaction' },
  { label: 'Все', value: 'all' },
];

const fetchObject = async () => {
  const id = route.params.id;
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  console.log(`Начало загрузки объекта с ID: ${id}`);

  try {
    const response = await axios.get(`${baseUrl}/stage_outcomes/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log(`Объект успешно загружен:`, response.data);
    object.value = response.data;
    object.value.condition = conditions.find(option => option.value === object.value.condition);
    object.value.result_framework = result_frameworks.find(option => option.value === object.value.result_framework);
    console.log(`Объект нормализован:`, object.value);
    Object.assign(form, object.value);

  } catch (error) {
    console.error('Ошибка загрузки объекта:', error.response?.data || error.message);
  }
};

const validateForm = () => {
  errors.stage = form.stage ? '' : 'Этап обязателен';
  errors.order = form.order ? '' : 'Порядок в этапе обязателен';
  errors.name = form.name ? '' : 'Название обязательно';
  errors.condition = form.condition ? '' : 'Условие обязательно';
  if (form.condition == 'tasks_success' || form.condition == 'tasks_success_or_under_review' || form.condition == 'tasks_failed') {
    errors.related_tasks = form.related_tasks ? '' : 'Связанные задачи обязательны';
  }
  errors.result_framework = form.result_framework ? '' : 'Рамки результатов обязательны';
  return Object.values(errors).every((error) => !error);
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

    // Подготовка данных для JSON-запроса
    const jsonData = {
      stage: form.stage.id,
      order: form.order,
      name: form.name,
      condition: form.condition.value,
      related_tasks: form.related_tasks.map(item => item.id),
      result_framework: form.result_framework.value,
      completes_stage: form.completes_stage,
      completes_process: form.completes_process,
      ...(form.activated_stages && { activated_stages: form.activated_stages.map(item => item.id) }),
      ...(form.activated_tasks && { activated_tasks: form.activated_tasks.map(item => item.id) }),
      desc: form.desc,
    };
    const stageId = form.stage.id

    console.log('JSON данные перед отправкой:', jsonData);

    await axios.patch(`${baseUrl}/stage_outcomes/${id}/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Данные обновлены');

    router.push({ name: 'StageDetail', params: { id: stageId }  });
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
  router.back();
};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await loadStages();
    await loadTasks();
    await fetchObject();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>
/* Добавьте стили при необходимости */
</style>