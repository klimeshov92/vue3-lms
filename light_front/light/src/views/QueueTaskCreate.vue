<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание задачи очереди</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">

        <div class="form-field">
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

        <div class="form-field">
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
            :disabled="form.queue.auto_assignment"
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

        <div class="form-field">
          <label for="item" class="form-label">Пункт:</label>
          <input v-model="form.item" id="item" type="number" class="form-input" placeholder="Введите пункт" />
          <span v-if="errors.item" class="error">{{ errors.item }}</span>
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
import { baseUrl, isTokenValid , goBackSmart } from '../utils/utils';

const router = useRouter();
const route = useRoute();

const loading = ref(false);

const form = reactive({
  queue: null,
  task: null,
  executor: null,
  item: null,
});
const errors = reactive({});

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

const validateForm = () => {
  errors.queue = form.queue ? '' : 'Очередь обязательна';
  errors.task = form.task ? '' : 'Задача обязательна';
  errors.item = form.item ? '' : 'Пункт обязателен';
  if (!form.queue.auto_assignment) {
    errors.executor = form.executor ? '' : 'Исполнитель обязателен';
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
      queue: form.queue.id,
      task: form.task.id,
      executor: form.executor.id || null,
      item: form.item,
    };
    const queueId = form.queue.id

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/queue_tasks/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);
    router.push({ name: 'QueueDetail', params: { id: queueId }  });
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
  const queueId = form.queue.id
  router.push({ name: 'QueueDetail', params: { id: queueId } });
};

onMounted(async () => {
  console.log('Компонент смонтирован, начинаем загрузку данных...');
  try {
    await loadQueues();
    await loadQueueById();
    await loadAccounts();
    await loadTasks();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>
/* Добавьте стили при необходимости */
</style>
