<template>

  <div v-if="loading">

    <div v-if="object" class="form-page">

      <div class="form-header">
        <h1>Редактирование настроек оповещений</h1>
      </div>

      <form @submit.prevent="saveChanges" class="form" id="edit-form">

        <div class="form-field">
          <label class="form-label">Аккаунт:</label>
          <multiselect
            v-model="form.account"
            :options="accounts"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите аккаунта"
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
          <span v-if="errors.account" class="error">{{ errors.account }}</span>
        </div>

        <div class="form-field">
          <label for="self_tasks_tracking" class="form-label">Отслеживание своих задач:</label>
          <input v-model="form.self_tasks_tracking" id="self_tasks_tracking" type="checkbox" class="form-input" />
        </div>
        
        <div class="form-field">
          <label for="controlled_tasks_tracking" class="form-label">Отслеживание задач на контроле:</label>
          <input v-model="form.controlled_tasks_tracking" id="controlled_tasks_tracking" type="checkbox" class="form-input" />
        </div>

        <div class="form-field">
          <label for="observed_tasks_tracking" class="form-label">Отслеживание задач под наблюдением:</label>
          <input v-model="form.observed_tasks_tracking" id="observed_tasks_tracking" type="checkbox" class="form-input" />
        </div>

        <div class="form-field">
          <label for="self_tasks_reminder_period" class="form-label">Период напоминания для своих задач (дней):</label>
          <input 
            v-model="form.self_tasks_reminder_period" 
            id="self_tasks_reminder_period" 
            type="number" 
            class="form-input" 
            placeholder="Введите период в днях"
          />
          <span v-if="errors.self_tasks_reminder_period" class="error">{{ errors.self_tasks_reminder_period }}</span>
        </div>

        <div class="form-field">
          <label for="controlled_tasks_reminder_period" class="form-label">Период напоминания для задач на контроле (дней):</label>
          <input 
            v-model="form.controlled_tasks_reminder_period" 
            id="controlled_tasks_reminder_period" 
            type="number" 
            class="form-input" 
            placeholder="Введите период в днях"
          />
          <span v-if="errors.controlled_tasks_reminder_period" class="error">{{ errors.controlled_tasks_reminder_period }}</span>
        </div>

        <div class="form-field">
          <label for="observed_tasks_reminder_period" class="form-label">Период напоминания для задач под наблюдением (дней):</label>
          <input 
            v-model="form.observed_tasks_reminder_period" 
            id="observed_tasks_reminder_period" 
            type="number" 
            class="form-input" 
            placeholder="Введите период в днях"
          />
          <span v-if="errors.observed_tasks_reminder_period" class="error">{{ errors.observed_tasks_reminder_period }}</span>
        </div>

      </form>

      <div class="form-menu button-group">
        <button type="submit" class="button" form="edit-form">Сохранить</button>
        <button type="button" @click="cancelEdit" class="button">Отмена</button>
      </div>
    </div>

    <div v-else class="none-card">
      <div>Объект не найден</div>
    </div>

  </div>

  <div v-else class="loading">
    <div>Загрузка данных...</div>
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

const object = ref(null);
const form = reactive({
  account: null,
  self_tasks_tracking: false,
  controlled_tasks_tracking: false,
  observed_tasks_tracking: false,
  self_tasks_reminder_period: null,
  controlled_tasks_reminder_period: null,
  observed_tasks_reminder_period: null,
});

const loading = ref(false);

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

const fetchObject = async () => {
  const id = route.params.id;
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/notification_settings/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    object.value = response.data;
    console.log(`Объект успешно загружен:`, object.value);
    Object.assign(form, object.value);

  } catch (error) {
    console.error('Ошибка загрузки объекта:', error.response?.data || error.message);
  }
};

const errors = reactive({});
const validateForm = () => {
  errors.account = form.account ? '' : 'Аккаунт обязателен!';
  errors.self_tasks_reminder_period = form.self_tasks_reminder_period ? '' : 'Период напоминания для своих задач обязателен!';
  errors.controlled_tasks_reminder_period = form.controlled_tasks_reminder_period ? '' : 'Период напоминания для задач на контроле обязателен!';
  errors.observed_tasks_reminder_period = form.observed_tasks_reminder_period ? '' : 'Период напоминания для задач обязателен!';
  return Object.values(errors).every((err) => !err);
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

  const jsonData = {
    account: form.account?.id,
    self_tasks_tracking: form.self_tasks_tracking,
    controlled_tasks_tracking: form.controlled_tasks_tracking,
    observed_tasks_tracking: form.observed_tasks_tracking,
    self_tasks_reminder_period: form.self_tasks_reminder_period,
    controlled_tasks_reminder_period: form.controlled_tasks_reminder_period,
    observed_tasks_reminder_period: form.observed_tasks_reminder_period,
  };

    console.log('JSON данные перед отправкой:', jsonData);

    await axios.patch(`${baseUrl}/notification_settings/${id}/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Данные обновлены');

    router.push({ name: 'Cabinet'});
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
    await fetchObject();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>
