<template>

  <div v-if="loading">

    <div v-if="object" class="form-page">

      <div class="form-header">
        <h1>Редактирование курса</h1>
      </div>

      <form @submit.prevent="saveChanges" class="form" id="edit-form">

        <div class="form-field">
          <label for="avatar" class="form-label">Аватар:</label>
          <input type="file" id="avatar" @change="onAvatarFileChange" class="form-input" />
          <div v-if="avatar_url" class="avatar-preview">
            <span class="avatar-preview-text">Текущий аватар:</span>
            <a :href="avatar_url" target="_blank" class="link" >{{ avatar_url }}</a>
          </div>
        </div>

        <div class="form-field">
          <label for="upload_file" class="form-label">Загружаемый курс:</label>
          <input type="file" id="upload_file" @change="onZipFileChange" class="form-input" />
          <div v-if="upload_url" class="upload_file-preview">
            <span class="upload_file-preview-text">Текущий курс:</span>
            <a :href="upload_url" target="_blank" class="link" >{{ upload_url }}</a>
          </div>
        </div>

        <div class="form-field">
          <label class="form-label">Тип курса:</label>
          <multiselect
            v-model="form.constructor_type"
            :options="constructor_types"
            :searchable="false"
            :multiple="false"
            :close-on-select="true"
            :clear-on-select="true"
            placeholder="Выберите тип курса"
            label="label"
            track-by="value"
            :preselect-first="false"
            :select-label="``"
            :deselect-label="``"
            :selected-label="``"
          />
          <span v-if="errors.constructor_type" class="error">{{ errors.constructor_type }}</span>
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
  constructor_type: '',
  name: '',
  desc: '',
  categories: [],
});

const loading = ref(false);

const constructor_types = [
  { label: 'Ispring', value: 'ispring' },
  { label: 'Articulate', value: 'articulate' },
  { label: 'Scroll', value: 'scroll' },
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

const fetchObject = async () => {
  const id = route.params.id;
  let token = localStorage.getItem('access_token');
  const validToken = isTokenValid(token);
  if (token && !validToken) { 
    router.push({ name: 'Login' });
    return;
  }

  try {
    const response = await axios.get(`${baseUrl}/courses/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    object.value = response.data;
    console.log(`Объект успешно загружен:`, object.value);
    object.value.constructor_type = constructor_types.find(option => option.value === object.value.constructor_type);
    console.log(`Объект нормализован:`, object.value);
    Object.assign(form, object.value);
    upload_url.value = object.value.upload_file || '';

  } catch (error) {
    console.error('Ошибка загрузки объекта:', error.response?.data || error.message);
  }
};

const uploadFile = ref(null);
const upload_url = ref(null);
const onZipFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    uploadFile.value = file;
    upload_url.value = URL.createObjectURL(file);
  }
};

const avatarFile = ref(null);
const avatar_url = ref(null);
const onAvatarFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    avatarFile.value = file;
    avatar_url.value = URL.createObjectURL(file);
  }
};

const errors = reactive({});
const validateForm = () => {
  errors.constructor_type = form.constructor_type.value ? '' : 'Тип курса обязателен!';
  errors.name = form.name ? '' : 'Название обязательно!';
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
      constructor_type: form.constructor_type.value,
      name: form.name,
      desc: form.desc,
      categories: form.categories.map(item => item.id),
    };

    console.log('JSON данные перед отправкой:', jsonData);

    await axios.patch(`${baseUrl}/courses/${id}/`, jsonData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log('Данные обновлены');

    if (uploadFile.value) {
      const fileFormData = new FormData();
      fileFormData.append('upload_file', uploadFile.value);
      const filePatchUrl = `${baseUrl}/courses/${id}/`;
      await axios.patch(filePatchUrl, fileFormData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Файл успешно обновлен');
    }

    if (avatarFile.value) {
      const avatarFormData = new FormData();
      avatarFormData.append('avatar', avatarFile.value);
      const avatarPatchUrl = `${baseUrl}/courses/${id}/`;
      await axios.patch(avatarPatchUrl, avatarFormData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Аватар успешно обновлен');
    }

    console.log('Изменения сохранены');
    router.push({ name: 'CourseDetail', params: { id: id } });
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
    await loadCategories();
    await fetchObject();
    loading.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
});

</script>
