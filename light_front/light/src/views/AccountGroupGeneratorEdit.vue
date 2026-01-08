<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Редактирование сотрудников</h1>
      </div>

      <form v-if="object" @submit.prevent="saveChanges" class="form" id="edit-form">
        <div class="form-field">
          <label for="group" class="form-label">Группа:</label>
          <multiselect
            v-model="form.group"
            :options="groups"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите группу"
            label="name"
            track-by="id"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
            :disabled="!!groupId"
          >
          <template #noOptions>
              <span>Список пуст</span>
            </template>
            <template #noResult>
              <span>Ничего не найдено</span>
            </template>
          </multiselect>
          <span v-if="errors.group" class="error">{{ errors.group }}</span>
        </div>

        <div class="form-field">
          <label class="form-label">Добавляемые аккунты:</label>
          <multiselect
            v-model="form.added_users"
            :options="filteredAddedUsers"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите аккаунты"
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
          <label class="form-label">Исключаемые аккунты:</label>
          <multiselect
            v-model="form.excluded_users"
            :options="filteredExcludedUsers"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите аккаунты"
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
          <label class="form-label">Добавляемые группы:</label>
          <multiselect
            v-model="form.added_groups"
            :options="filteredAddedGroups"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите группы"
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
          <label class="form-label">Исключаемые группы:</label>
          <multiselect
            v-model="form.excluded_groups"
            :options="filteredExcludedGroups"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите группы"
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
          <label for="use_days_worked" class="form-label">Учитывать отработанные дни:</label>
          <input v-model="form.use_days_worked" id="use_days_worked" type="checkbox" class="form-input" />
        </div>

        <div v-if="form.use_days_worked" class="form-field">
          <label for="days_worked_gte" class="form-label">Отработано от (дней):</label>
          <input v-model="form.days_worked_gte" id="days_worked_gte" type="number" class="form-input" placeholder="Введите минимальное количество отработанных дней" />
        </div>

        <div v-if="form.use_days_worked" class="form-field">
          <label for="days_worked_lte" class="form-label">Отработано до (дней):</label>
          <input v-model="form.days_worked_lte" id="days_worked_lte" type="number" class="form-input" placeholder="Введите максимальное количество отработанных дней" />
        </div>

        <div class="form-field">
          <label for="autoupdate" class="form-label">Автообновление:</label>
          <input v-model="form.autoupdate" id="autoupdate" type="checkbox" class="form-input" />
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
import { watch, computed, ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const loading = ref(false);

const groupId = route.query.groupId || '';

const object = ref(null);
const form = reactive({
  group: null,
  added_users: [],
  excluded_users: [],
  added_groups: [],
  excluded_groups: [],
  use_days_worked: false,
  days_worked_gte: null,
  days_worked_lte: null,
  autoupdate: false,
});

watch(
  () => form.use_days_worked,
  (newValue) => {
    if (!newValue) {
      form.days_worked_gte = null;
      form.days_worked_lte = null;
    }
  }
);

const errors = reactive({});

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
    const response = await axios.get(`${baseUrl}/group_generators/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log(`Объект успешно загружен:`, response.data);
    object.value = response.data;
    Object.assign(form, object.value);

    if (form.days_worked_gte || form.days_worked_lte) {
      form.use_days_worked = true;
    }

  } catch (error) {
    console.error('Ошибка загрузки объекта:', error.response?.data || error.message);
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

const filteredAddedUsers = computed(() => {
  return accounts.value.filter(
    (account) => !form.excluded_users.some((excluded) => excluded.id === account.id)
  );
});

const filteredExcludedUsers = computed(() => {
  return accounts.value.filter(
    (account) => !form.added_users.some((added) => added.id === account.id)
  );
});

const filteredAddedGroups = computed(() => {
  return groups.value.filter(
    (group) => !form.excluded_groups.some((excluded) => excluded.id === group.id)
  );
});

const filteredExcludedGroups = computed(() => {
  return groups.value.filter(
    (group) => !form.added_groups.some((added) => added.id === group.id)
  );
});

const validateForm = () => {
  if (!form.group) {
    errors.group = 'Группа обязательна';
  } else if (form.group.type !== 'custom') {
    errors.group = 'Группа должна быть пользовательской';
  } else {
    errors.group = '';
  }
  console.log('Тип группы:', form.group.type);
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
      group: form.group.id,
      added_users: form.added_users.map(user => user.id),
      excluded_users: form.excluded_users.map(user => user.id),
      added_groups: form.added_groups.map(group => group.id),
      excluded_groups: form.excluded_groups.map(group => group.id),
      days_worked_gte: form.days_worked_gte,
      days_worked_lte: form.days_worked_lte,
      autoupdate: form.autoupdate,
    };
    const groupId = form.group.id

    console.log('JSON данные перед отправкой:', jsonData);

    // Отправка JSON-запроса для обновления данных пользователя
    await axios.patch(`${baseUrl}/group_generators/${id}/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Данные обновлены');

    router.push({ name: 'AccountGroupDetail', params: { id: groupId }  });
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
    await loadGroups();
    await loadAccounts();
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