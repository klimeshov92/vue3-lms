<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание топика</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">

        <div class="form-field">
          <label class="form-label">Тип топика:</label>
          <multiselect
            v-model="form.topic_type"
            :options="topic_types"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите тип топика"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
            :disabled="!!taskId || !!queueId"
          />
          <span v-if="errors.topic_type" class="error">{{ errors.topic_type }}</span>
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

        <div v-if="form.topic_type.value == 'common_topic'" class="form-field">
          <label for="name" class="form-label">Название:</label>
          <input v-model="form.name" id="name" type="text" class="form-input" placeholder="Введите название" required />
          <span v-if="errors.name" class="error">{{ errors.name }}</span>
        </div>

        <div v-if="form.topic_type.value == 'task_topic'" class="form-field">
          <label class="form-label">Задача:</label>
          <multiselect
            v-model="form.task"
            :options="tasks"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите задачу"
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
          <span v-if="errors.task" class="error">{{ errors.task }}</span>
        </div>

        <div v-if="form.topic_type.value == 'queue_topic'" class="form-field">
          <label class="form-label">Очередь:</label>
          <multiselect
            v-model="form.queue"
            :options="queues"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите очередь"
            label="str"
            track-by="id"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
            :disabled="!!queueId"
          >
            <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
          <span v-if="errors.queue" class="error">{{ errors.queue }}</span>
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
  topic_type: '',
  task: null,
  queue: null,
  name: '',
  desc: '',
  categories: [],
});

const loading = ref(false);

const topic_types = [
  { label: 'Обычный топик', value: 'common_topic' },
  { label: 'Топик задачи', value: 'task_topic' },
  { label: 'Топик очереди', value: 'queue_topic' },
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

const taskId = route.query.taskId || '';

const loadTaskById = () => {
  if (taskId) {
    console.log('Task ID:', taskId);
    const task = tasks.value.find(task => task.id === parseInt(taskId, 10));
    if (task) {
      form.task = task;
    } else {
      console.error('Task не найден.');
    }
  } else {
    console.log('Task ID не найден.');
  }
};

const queues = ref([]);
const loadQueues = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/queues/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    queues.value = response.data.results || [];
    console.log('Очереди загружены:', queues.value);
  } catch (error) {
    console.error('Ошибка при загрузке очередей:', error.response ? error.response.data : error.message);
  }
};

const queueId = route.query.queueId || '';

const loadQueueById = () => {
  if (queueId) {
    console.log('Queue ID:', queueId);
    const queue = queues.value.find(queue => queue.id === parseInt(queueId, 10));
    if (queue) {
      form.queue = queue;
    } else {
      console.error('Queue не найден.');
    }
  } else {
    console.log('Queue ID не найден.');
  }
};

watch(
  () => form.task_type,
  (newValue) => {
    if (newValue.value != 'common_topic') {
      form.name = '';
    }
    if (newValue.value != 'task_topic') {
      form.task = null;
    }
    if (newValue.value != 'queue_topic') {
      form.queue = null;
    }
  }
);

const cancelEdit = () => {
  const taskId = route.query.taskId || '';
  const queueId = route.query.queueId || '';
  if (taskId){
    router.push({ name: 'TaskDetail', params: { id: taskId }  });
  } else if (queueId){
    router.push({ name: 'QueueDetail', params: { id: queueId }  });
  } else {
    router.push({ name: 'TaskList' });
  }
};

const errors = reactive({});
const validateForm = () => {
  if (form.task_type == 'common_topic') {
    errors.name = form.name ? '' : 'Название обязательно!';
  }
  if (form.task_type == 'task_topic') {
    errors.task = form.task ? '' : 'Задача обязательна!';
  }
  if (form.task_type == 'queue_topic') {
    errors.queue = form.queue ? '' : 'Очередь обязательна!';
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
      topic_type: form.topic_type.value,
      task: form.task?.id,
      queue: form.queue?.id,
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

    const jsonResponse = await axios.post(`${baseUrl}/topics/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);

    const taskId = route.query.taskId || '';
    const queueId = route.query.queueId || '';
    if (taskId){
      router.push({ name: 'TaskDetail', params: { id: taskId }  });
    } else if (queueId){
      router.push({ name: 'QueueDetail', params: { id: queueId }  });
    } else {
      router.push({ name: 'TopicDetail', params: { id: jsonResponse.data.id }  });
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
    await loadCategories();
    await loadTasks();
    await loadTaskById();
    await loadQueues();
    await loadQueueById();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
