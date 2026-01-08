<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Редактирование назначения на должность</h1>
      </div>

      <form v-if="object" @submit.prevent="saveChanges" class="form" id="edit-form">

        <div class="form-field">
          <label for="account" class="form-label">Сотрудник:</label>
          <multiselect
            v-model="form.account"
            :options="accounts"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите категорию"
            label="username"
            track-by="id"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
            :disabled="!!accountId"
          >
            <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
          <span v-if="errors.account" class="error">{{ errors.account }}</span>
        </div>

        <div class="form-field">
          <label for="position" class="form-label">Должность:</label>
          <multiselect
            v-model="form.position"
            :options="positions"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите должность"
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
          <span v-if="errors.position" class="error">{{ errors.position }}</span>
        </div>


        <div class="form-field">
          <label class="form-label">Тип:</label>
          <multiselect
            v-model="form.role"
            :options="roles"
            :multiple="false"
            :searchable="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите тип"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.role" class="error">{{ errors.role }}</span>
        </div>


        <div class="form-field">
          <label for="start_date" class="form-label">Дата начала работы:</label>
          <input v-model="form.start_date" id="start_date" type="date" class="form-input" />
          <span v-if="errors.start_date" class="error">{{ errors.start_date }}</span>
        </div>

        <div class="form-field">
          <label for="end_date" class="form-label">Дата окончания работы:</label>
          <input v-model="form.end_date" id="end_date" type="date" class="form-input" />
          <span v-if="errors.end_date" class="error">{{ errors.end_date }}</span>
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
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const loading = ref(false);

const accountId = route.query.accountId || '';

const object = ref(null);
const form = reactive({
  account: null,
  position: null,
  role: '',
  start_date: null,
  end_date: null,
});
const errors = reactive({});

const roles = [
  { value: 'employee', label: 'Сотрудник' },
  { value: 'manager', label: 'Менеджер' },
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
    const response = await axios.get(`${baseUrl}/placements/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log(`Объект успешно загружен:`, response.data);
    object.value = response.data;
    object.value.role = roles.find(option => option.value === object.value.role);
    console.log(`Объект нормализован:`, object.value);
    Object.assign(form, object.value);

  } catch (error) {
    console.error('Ошибка загрузки объекта:', error.response?.data || error.message);
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

const positions = ref([]);
const loadPositions = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/positions/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    positions.value = response.data.results || [];
    console.log('Должности загружены:', positions.value);
  } catch (error) {
    console.error('Ошибка при загрузке должностей:', error.response ? error.response.data : error.message);
  }
};

const validateForm = () => {
  errors.account = form.account ? '' : 'Сотрудник обязателен';
  errors.position = form.position ? '' : 'Должность обязательна';
  errors.role = form.role ? '' : 'Тип обязателен';
  errors.start_date = form.start_date ? '' : 'Дата начала обязательна';
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
      account: form.account.id,
      position: form.position.id,
      role: form.role.value,
      start_date: form.start_date,
      end_date: form.end_date,
    };
    const accountId = form.account.id

    console.log('JSON данные перед отправкой:', jsonData);

    // Отправка JSON-запроса для обновления данных пользователя
    await axios.patch(`${baseUrl}/placements/${id}/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Данные обновлены');

    router.push({ name: 'AccountDetail', params: { id: accountId }  });
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
    await loadAccounts();
    await loadPositions();
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