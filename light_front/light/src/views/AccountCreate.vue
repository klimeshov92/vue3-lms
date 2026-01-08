<template>

  <div v-if="loading">

    <div class="form-page">
      <div class="form-header">
        <h1>Создание аккаунта</h1>
      </div>

      <form @submit.prevent="createObject" class="form" id="form">
        <div class="form-field">
          <label for="avatar" class="form-label">Аватар:</label>
          <input type="file" id="avatar" @change="onFileChange" class="form-input" />
        </div>

        <div class="form-field">
          <label for="username" class="form-label">Имя пользователя:</label>
          <input v-model="form.username" id="username" type="text" class="form-input" placeholder="Введите имя пользоваетля" required />
          <span v-if="errors.username" class="error">{{ errors.username }}</span>
        </div>

        <div class="form-field">
          <label for="email" class="form-label">Электронная почта:</label>
          <input v-model="form.email" id="email" type="email" class="form-input" placeholder="Введите электронную почту" required />
          <span v-if="errors.email" class="error">{{ errors.email }}</span>
        </div>

        <div class="form-field">
          <label for="password" class="form-label">Пароль:</label>
          <div class="password-wrapper">
            <input 
            v-model="form.password" 
            :type="isPasswordVisible ? 'text' : 'password'"
            id="password" 
            class="form-input password-input"
            placeholder="Введите пароль"
            required 
            />
            <span class="toggle-password" @click="togglePasswordVisibility">{{ isPasswordVisible ? '👁️' : '👁️‍🗨️' }}</span>
          </div>
          <span v-if="errors.password" class="error">{{ errors.password }}</span>
        </div>

        <div class="form-field">
          <label for="last_name" class="form-label">Фамилия:</label>
          <input v-model="form.last_name" id="last_name" type="text" class="form-input" placeholder="Введите фамилия"/>
        </div>

        <div class="form-field">
          <label for="first_name" class="form-label">Имя:</label>
          <input v-model="form.first_name" id="first_name" type="text" class="form-input" placeholder="Введите имя"/>
        </div>

        <div class="form-field">
          <label for="fathers_name" class="form-label">Отчество:</label>
          <input v-model="form.fathers_name" id="fathers_name" type="text" class="form-input" placeholder="Введите отчество"/>
        </div>

        <div class="form-field">
          <label for="is_active" class="form-label">Активен:</label>
          <input v-model="form.is_active" id="is_active" type="checkbox" class="form-input" />
        </div>

        <div class="form-field">
          <label class="form-label">Права:</label>
          <multiselect
            v-model="form.user_permissions"
            :options="permissions"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder="Выберите права"
            label="codename"
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
          <label class="form-label">Группы:</label>
          <multiselect
            v-model="form.groups"
            :options="groups"
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
          <label for="is_staff" class="form-label">Пользователь административной панели:</label>
          <input v-model="form.is_staff" id="is_staff" type="checkbox" class="form-input" />
        </div>

        <div class="form-field">
          <label for="is_superuser" class="form-label">Суперпользователь:</label>
          <input v-model="form.is_superuser" id="is_superuser" type="checkbox" class="form-input" />
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
import { reactive, onMounted, ref } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';
import Multiselect from 'vue-multiselect';
import '../assets/styles/custom-multiselect.css';
import { baseUrl, isTokenValid } from '../utils/utils';

const route = useRoute();
const router = useRouter();

const form = reactive({
  username: '',
  email: '',
  password: '',
  last_name: '',
  first_name: '',
  fathers_name: '',
  is_active: true,
  user_permissions: [],
  groups: [],
  is_staff: false,
  is_superuser: false,
});

const loading = ref(false);



const permissions = ref([]);
const loadPermissions = async () => {
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/permissions/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    permissions.value = response.data.results || [];
    console.log('Разрешения загружены:', permissions.value);
  } catch (error) {
    console.error('Ошибка при загрузке разрешений:', error.response ? error.response.data : error.message);
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
    const response = await axios.get(`${baseUrl}/groups/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    groups.value = response.data.results || [];
    console.log('Группы загружены:', groups.value);
  } catch (error) {
    console.error('Ошибка при загрузке групп:', error.response ? error.response.data : error.message);
  }
};

const avatarFile = ref(null);
const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    avatarFile.value = file;
  }
};

const isPasswordVisible = ref(false);
const togglePasswordVisibility = () => {
  isPasswordVisible.value = !isPasswordVisible.value;
};

const cancelEdit = () => {
  router.push({ name: 'AccountList' });
};

const errors = reactive({});
const validateForm = () => {
  errors.username = form.username ? '' : 'Имя пользователя обязательно!';
  errors.email = form.email ? '' : 'Электронная почта обязательна!';
  errors.password = form.password ? '' : 'Пароль обязателен!';
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
      username: form.username,
      email: form.email,
      password: form.password,
      first_name: form.first_name,
      last_name: form.last_name,
      fathers_name: form.fathers_name,
      is_active: form.is_active,
      is_staff: form.is_staff,
      is_superuser: form.is_superuser,
      user_permissions: form.user_permissions.map(item => item.id),
      groups: form.groups.map(item => item.id),
    };

    console.log('JSON данные перед отправкой:', jsonData);
    let token = localStorage.getItem('access_token');
    const validToken = isTokenValid(token);
    if (token && !validToken) { 
      router.push({ name: 'Login' });
      return;
    }

    const jsonResponse = await axios.post(`${baseUrl}/accounts/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Объект создан:', jsonResponse.data);

    if (avatarFile.value) {
      const avatarFormData = new FormData();
      avatarFormData.append('avatar', avatarFile.value);

      const avatarPatchUrl = `${baseUrl}/accounts/${jsonResponse.data.id}/`;
      const avatarPatchResponse = await axios.patch(avatarPatchUrl, avatarFormData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Аватар успешно обновлен:', avatarPatchResponse.data);
    }

    router.push({ name: 'AccountDetail', params: { id: jsonResponse.data.id }  });
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
    await loadPermissions();
    await loadGroups();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>

<style scoped>

</style>
